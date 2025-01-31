import discord
from discord.ext import commands

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guild",
                      description="Thông tin server",
                      usage="!guild")
    async def guild_info(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"{guild.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=guild.owner.mention)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Guild(bot))