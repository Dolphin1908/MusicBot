import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll",
                      description="Tạo cuộc thăm dò ý kiến",
                      usage="!poll <nội_dung>")
    async def create_poll(self, ctx, *, question):
        embed = discord.Embed(
            title="📊 Cuộc thăm dò ý kiến",
            description=question,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Thăm dò ý kiến bởi {ctx.author.display_name}")

        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")