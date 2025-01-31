import discord
from discord.ext import commands
from config import DISCORD_TOKEN, COMMAND_PREFIX
from utils.help_view import HelpView

# Khởi tạo bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

# Thêm tham số `help_command=None` để tắt help command mặc định
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

# Tải các cogs từ thư mục `cogs`
async def load_cogs():
    for extension in ["general", "admin", "fun", "guild", "voice", "translator"]:
        try:
            await bot.load_extension(f"cogs.{extension}")  # Thêm `await`
            print(f"Loaded cog: {extension}")
        except Exception as e:
            print(f"Failed to load cog {extension}: {e}")

@bot.event
async def on_ready():
    print(f"Bot đã sẵn sàng! Đăng nhập với tên: {bot.user}")

@bot.command(name="help")
async def help_command(ctx, page: int = 1):
    cogs = list(bot.cogs.items())
    cogs_per_page = 1
    total_pages = (len(cogs) + cogs_per_page - 1) // cogs_per_page

    view = HelpView(page, total_pages, cogs, None)
    
    start = (page - 1) * cogs_per_page
    end = start + cogs_per_page
    selected_cogs = cogs[start:end]

    embed = discord.Embed(
        title=f"Danh sách lệnh - Trang {page}/{total_pages}", 
        color=discord.Color.blue())
    embed.set_footer(text=f"Dùng !help <số trang> để xem trang khác.")

    selected_cogs = cogs[:cogs_per_page]
    for cog_name, cog in selected_cogs:
        commands_list = cog.get_commands()
        cog_help = ""
        for command in commands_list:
            if not command.hidden:
                cog_help += f"🔹 **{command.name}**: {command.description or 'Không có mô tả'}\n"
        
        embed.add_field(
            name=cog_name, 
            value=cog_help or "Không có lệnh nào", 
            inline=False)

    view.sent_message = await ctx.send(embed=embed, view=view)

# Hàm khởi chạy bot
async def main():
    async with bot:
        await load_cogs()  # Gọi hàm load_cogs bất đồng bộ
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Sử dụng asyncio để chạy hàm chính