import os
from dotenv import load_dotenv
import asyncio

import nextcord
from nextcord.ext import commands

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="/",
    intents=intents,
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


async def play_sound(
    interaction: nextcord.Interaction, sound: str
):  # joins VC first then plays the sound
    if interaction.user.voice is None:
        return "You're not currently in a voice channel."

    voice_channel = interaction.user.voice.channel
    if interaction.guild.voice_client is not None:
        await interaction.guild.voice_client.disconnect()

    vc = await voice_channel.connect()

    vc.play(
        nextcord.FFmpegPCMAudio(sound),
        after=lambda e: print("done", e),
    )
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()

    return "Joined the voice channel and played the sound."


@bot.slash_command(name="boom", description="Plays a vine boom")
async def boom(interaction: nextcord.Interaction):
    await interaction.response.defer(ephemeral=True)
    message = await play_sound(interaction, "sounds/boom.mp3")
    await interaction.followup.send(message, ephemeral=True)


@bot.slash_command(name="correct", description="Plays a loud correct buzzer sound")
async def correct(interaction: nextcord.Interaction):
    await interaction.response.defer(ephemeral=True)
    message = await play_sound(interaction, "sounds/correct.mp3")
    await interaction.followup.send(message, ephemeral=True)


@bot.slash_command(name="incorrect", description="Plays a loud incorrect buzzer sound")
async def incorrect(interaction: nextcord.Interaction):
    await interaction.response.defer(ephemeral=True)
    message = await play_sound(interaction, "sounds/incorrect.mp3")
    await interaction.followup.send(message, ephemeral=True)


@bot.slash_command(name="sigma", description="Plays What The Sigma")
async def sigma(interaction: nextcord.Interaction):
    await interaction.response.defer(ephemeral=True)
    message = await play_sound(interaction, "sounds/what_the_sigma.mp3")
    await interaction.followup.send(message, ephemeral=True)


@bot.slash_command(name="disrupt", description="Plays Disrupted Sigma")
async def disrupt(interaction: nextcord.Interaction):
    await interaction.response.defer(ephemeral=True)
    message = await play_sound(interaction, "sounds/private/disrupt_sigma.mp3")
    await interaction.followup.send(message, ephemeral=True)


bot.run(TOKEN)
