import discord
from discord.ui import Button, View

class HelpView(View):
    def __init__(self, page: int, total_pages: int, cog_list: list, sent_message: discord.Message):
        super().__init__(timeout=30)  # Timeout có thể được điều chỉnh lâu hơn
        self.page = page
        self.total_pages = total_pages
        self.cog_list = cog_list
        self.sent_message = sent_message

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, row=1)
    async def previous_page(self, button: Button, interaction: discord.Interaction = None):
        if self.page > 1:
            self.page -= 1
            await self.update_help_page()

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, row=1)
    async def next_page(self, button: Button, interaction: discord.Interaction = None):
        if self.page < self.total_pages:
            self.page += 1
            await self.update_help_page()

    async def update_help_page(self):
        cogs_per_page = 1  # Hiển thị mỗi trang 1 cog
        start = (self.page - 1) * cogs_per_page
        end = start + cogs_per_page
        selected_cogs = self.cog_list[start:end]

        await self.update_buttons()

        embed = discord.Embed(
            title=f"📖 Danh sách lệnh - Trang {self.page}/{self.total_pages}",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Dùng !help <số trang> để xem trang khác.")

        for cog_name, cog in selected_cogs:
            commands_list = cog.get_commands()
            cog_help = ""
            for command in commands_list:
                if not command.hidden:
                    cog_help += f"🔹 **{command.name}**: {command.description or 'Không có mô tả'}\n"

            embed.add_field(
                name=f"**{cog_name}**",
                value=cog_help or "Không có lệnh nào.",
                inline=False
            )
        await self.sent_message.edit(embed=embed, view=self)

    async def update_buttons(self):
        previous_button = self.children[0]
        next_button = self.children[1]

        if self.page == 1:
            previous_button.disabled = True
        else:
            previous_button.disabled = False

        if self.page == self.total_pages:
            next_button.disabled = True
        else:
            next_button.disabled = False