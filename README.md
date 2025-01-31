# Hướng Dẫn Tạo MusicBot

## Bước 1: Tạo Bot Discord
1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications).
2. Nhấn **New Application** để tạo một ứng dụng mới.
3. Điều hướng đến **Bot** và nhấn **Add Bot**.
4. Tuỳ chỉnh tên, avatar của bot (tuỳ chọn).
5. Vào mục **OAuth2 > URL Generator**.
6. Trong phần **Scopes**, chọn **bot**.
7. Cuộn xuống **Bot Permissions** và cấp quyền phù hợp cho bot của bạn.
8. Sao chép URL đã tạo và dán vào trình duyệt.
9. Xác thực và thêm bot vào server của bạn.

## Bước 2: Lấy Token của Bot
1. Trong **Discord Developer Portal**, vào phần **Bot**.
2. Nếu cần, thay đổi tên hoặc ảnh đại diện của bot.
3. Trong phần **TOKEN**, nhấn **Copy** để sao chép token.
4. Dán token vào file `.env` với định dạng:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
5. Nếu không thể sao chép token, nhấn **Reset Token** để tạo token mới.

# Guide to Creating MusicBot

## Step 1: Create a Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** to create a new application.
3. Navigate to **Bot** and click **Add Bot**.
4. Customize the bot's name and avatar (optional).
5. Go to **OAuth2 > URL Generator**.
6. Under **Scopes**, select **bot**.
7. Scroll down to **Bot Permissions** and assign the necessary permissions.
8. Copy the generated URL and paste it into your browser.
9. Authenticate and add the bot to your server.

## Step 2: Get Your Bot Token
1. In **Discord Developer Portal**, go to the **Bot** section.
2. Optionally, change the bot's name or avatar.
3. In the **TOKEN** section, click **Copy** to obtain the token.
4. Paste the token into a `.env` file using the format:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
5. If you cannot copy the token, click **Reset Token** to generate a new one.