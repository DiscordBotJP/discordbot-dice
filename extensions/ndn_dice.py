import discord
from discord.ext import commands
from daug.utils.dpyexcept import excepter
from random import randint
import re
import time

from utils.dashboard_config import DashboardConfigCache

ndnpattern = re.compile(r'(\d+)d(\d+)')


class NDNDiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dashboard_config = DashboardConfigCache()
        self.last_response_at_by_guild: dict[int, float] = {}

    @commands.Cog.listener()
    @excepter
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        match = ndnpattern.fullmatch(message.content)
        if match is None:
            return
        if message.guild is not None:
            settings = await self.dashboard_config.get()
            dashboard_setting = settings.for_guild(message.guild.id)
            if not dashboard_setting.enabled:
                return
            last_response_at = self.last_response_at_by_guild.get(message.guild.id, 0)
            interval_seconds = dashboard_setting.interval_minutes * 60
            if interval_seconds > 0 and time.monotonic() - last_response_at < interval_seconds:
                return
        else:
            dashboard_setting = None

        m, n = map(int, match.groups())
        max_rolls = dashboard_setting.max_dice_rolls if dashboard_setting else 100
        max_sides = dashboard_setting.max_dice_sides if dashboard_setting else 10000
        if m < 1 or n < 2:
            await message.reply('1回以上、2面以上の NdN 形式で指定してください。')
            return
        if m > max_rolls or n > max_sides:
            await message.reply(f'{max_sides}面{max_rolls}回({max_rolls}d{max_sides})まで対応しています。')
            return
        rolls = [randint(1, n) for _ in range(m)]
        roll_sum = sum(rolls)
        results = [
            f'{n}面ダイスを{m}回振りました',
            f'出目: {", ".join(str(x) for x in rolls)}',
            f'合計: {roll_sum}',
        ]
        response = '\n'.join(results)
        await message.reply(response)
        if message.guild is not None:
            self.last_response_at_by_guild[message.guild.id] = time.monotonic()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NDNDiceCog(bot))
