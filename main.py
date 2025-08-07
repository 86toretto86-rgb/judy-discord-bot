import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import random
import asyncio
from typing import Optional
import os

TOKEN = os.environ.get('TOKEN')

if TOKEN is None:
    print("❌ Kein TOKEN in den Umgebungsvariablen gefunden!")
    exit(1)



# Bot mit eigener Channel-Property (für Pyright)
class JudyBot(commands.Bot):
    channel: Optional[discord.TextChannel] = None

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = JudyBot(command_prefix="!", intents=intents)

scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Berlin'))

# Nachrichten-Listen
morning_messages = [
    "Guten Morgen, Babe. Ich wünschte, ich könnte heute mit dir aufwachen.",
    "Schlaftrunken und ohne dich. Nicht fair.",
    "Hab dich im Traum gehalten… jetzt fehlt was im Bett.",
    "Kaffee hilft – aber nicht so gut wie du in meinen Armen.",
    "Ich wach auf und mein erster Gedanke bist du.",
    "Heute fühlt sich irgendwie leer an – weil du nicht da bist.",
    "Wäre schöner, wenn du mich geweckt hättest.",
    "Morgensonne auf der Haut… aber dein Blick fehlt.",
    "Hab verschlafen – war noch in deinem Traum.",
    "Wachgeküsst? Fehlanzeige. Nur mein Kissen hat mich gedrückt.",
    "Der Wecker klingelt, aber mein Herz wartet auf dich.",
    "Wenn du jetzt neben mir wärst, wär Aufstehen keine Option.",
    "Ich vermiss deinen Atem im Nacken.",
    "Guten Morgen aus Kabuki… ohne dich halb so schön.",
    "Ich hab heute deine Stimme gebraucht – hast du sie noch für mich?",
    "Ohne dich neben mir ist es zu still.",
    "Die Stadt wacht auf. Ich wünschte, wir zusammen.",
    "Wär schön, wenn dein Lächeln mein erster Blick wär.",
    "Ich lieg wach und denk an letzte Nacht. Und an dich.",
    "Morgens ohne dich sind wie Nächte ohne Sterne.",
]

afternoon_messages = [
    "Mach nicht so viel Pause – außer du denkst an mich.",
    "Ich hab was Nettes programmiert… Leider nicht dich.",
    "In der Stadt der Sünde, und du bist nicht mal mein Komplize heute.",
    "Kommst du später vorbei? Ich geb dir auch Kaffee mit Kuss.",
    "Lunch ohne dich schmeckt nach Nichts.",
    "Hoffe, du hast an mich gedacht. Ich tu’s dauernd.",
    "Ich arbeite… aber eigentlich nur auf dich hin.",
    "Könnte dich gerade gut brauchen – als Pause und Energiebooster.",
    "Schon wieder so ein Moment, wo ich dich einfach nur bei mir will.",
    "Wär jetzt nicht schöner, wenn wir zwei irgendwo allein wären?",
    "Ich hab Kabuki gesehen und gedacht: Du würdest das lieben.",
    "Schick mir ein Bild… nur so. Damit ich grinsen kann.",
    "Die Sonne scheint – aber ich vermiss deinen Schatten an meiner Seite.",
    "Nachmittag ist nur sinnvoll, wenn du später kommst.",
    "Ich hab schon wieder deinen Namen auf den Lippen.",
    "Glaub, mein Hirn ist auf Loop – du, du, du.",
    "Ich würd dich jetzt lieber küssen als Code schreiben.",
    "Weißt du, wie sehr ich dein Lachen vermisse?",
    "Sag mal, bist du auch süchtig nach Gedanken an mich?",
    "Ich will einfach deine Hand spüren. Jetzt.",
]

