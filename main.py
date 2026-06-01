import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import aiosqlite
import os
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("TOKEN")
MEMBER_CHANNEL = int(os.getenv("MEMBER_CHANNEL"))
ADMIN_CHANNEL = int(os.getenv("ADMIN_CHANNEL"))

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

CURRENT_ROUND = "เช้า"

# ---------------- DATABASE ----------------

async def setup_db():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            user_id INTEGER,
            nickname TEXT,
            round TEXT,
            date TEXT
        )
        """)
        await db.commit()

# ---------------- MODAL ----------------

class AttendanceModal(Modal, title="เช็คชื่อสมาชิก"):

    nickname = TextInput(
        label="ชื่อเล่น",
        placeholder="กรอกชื่อเล่น"
    )

    async def on_submit(self, interaction: discord.Interaction):

        today = datetime.now().strftime("%Y-%m-%d")

        async with aiosqlite.connect("database.db") as db:

            check = await db.execute("""
            SELECT * FROM attendance
            WHERE user_id = ?
            AND round = ?
            AND date = ?
            """,
            (
                interaction.user.id,
                CURRENT_ROUND,
                today
            ))

            data = await check.fetchone()

            if data:
                await interaction.response.send_message(
                    "❌ คุณเช็คชื่อรอบนี้แล้ว",
                    ephemeral=True
                )
                return

            await db.execute("""
            INSERT INTO attendance
            VALUES(?,?,?,?)
            """,
            (
                interaction.user.id,
                str(self.nickname),
                CURRENT_ROUND,
                today
            ))

            await db.commit()

        await interaction.response.send_message(
            f"✅ เช็คชื่อสำเร็จ\n"
            f"ชื่อเล่น : {self.nickname}\n"
            f"รอบ : {CURRENT_ROUND}",
            ephemeral=True
        )

        admin_channel = bot.get_channel(ADMIN_CHANNEL)

        embed = discord.Embed(
            title="📊 รายงานการเช็คชื่อ",
            color=0x00ff00
        )

        embed.add_field(
            name="สมาชิก",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="ชื่อเล่น",
            value=str(self.nickname),
            inline=False
        )

        embed.add_field(
            name="รอบ",
            value=CURRENT_ROUND,
            inline=False
        )

        await admin_channel.send(embed=embed)

# ---------------- BUTTON ----------------

class AttendanceButton(Button):
    def __init__(self):
        super().__init__(
            label="เช็คชื่อ",
            style=discord.ButtonStyle.green,
            emoji="✅"
        )

    async def callback(self, interaction):
        await interaction.response.send_modal(
            AttendanceModal()
        )

class AttendanceView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AttendanceButton())

# ---------------- SEND PANEL ----------------

async def send_attendance(round_name):

    global CURRENT_ROUND
    CURRENT_ROUND = round_name

    channel = bot.get_channel(MEMBER_CHANNEL)

    embed = discord.Embed(
        title="📋 ระบบเช็คชื่อสมาชิก",
        description=(
            f"รอบ : **{round_name}**\n\n"
            "กรุณากดปุ่มด้านล่างเพื่อเช็คชื่อ"
        ),
        color=0x3498db
    )

    embed.set_footer(
        text="Attendance System"
    )

    await channel.send(
        embed=embed,
        view=AttendanceView()
    )

# ---------------- READY ----------------

@bot.event
async def on_ready():

    await setup_db()

    scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")

    scheduler.add_job(
        send_attendance,
        "cron",
        day_of_week="mon",
        hour=7,
        minute=30,
        args=["เช้า"]
    )

    scheduler.add_job(
        send_attendance,
        "cron",
        day_of_week="mon",
        hour=11,
        minute=30,
        args=["เที่ยง"]
    )

    scheduler.add_job(
        send_attendance,
        "cron",
        day_of_week="mon",
        hour=19,
        minute=30,
        args=["เย็น"]
    )

    scheduler.start()

    bot.add_view(AttendanceView())

    print(f"Logged in as {bot.user}")

bot.run(TOKEN)