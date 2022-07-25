import discord
from discord.ext import commands
from datetime import datetime
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os

bot = commands.Bot(command_prefix="$", description="This is a daily bot")

names = {
    "cobrador73": "Matheus",
    "EduardoPicolo": "Eduardo",
    "There Is No Hope": "Pedro",
    "SamuelNog": "Samuel",
    "Sayuck": "Roberto",
    "brun0sk#3553": "Bruno",
    "davess#2780": "Davi",
    "Giovanni A.#3341": "Giovanni",
    "GG#9631": "Guilherme",
    "nicolas-souza#3761": "Nicolas",
    "Antogalatic#0160": "Rodrigo",
    "Caldas#5891": "Algusto",
}

coleted = []


async def func():
    # send message in daily channel
    global coleted
    channel = bot.get_channel(1000926747891601610)
    coleted = []
    await channel.send("@everyone Não esqueçam de responder sua Daily hoje!")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Coleta daily"))

    scheduler = AsyncIOScheduler()

    scheduler.add_job(func, CronTrigger(hour=7, minute=0, second=20), args=[])
    scheduler.start()

    print("My Ready is Body")


@bot.command()
async def table(ctx):
    channel = bot.get_channel(1000926747891601610)
    await channel.send("@everyone", file=discord.File("table.md"))
    await ctx.send("Enviado!")


@bot.command()
async def template(ctx):
    await ctx.send(
        "O Template é:\n\n"
        + "Ontem: Relato do trabalho feito ontem\n"
        + "Hoje: Relato do trabalho que pretende-se realizar hoje\n"
        + "Bloqueio: Não para quando não existir e uma descrição"
        + " para o caso de haver bloqueio\n"
    )


@bot.command()
async def daily(ctx, message: str):
    splitted_message = message.split(" ")
    print(f"message: {message}")
    await ctx.send(f"Daily de {ctx.author.name} coletada!")


@bot.command()
async def xingue(ctx, message: str):
    print(f"message: {message}")
    insultos = [
        "corno",
        "vagabundo",
        "miseravel",
        "equino",
        "largado",
        "perdido",
        "careca",
        "bastardo",
        "bicha",
        "inseminado",
        "inseto",
        "gorila",
        "cachorro",
        "feio",
        "bobo",
        "bosta",
    ]
    await ctx.send(f"O {message} é um {random.choice(insultos)}!")


@bot.listen()
async def on_message(message):
    global coleted

    if (
        "ontem" in message.content.lower()
        and "hoje" in message.content.lower()
        and "bloqueio" in message.content.lower()
        and message.channel.id == 1000926747891601610
    ):
        if message.author.name not in coleted:
            splitted_message = [
                f"{i.split(':')[1]}" for i in message.content.split("\n")
            ]

            # ['Ontem: tal tal', 'Hoje: tal tal tal', 'Bloqueio: nao']
            line = f"| {names[message.author.name]} | {datetime.today().strftime('%d-%m-%Y')} | {splitted_message[0]} | {splitted_message[1]} | {splitted_message[2]} |"
            print(line)
            with open("table.md", "a") as f:
                f.write(line + "\n")

                coleted.append(message.author.name)

            await message.channel.send(f"Daily de {message.author} coletada!")
            await bot.process_commands(message)
        else:
            await message.channel.send(
                f"{message.author} sua daily já foi coletada hoje!"
            )


# get TOKEN from .env
bot.run(os.getenv("TOKEN"))
