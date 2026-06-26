# discordbot-dice

NdN形式のダイスを振る単機能 Discord Bot です。

## 環境変数

```txt
DISCORD_BOT_TOKEN=
OPS_LOG_HUB_URL=
OPS_LOG_HUB_KEY=
OPS_LOG_PROJECT=discordbot-dice
OPS_LOG_ENVIRONMENT=development
DASHBOARD_CONFIG_URL=https://dashboard.discordbot.jp/api/bot-runtime/settings
DASHBOARD_BOT_CONFIG_SECRET=
```

`OPS_LOG_HUB_URL` は `https://<ops-log-hub-domain>/api/ingest/discord-bot` の形式です。

`OPS_LOG_HUB_URL` と `OPS_LOG_HUB_KEY` が未設定の場合、Bot はログ送信なしで動作します。

## ops-log-hub に送信するイベント

- `startup`: Bot 起動時
- `command_error`: slash command または prefix command の実行エラー

通常の debug / info ログは Railway Logs に残し、`ops-log-hub` には運用判断に必要なイベントだけを送ります。

## Discord Bot JP dashboard 連携

`DASHBOARD_BOT_CONFIG_SECRET` を設定すると、Bot は `DASHBOARD_CONFIG_URL` からサーバー別設定を署名付きで取得します。
dashboard ではサーバーごとの有効/無効、最小応答間隔、基準時刻を保存できます。
Bot は無効化されたサーバーでは反応せず、最小応答間隔が設定されている場合は連続返信を抑制します。
