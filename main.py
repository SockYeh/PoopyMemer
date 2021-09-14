import json
import discord, requests, urllib.parse
from discord.ext import commands


def get_prefix(bot, message):
    with open("guilds.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(get_prefix, case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("bot is online!")
    await bot.change_presence(
        activity=discord.activity.Game(f"pm Help in {len(bot.guilds)} guilds.")
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("Command not found!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("You dont have permissions to use this command!")


@bot.event
async def on_guild_join(guild):
    with open("guilds.json", "r+") as f:
        data = json.load(f)
    guild_id = guild.id
    data[guild_id] = "pm "
    with open("guilds.json", "w") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("guilds.json", "r+") as f:
        data = json.load(f)
    guild_id = guild.id
    data.pop(guild_id)
    with open("guilds.json", "w") as f:
        json.dump(data, f, indent=4)


@bot.command()
async def meme(ctx):
    r = requests.get("https://some-random-api.ml/meme")
    data = r.json()
    cate = data["category"]
    e = discord.Embed(
        title=f"{cate} Meme!", description=data["caption"], color=0xFFA500
    )
    e.set_image(url=data["image"])
    await ctx.channel.send(embed=e)


@bot.command()
async def joke(ctx):
    r = requests.get("https://some-random-api.ml/joke")
    await ctx.channel.send(r.json()["joke"])


@bot.command()
async def animal(ctx, animal):
    animal = animal.lower().strip()
    animals = [
        "dog",
        "cat",
        "panda",
        "fox",
        "redpanda",
        "koala",
        "bird",
        "raccoon",
        "kangaroo",
    ]
    if animal in animals:
        if animal == "bird":
            animal = "birb"
        r = requests.get(f"https://some-random-api.ml/animal/{animal}")
        animal = animal.upper()
        fact = r.json()["fact"]
        img = r.json()["image"]
        e = discord.Embed(title=f"{animal} FACT!", description=fact)
        e.set_image(url=img)
        await ctx.channel.send(embed=e)
    else:
        await ctx.channel.send(
            "Not a valid animal type! The supported animals are: **Dog** | **Cat** | **Panda** | **Fox** | **RedPanda** | **Bird** | **Raccoon** | **Kangaroo**"
        )


@bot.command()
async def chat(ctx, *, message):
    message = urllib.parse.quote_plus(message)
    r = requests.get(
        f"https://some-random-api.ml/chatbot?message={message}&key=URL_API_KEY"
    )
    resp = r.json()["response"]
    await ctx.channel.send(resp)


@bot.command()
async def pokemon(ctx, *, pokemon):
    pokemon = pokemon.lower().strip()
    pokemon = urllib.parse.quote_plus(pokemon)
    r = requests.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon}")
    data = r.json()
    if "error" in data:
        err = data["error"]
        await ctx.channel.send(err)
        return
    e = discord.Embed(title=pokemon.upper().strip(), description="", color=0xFFA500)

    for item in data:

        if (
            item == "type"
            or item == "species"
            or item == "abilities"
            or item == "gender"
            or item == "egg_groups"
        ):
            for ite in data[item]:
                datt = ""
                datt += ite + " "
            e.add_field(name=item.upper(), value=datt)
        if item == "family":
            for ite in data[item]["evolutionLine"]:
                datt = ""
                datt += ite + " "
            e.add_field(name=item.upper(), value=datt)
        if item == "sprites":
            datt = data[item]["normal"]
            e.set_image(url=datt)
        if item == "stats":
            datt = ""
            for datee in data["stats"]:
                e.add_field(name=datee.upper(), value=data["stats"][datee])
    await ctx.channel.send(embed=e)


@bot.command()
async def help(ctx):
    e = discord.Embed(title="Commands", description="", color=0xFFA500)
    e.add_field(
        name="Pokemon (pokemon)",
        value="Gives information on given pokemon.",
        inline=False,
    )
    e.add_field(name="Chat (message)", value="Talks to you.", inline=False)
    e.add_field(
        name="Animal (animal)", value="Gives fact and image on animal.", inline=False
    )
    e.add_field(name="Joke", value="Sends a random joke.", inline=False)
    e.add_field(name="Meme", value="Sends a random meme.", inline=False)
    e.add_field(
        name="Change_Prefix (prefix)",
        value="Changes guild prefix to given prefix.",
        inline=False,
    )
    e.add_field(
        name="Reset_Prefix", value="Changes guild prefix back to `pm `.", inline=False
    )
    e.add_field(
        name="RickRoll (user)",
        value="Sends rickroll lyrics to given user.",
        inline=False,
    )

    await ctx.channel.send(embed=e)


@bot.command()
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, *, prefix):
    with open("guilds.json", "r+") as f:
        data = json.load(f)
    guild_id = ctx.guild.id
    data[str(guild_id)] = prefix
    with open("guilds.json", "w") as f:
        json.dump(data, f, indent=4)
    await ctx.channel.send(f"Changed Guild Prefix to `{prefix}`")


@bot.command()
@commands.has_permissions(administrator=True)
async def reset_prefix(ctx):
    with open("guilds.json", "r+") as f:
        data = json.load(f)
    guild_id = ctx.guild.id
    data[str(guild_id)] = "pm "
    with open("guilds.json", "w") as f:
        json.dump(data, f, indent=4)
    await ctx.channel.send(f"Changed Guild Prefix to `pm `")


@bot.command()
async def rickroll(ctx, user: discord.User):
    await user.send(
        "We're no strangers to love\nYou know the rules and so do I\nA full commitment's what I'm thinking of\nYou wouldn't get this from any other guy\nI just wanna tell you how I'm feeling\nGotta make you understand\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nWe've known each other for so long\nYour heart's been aching, but you're too shy to say it\nInside, we both know what's been going on\nWe know the game, and we're gonna play itAnd if you ask me how I'm feeling\nDon't tell me you're too blind to see\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nOoh (Give you up)\nOoh-ooh (Give you up)\nOoh-ooh\nNever gonna give, never gonna give (Give you up)\nOoh-ooh\nNever gonna give, never gonna give (Give you up)We've known each other for so long\nYour heart's been aching, but you're too shy to say it\nInside, we both know what's been going on\nWe know the game, and we're gonna play it\nI just wanna tell you how I'm feeling\nGotta make you understand\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you"
    )
    await ctx.channel.send(f"Sent rickroll to {user.name}")


@bot.command()
async def invite(ctx):
    e = discord.Embed(
        title="Invite Me!",
        description=f"You can invite me to ur server [here](INVITE_URL).",
        color=0xFFA500,
    )
    await ctx.channel.send(embed=e)


bot.run("BOT_TOKEN")
