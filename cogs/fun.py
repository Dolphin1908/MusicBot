from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", 
                      description="Lệnh tung xúc xắc",
                      usage="!roll [số_mặt]")
    async def roll_dice(self, ctx, sides: int = 6):
        result = random.randint(1, sides)
        await ctx.send(f"🎲 Bạn tung được: {result}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
