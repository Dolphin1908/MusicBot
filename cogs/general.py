from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping",
                      description="Lệnh kiểm tra kết nối",
                      usage="!ping")
    async def ping(self, ctx):
        await ctx.send('Pong!')
    
    @commands.command(name="hello",
                      description="Lệnh chào hỏi",
                      usage="!hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(General(bot))