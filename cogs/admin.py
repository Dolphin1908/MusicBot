from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear",
                      description="Xóa số lượng tin nhắn",
                      usage="!clear <số_lượng>")
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Đã xóa {amount} tin nhắn!", delete_after=5)

    @commands.command(name="clearall",
                      description="Xóa toàn bộ tin nhắn",
                      usage="!clearall")
    @commands.has_permissions(manage_messages=True)
    async def clear_all_messages(self, ctx):
        await ctx.channel.purge()
        await ctx.send("Đã xóa toàn bộ tin nhắn!", delete_after=5)

    @commands.command(name="kick",
                      description="Đá ra khỏi server",
                      usage="!kick <@user> [lý_do]")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: commands.MemberConverter, *, reason=None):
        await member.kick(reason=reason)
        await member.send(f"Bạn đã bị đá ra khỏi {ctx.guild.name} với lý do: {reason}\nLiên hệ {ctx.guild.owner.mention} để biết thêm chi tiết.")
        await ctx.send(f"Đã đá {member} ra khỏi server!", delete_after=5)

    @commands.command(name="ban",
                      description="Cấm tham gia server",
                      usage="!ban <@user> [lý_do]")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: commands.MemberConverter, *, reason=None):
        await member.ban(reason=reason)
        await member.send(f"Bạn đã bị cấm tham gia {ctx.guild.name} với lý do: {reason}\nLiên hệ {ctx.guild.owner.mention} để biết thêm chi tiết.")
        await ctx.send(f"Đã cấm {member} tham gia server!", delete_after=5)

    @commands.command(name="unban",
                      description="Bỏ cấm tham gia server",
                      usage="!unban <user_id>")
    @commands.has_permissions(ban_members=True)
    async def unban_member(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"Đã bỏ cấm {user} tham gia server!", delete_after=5)

async def setup(bot):
    await bot.add_cog(Admin(bot))
