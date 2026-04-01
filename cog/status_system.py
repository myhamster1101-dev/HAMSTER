import discord
from discord.ext import commands
import datetime

class StatusSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        guild = ctx.guild
        online_members = sum(1 for m in guild.members if m.status != discord.Status.offline)
        total_members = guild.member_count
        
        embed = discord.Embed(
            title="🖥️ SERVER NETWORK STATUS",
            description="ตรวจสอบสถานะการทำงานของระบบและจำนวนประชากรในขณะนี้",
            color=0x2ecc71, # สีเขียวแสดงถึงความ Online
            timestamp=datetime.datetime.now()
        )
        
        # ตกแต่งข้อมูลด้วย Emoji และ Code Block
        embed.add_field(name="🌐 Server Status", value="```diff\n+ Online & Stable\n```", inline=False)
        embed.add_field(name="👥 Total Members", value=f"**{total_members}** คน", inline=True)
        embed.add_field(name="🟢 Online Now", value=f"**{online_members}** คน", inline=True)
        embed.add_field(name="📊 Server Level", value=f"Level {guild.premium_tier}", inline=True)
        
        # ใส่รูปภาพแบนเนอร์ (เปลี่ยน URL เป็นรูปของคุณได้)
        embed.set_image(url="https://i.imgur.com/rN975W6.png") 
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.set_footer(text=f"Requested by {ctx.author.name} | p.hxmster System")

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 **Pong!** ความเร็วบอท: `{latency}ms`")

async def setup(bot):
    await bot.add_cog(StatusSystem(bot))
