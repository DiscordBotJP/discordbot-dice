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

        m, n = map(int, match.groups())
        if m > 100 or n > 10000:
            await message.reply('10000面100回(100d10000)以上は対応していません。')
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
