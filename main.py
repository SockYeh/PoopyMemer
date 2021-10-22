import json, random
import discord, requests, urllib.parse
from discord.ext import commands

TOKEN = ""
API_URL_KEY = ""


def get_prefix(bot, message):
    try:
        with open("guilds.json", "r") as f:
            prefixes = json.load(f)

        return ["pm ", prefixes[str(message.guild.id)]]
    except:
        return "pm "


bot = commands.Bot(get_prefix, case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("bot is online!")
    await bot.change_presence(
        activity=discord.activity.Game(f"pm Help in {len(bot.guilds)} guilds.")
    )
    for guild in bot.guilds:
        if guild.id != 773030062425374720:
            await bot.get_guild(guild.id).leave()
            print(f"left {guild}")


@bot.event
async def on_message(ctx):
    mentions = [str(m) for m in ctx.mentions]
    if str(bot.user) in list(mentions):
        prefix = get_prefix(bot, ctx)
        pprefix = "` | `".join(prefix)
        await ctx.channel.send(f"My prefix for this guild is **`{pprefix}`**")
    await bot.process_commands(ctx)


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
    data.pop(str(guild_id))
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
    e.set_footer(
        text=f"Command Invoked by {ctx.author} | Bot made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
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
        e = discord.Embed(title=f"{animal} FACT!", description=fact, color=0xFFA500)
        e.set_footer(
            text=f"Command Invoked by {ctx.author} | Bot made by SockYeh#0001",
            icon_url=ctx.author.avatar_url,
        )
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
        f"https://some-random-api.ml/chatbot?message={message}&key={API_URL_KEY}"
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
    e.set_footer(
        text=f"Command Invoked by {ctx.author} | Bot made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    for item in data:

        if (
            item == "type"
            or item == "species"
            or item == "abilities"
            or item == "gender"
            or item == "egg_groups"
        ):
            datt = ", ".join(data[item])
            e.add_field(name=item.upper(), value=datt)
        if item == "family":
            datt = ", ".join(data[item]["evolutionLine"])
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
        name="General",
        value="Help **|** Ping **|** Avatar [user] ",
        inline=False,
    )
    e.add_field(name="Moderation", value="Mute (user) [reason] **|** Unmute (user)")
    e.add_field(
        name="Fun",
        value="Pokemon (pokemon) **|** Chat (message) **|** Joke **|** Meme **|** Rickroll (user) **|** Inspire **|** Animal (animal)",
        inline=False,
    )
    e.add_field(
        name="Economy",
        value="Balance [user] **|** Daily **|** Work **|** Rob **|** Give (user) (amount) **|** CoinFlip (amount) **|** Leaderboard",
        inline=False,
    )
    e.add_field(
        name="Settings",
        value="Change_Prefix (prefix) **|** Reset_Prefix",
        inline=False,
    )
    e.set_footer(
        text=f"Command Invoked by {ctx.author} | Bot made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
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
    if user.id == 844244515933913149:
        user = ctx.author
    await user.send(
        "We're no strangers to love\nYou know the rules and so do I\nA full commitment's what I'm thinking of\nYou wouldn't get this from any other guy\nI just wanna tell you how I'm feeling\nGotta make you understand\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nWe've known each other for so long\nYour heart's been aching, but you're too shy to say it\nInside, we both know what's been going on\nWe know the game, and we're gonna play itAnd if you ask me how I'm feeling\nDon't tell me you're too blind to see\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nOoh (Give you up)\nOoh-ooh (Give you up)\nOoh-ooh\nNever gonna give, never gonna give (Give you up)\nOoh-ooh\nNever gonna give, never gonna give (Give you up)We've known each other for so long\nYour heart's been aching, but you're too shy to say it\nInside, we both know what's been going on\nWe know the game, and we're gonna play it\nI just wanna tell you how I'm feeling\nGotta make you understand\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you"
    )
    await ctx.channel.send(f"Sent rickroll to {user.name}")


@bot.command()
async def inspire(ctx):
    r = requests.get("https://zenquotes.io/api/random")
    quote = r.json()[0]["q"]
    quoter = r.json()[0]["a"]
    await ctx.channel.send(f'"{quote}" - {quoter}')


@bot.command()
async def avatar(ctx, user: discord.User = None):
    if user != None:
        ava_url = user.avatar_url
        usr_name = f"{user.name}#{user.discriminator}"
    else:
        ava_url = ctx.author.avatar_url
        usr_name = f"{ctx.author.name}#{ctx.author.discriminator}"
    e = discord.Embed(title=f"{usr_name}'s Avatar", description="", color=0xFFA500)
    e.set_footer(
        text=f"Command Invoked by {ctx.author} | Bot made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
    e.set_image(url=ava_url)
    await ctx.channel.send(embed=e)


@bot.command()
async def ping(ctx):
    await ctx.channel.send(f"Pong! My Latency/Ping is {round(bot.latency*1000)}ms")


@bot.command()
async def balance(ctx, user: discord.User = None):
    if user != None:
        userid = user.id
    else:
        userid = ctx.author.id
    with open("users.json", "r+") as f:
        data = json.load(f)
    if str(userid) in data:
        balance = data[str(userid)]["balance"]
        await ctx.channel.send(
            f"{ctx.author.mention} has **${balance}** in their wallet."
        )
    else:
        data[str(userid)] = {"balance": 0}
        await ctx.channel.send(
            f"Wallet created for {ctx.author.mention}. They now have **$0**."
        )
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)


@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    userid = ctx.author.id
    with open("users.json", "r+") as f:
        data = json.load(f)
    if str(userid) not in data:
        data[str(userid)] = {"balance": 0}
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)

    data[str(userid)]["balance"] += 1000
    c_bal = data[str(userid)]["balance"]
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)
    await ctx.channel.send(
        f"Added **$1000** to your wallet! Your current balance is **${c_bal}**"
    )


@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f"You can only use this command once every 24 hours!")