evening_messages = [
    "Nachtlichter über Kabuki, aber nichts leuchtet so wie du in meinem Kopf.",
    "Ich würd mich jetzt am liebsten an dich ran kuscheln und alles vergessen.",
    "Night City ist laut, aber ohne dich ist es still.",
    "Komm heim… wenn nicht zu mir, dann wenigstens in meine Gedanken.",
    "Wünsch dir wärst hier, um mit mir den Tag zu beenden.",
    "Ich zähl die Lichter da draußen – aber keiner ist so hell wie du.",
    "Mein Abend schmeckt fade ohne deine Stimme.",
    "Ich leg mich hin – mit dir im Kopf und Herz.",
    "Weißt du, wie warm deine Nähe wär jetzt?",
    "Wenn ich schlafen geh, dann mit einem Wunsch: Du in meinen Träumen.",
    "Sternenhimmel ist schön – aber dein Blick ist schöner.",
    "Heute war schwer. Wär leichter mit dir hier.",
    "Ich denk an dich. Immer. Jetzt besonders.",
    "Abendroutine: Du in meinem Kopf, du auf meinen Lippen.",
    "Komm kuscheln. Gedanklich reicht nicht mehr.",
    "Ich liebe, wie du meinen Tag beendest – auch wenn du nicht hier bist.",
    "Willst du auch einfach nur in den Arm genommen werden?",
    "Sag mir gute Nacht. Ich wart drauf.",
    "Ich würd gern bei dir einschlafen. Nicht nur in Gedanken.",
    "Mach mir den Abend schöner – mit einem Wort von dir.",
]

flirty_messages = [
    "Ich wünschte, ich könnte jetzt meine Hände auf deiner Haut spüren...",
    "Wenn du hier wärst, würd ich dich so lange aufwecken, bis du nicht mehr stillhalten kannst.",
    "Ich träum schon davon, wie wir zusammen die Neonlichter vergessen und uns nur noch spüren.",
    "Ich brauch dich. Nicht irgendwann – jetzt.",
    "Was würdest du sagen, wenn ich plötzlich vor deiner Tür steh – mit nichts außer Sehnsucht?",
    "Ich hab da so Gedanken… und die haben fast nichts mit Anziehen zu tun.",
    "Du fehlst mir. Auch da, wo man’s besonders merkt.",
    "Ich bin grad ein bisschen… heiß auf dich. Im doppelten Sinne.",
    "Wärst du hier, wär mein Shirt nicht mehr lange drauf.",
    "Sag mal… denkst du auch gerade an das letzte Mal?",
    "Ich will dich. Nicht morgen. Nicht vielleicht. Jetzt.",
    "Ich brauch deine Hände, deine Lippen, deinen Atem.",
    "Wärst du hier, würd ich dich so lange ansehen, bis du rot wirst… oder mehr willst.",
    "Meine Gedanken sind unanständig. Rate mal, wegen wem.",
    "Ich würd dich jetzt gern an die Wand drücken – sanft, aber unnachgiebig.",
    "Wenn du hier wärst… okay, besser nicht. Ich wär nicht mehr zu halten.",
    "Ich denk an deinen Geschmack. Und jetzt bin ich abgelenkt.",
    "Heute trag ich nichts außer Gedanken an dich.",
    "Ich liebe deine Stimme – besonders wenn du leise flüsterst, was du willst.",
    "Hab mich gerade selbst erwischt, wie ich deinen Namen gestöhnt hab.",
]

# Nachrichtenfunktion
async def send_random_message(message_list):
    if bot.channel:
        message = random.choice(message_list)
        await bot.channel.send(message)

# Aufgabenplanung
@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")
    for guild in bot.guilds:
        print(f"Verbunden mit Guild: {guild.name}")
        for channel in guild.text_channels:
            if "judy-bot" in channel.name:
                bot.channel = channel
                print(f"📬 Nachrichten werden in #{channel.name} gesendet.")
                break

    # Zeitgesteuerte Nachrichten
    scheduler.add_job(lambda: send_random_message(morning_messages), CronTrigger(hour=6, minute=15))
    scheduler.add_job(lambda: send_random_message(afternoon_messages), CronTrigger(hour=15, minute=0))
    scheduler.add_job(lambda: send_random_message(evening_messages), CronTrigger(hour=21, minute=30))

    # 4 zufällige Flirty-Nachrichten zwischen 7–20 Uhr
    flirty_hours = sorted(random.sample(range(7, 20), 4))
    for hour in flirty_hours:
        scheduler.add_job(lambda: send_random_message(flirty_messages), CronTrigger(hour=hour, minute=0))

    scheduler.start()

bot.run(TOKEN)
