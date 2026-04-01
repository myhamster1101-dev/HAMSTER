import discord
from discord.ext import commands
import os

class VoiceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label='🎧 ติดต่อแอดมิน (เข้าห้องพักคอย)', style=discord.ButtonStyle.primary, custom_id='contact_v2')
    async def contact(self, interaction: discord.Interaction, button: discord.ui.Button):
        wait_room = interaction.guild.get_channel(int(os.getenv('WAITING_ROOM_ID')))
        if interaction.user.voice:
            await interaction.user.move_to(wait_room)
            await interaction.response.send_message("✅ ย้ายคุณไปห้องพักคอยแล้ว กรุณารอแอดมินสักครู่", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ กรุณาเข้าห้องเสียงก่อนกดปุ่มนี้ครับ", ephemeral=True)

class VoiceSystem(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        admin_role_id = int(os.getenv('ADMIN_ROLE_ID'))
        wait_room_id = int(os.getenv('WAITING_ROOM_ID'))
        if after.channel and after.channel.id != wait_room_id:
            if any(role.id == admin_role_id for role in member.roles):
                wait_room = member.guild.get_channel(wait_room_id)
                if wait_room and wait_room.members:
                    for m in wait_room.members:
                        try: await m.move_to(after.channel)
                        except: pass

    @commands.command()
    async def setup_voice(self, ctx):
        embed = discord.Embed(title="📞 ศูนย์ติดต่อแอดมิน", description="หากมีปัญหาต้องการปรึกษา กดปุ่มด้านล่างเพื่อรอพบแอดมิน", color=0x3498db)
        embed.set_footer(text="Developed by p.hxmster")
        await ctx.send(embed=embed, view=VoiceView())

async def setup(bot):
    await bot.add_cog(VoiceSystem(bot))
    bot.add_view(VoiceView())