@bot.command()
@commands.cooldown(1, 3000, commands.BucketType.user)
async def work(ctx):
    amt = random.randint(200, 500)
    userid = ctx.author.id
    with open("users.json", "r+") as f:
        data = json.load(f)
    if str(userid) not in data:
        data[str(userid)] = {"balance": 0}
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)

    data[str(userid)]["balance"] += amt
    c_bal = data[str(userid)]["balance"]
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)
    await ctx.channel.send(
        f"You worked for **${amt}** and they have been added to your wallet! Your current balance is **${c_bal}**"
    )


@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f"You can only use this command once every 5 minutes!")


@bot.command()
@commands.cooldown(1, 3000, commands.BucketType.user)
async def rob(ctx):
    amt = random.randint(200, 500)
    p_m = random.choice([1, 2])
    if p_m == 1:
        userid = ctx.author.id
        with open("users.json", "r+") as f:
            data = json.load(f)
        if str(userid) not in data:
            data[str(userid)] = {"balance": 0}
            with open("users.json", "w") as f:
                json.dump(data, f, indent=4)

        data[str(userid)]["balance"] += amt
        c_bal = data[str(userid)]["balance"]
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)
        await ctx.channel.send(
            f"You robbed someone successfully for **${amt}** and they have been added to your wallet! Your current balance is **${c_bal}**"
        )
    if p_m == 2:
        userid = ctx.author.id
        with open("users.json", "r+") as f:
            data = json.load(f)
        if str(userid) not in data:
            data[str(userid)] = {"balance": 0}
            with open("users.json", "w") as f:
                json.dump(data, f, indent=4)

        data[str(userid)]["balance"] -= amt
        c_bal = data[str(userid)]["balance"]
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)
        await ctx.channel.send(
            f"You robbed someone unsuccessfully and lost **${amt}**. Your current balance is **${c_bal}**"
        )


@rob.error
async def rob_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f"You can only use this command once every 5 minutes!")


