# Rocket League Code Scanner

Scans Reddit and Epic Games forums twice a day for Rocket League promo codes and sends a Telegram message when new ones are found.

## Setup

### 1. Create a GitHub repository

Create a new repository on GitHub (can be public or private) and push this entire folder to it.

### 2. Add your Telegram secrets

Go to your repository on GitHub → **Settings** → **Secrets and variables** → **Actions** → **New repository secret** and add:

| Secret name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather (e.g. `123456789:ABCdef...`) |
| `TELEGRAM_CHAT_ID` | Your personal chat ID (e.g. `987654321`) |

> **How to get your chat ID:** Start a chat with your bot, then open this URL in a browser (replace TOKEN):
> `https://api.telegram.org/botTOKEN/getUpdates`
> Look for `"id"` inside `"chat"`.

### 3. Test it manually

Go to the **Actions** tab → **Rocket League Code Scanner** → **Run workflow**.

Check the job logs to confirm it ran without errors. If codes are found, you'll get a Telegram message.

### 4. Let it run automatically

The scanner runs automatically at **08:00 UTC** and **20:00 UTC** every day. After each run, `seen_codes.json` is automatically committed back to the repo to track which codes were already found (so you won't get duplicate alerts).

## How to redeem a code

**Main Menu → Extras → Redeem Code**