@bot.command()
async def give(ctx, user: discord.User = None, amt: int = None):
    if user == None:
        await ctx.channel.send("Please specify a user to give money to!")
        return
    if user.bot:
        await ctx.channel.send("Cant send money to a bot!")
        return
    elif amt == None:
        await ctx.channel.send("Please specify the amount to be given to the user!")
        return

    g_userid = user.id
    c_userid = ctx.author.id
    with open("users.json", "r+") as f:
        data = json.load(f)
    if str(c_userid) not in data:
        data[str(c_userid)] = {"balance": 0}
    if data[str(c_userid)]["balance"] >= amt:
        data[str(c_userid)]["balance"] -= amt

        if str(g_userid) not in data:
            data[str(g_userid)] = {"balance": 0}

        data[str(g_userid)]["balance"] += amt
        c_bal = data[str(c_userid)]["balance"]
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)
        await ctx.channel.send(
            f"You sent **${amt}** to {user.mention}. Your current balance is **${c_bal}**."
        )
    else:
        await ctx.channel.send("You are broke. You cant send the user that amount!")


@bot.command()
async def coinflip(ctx, amt: int = None):
    if amt == None:
        await ctx.channel.send("Please specify the amount!")
        return
    userid = ctx.author.id
    with open("users.json", "r+") as f:
        data = json.load(f)
    chc = random.choice(["-", "+"])
    if data[str(userid)]["balance"] >= amt:
        if chc == "-":
            data[str(userid)]["balance"] -= amt
            c_bal = data[str(userid)]["balance"]
            await ctx.channel.send(
                f"You lost **${amt}** while coin fliping. Your current balance is **${c_bal}**. "
            )
        elif chc == "+":
            data[str(userid)]["balance"] += amt
            c_bal = data[str(userid)]["balance"]
            await ctx.channel.send(
                f"You won **${amt}** while coin fliping! Your current balance is **${c_bal}**. "
            )
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        await ctx.channel.send("You are broke. You cant coinflip that amount!")


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def suggest(ctx, *, args=None):
    if args == None:
        await ctx.channel.send("Please specify your suggestion!")
        return
    chl = await bot.fetch_channel(869120280247820318)  # 869120280247820318
    e = discord.Embed(
        title=f"Suggestion by {ctx.author}", description=args, color=0xFFA500
    )
    msg = await chl.send(embed=e)
    await msg.add_reaction("✅")
    await msg.add_reaction("❎")
    await ctx.channel.send(f'Sent suggestion "{args}" in {chl.mention}!')


@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send("You can only use this command once every 30 seconds!")


@bot.command()
@commands.has_role(773035668132855838)
async def mute(ctx, user: discord.User = None, *, reason=None):
    if user == None:
        await ctx.channel.send("Please mention the user you want to mute!")
        return
    try:
        await user.add_roles(
            discord.utils.get(
                ctx.guild.roles, name="------------Muted >:D-------------"
            )
        )
        await ctx.channel.send(f"Muted {user.mention} Successfully. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"There was an error running this command " + str(e))


@bot.command()
@commands.has_role(773035668132855838)
async def unmute(ctx, user: discord.User = None):
    if user == None:
        await ctx.channel.send("Please mention the user you want to unmute!")
        return
    try:
        await user.remove_roles(
            discord.utils.get(
                ctx.guild.roles, name="------------Muted >:D-------------"
            )
        )
        await ctx.channel.send(f"Unmuted {user.mention} Successfully.")
    except Exception as e:
        await ctx.send(f"There was an error running this command " + str(e))


@bot.command()
async def leaderboard(ctx):
    try:
        e = discord.Embed(title="Economy Leaderboard", description="", color=0xFFA500)
        with open("users.json", "r+") as f:
            data = json.load(f)
        allurs = []

        for item in data:
            allurs.append((item, data[item]["balance"]))
        allurs.sort(key=lambda allurs: allurs[1], reverse=True)
        index = 0
        for id_, bal in allurs:
            if index == 10:
                break
            index += 1
            user = await bot.fetch_user(id_)

            e.description += f"**{index}**. {user.mention} - ${bal}\n"
        e.set_footer(
            text=f"Command Invoked by {ctx.author} | Bot made by SockYeh#0001",
            icon_url=ctx.author.avatar_url,
        )
        await ctx.channel.send(embed=e)
    except Exception as e:
        await ctx.channel.send(str(e))


bot.run(TOKEN)
