import discord
import time
import json
import asyncio
import datetime
import random
import os
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# client = discord.Client()
print(os.listdir())

bot = commands.Bot(command_prefix="?")
with open("resources.json", "r") as f:
    bot.config = json.load(f)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has been deployed.")


@tasks.loop(hours=24)
async def called_once_a_day():
    message_channel = bot.config["BotChannel"]["583864496964108288"]
    message_channel2 = bot.config["BotChannel"]["175184929611710465"]
    print(f"Got channel {message_channel}")
    await message_channel.send("Everyone do your Rubesty!")
    print(f"Got channel {message_channel2}")
    await message_channel2.send("Everyone do your Rubesty!")


@called_once_a_day.before_loop
async def before():
    now = datetime.now()
    secsleft = int(
        (timedelta(hours=24) - (now - now.replace(hour=12, minute=1, second=0,
                                                  microsecond=0))).total_seconds() % (
                    24 * 3600))
    await asyncio.sleep(secsleft)
    await bot.wait_until_ready()
    print("Finished waiting")


called_once_a_day.start()


def channel_check():
    async def pred(ctx):
        return ctx.message.channel.id == 659405687008264202 or \
               ctx.message.channel.id == 603809782742384652
    return commands.check(pred)


@bot.command(name="hello")
@channel_check()
async def hello(ctx):
    await ctx.send(f"H-H-Hello, {ctx.author.mention}.")


@bot.command(name="userinfo")
@channel_check()
async def userinfo(ctx, member: discord.Member = None):
    member = ctx.author if not member else member

    roles = [role for role in member.roles if role.name != "@everyone"]

    create_date = member.created_at.strftime("%a, %B %#d, %Y, %I:%M:%S %p UTC")
    join_date = member.joined_at.strftime("%a, %B %#d, %Y, %I:%M:%S %p UTC")
    values = []
    values.append(f"\n**ID Number**: {member.id}")
    values.append(f"\n**Display name**: {member.display_name}")
    values.append(f"\n**Created at**: {create_date}")
    values.append(f"\n**Joined at**: {join_date}")
    values.append(f"\n**Roles ({len(roles)})**: " + " ".join(
        [role.mention for role in roles]))
    values.append(f"\n**Bot?**: {member.bot}")

    embed = discord.Embed(colour=member.colour,
                          timestamp=ctx.message.created_at,
                          description=" ".join(values))
    embed.set_author(name=f"User Info - {member}", icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="rubyhelp")
@channel_check()
async def rubyhelp(ctx):
    embedded = discord.Embed(title="Help:", description="Useful commands")
    embedded.set_image(
        url="https://cdn.discordapp.com/emojis/496114760887042068.png?v=1")
    embedded.add_field(name="?hello", value="<:rubyHappy:496114760887042068>",
                       inline=True)
    embedded.add_field(name="CYaRon", value="We are CYaRon!", inline=True)
    embedded.add_field(name="Yay", value="Ruby-chan!", inline=True)
    embedded.add_field(name="?rubysay <message>",
                       value="Messages for Ruby to say", inline=True)
    embedded.add_field(name="Neso", value="Cuddle your nesos", inline=True)
    embedded.add_field(name="Hug", value="Hugs for everyone", inline=True)
    embedded.add_field(name="Tokyo", value="Ruby in Tokyo", inline=True)
    embedded.add_field(name="Ouin", value="Always paint", inline=True)
    embedded.add_field(name="Pigii", value="<:Rubyyy:615031254718611476>",
                       inline=True)
    embedded.add_field(name="Ganbaruby",
                       value="<a:ganbaonechan:660602824081670163>", inline=True)
    embedded.add_field(name="Headpat", value="Max comfort", inline=True)
    await ctx.send(content=None, embed=embedded)


@bot.event
async def on_member_join(member):
    """Bot Test Server: welcome channel ID, message
       Ganbaruby: ruby-chan-bot channel ID, message
       Casual Server: testing channel ID, message
    """
    welcome_ch_id = bot.config["WelcomeChannel"][str(member.guild.id)]
    welcome_msg = bot.config["WelcomeMsg"][str(member.guild.id)]
    await bot.get_channel(welcome_ch_id).send(
        welcome_msg.format(member.mention))
    print("Message sent")


@bot.command(name="rubysay")
@channel_check()
async def say(ctx, msg):
    content = ctx.message.content.replace("?rubysay ", "")
    await ctx.message.delete()
    ozo_list = ["Ozo is cute", "We love ozo", "Ozo is a good friend"]
    if "ozo" in content.lower():
        await ctx.send(random.choice(ozo_list))
    else:
        await ctx.send(content)


@bot.command(name="addrole")
@channel_check()
@commands.has_any_role("Mod", "Ganbaruby", "Wife")
async def add_role(ctx, *, role: discord.Role):
    member = ctx.author
    if role.name == "Ganbaruby":
        await ctx.send("Only Mods are allowed to assign this role.")
    else:
        await member.add_roles(role)
        embed = discord.Embed(colour=discord.Colour.magenta(),
                              description=f"Successfully gave {role.mention} to: `{member.display_name}`",
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


@add_role.error
async def add_role_error(ctx, error):
    tests = ["**Ensure that: **", "- You have the correct role: `Mod` or `Ganbaruby`",
             "- You typed in a valid role", "- You typed the command correctly: Format: `?addrole <@role_name>`"]
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description="\n".join(tests))
        await ctx.send(embed=embed)


@bot.command(name="removerole", aliases=["remove"])
@channel_check()
@commands.has_any_role("Mod", "Ganbaruby", "Wife")
async def remove_role(ctx, *, role: discord.Role):
    member = ctx.author
    await member.remove_roles(role)
    embed = discord.Embed(colour=discord.Colour.magenta(),
                          description=f"Successfully removed {role.mention} from: `{member.display_name}`",
                          timestamp=datetime.utcnow())
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@remove_role.error
async def remove_role_error(ctx, error):
    tests = ["**Ensure that: **", "- You have the correct role: `Mod` or `Ganbaruby`",
             "- You typed in a valid role", "- You typed the command correctly: Format: `?removerole <@role_name>`"]
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description="\n".join(tests))
        await ctx.send(embed=embed)


@bot.command(name="rolecolour", aliases=["rolecolor"])
@commands.has_permissions(manage_roles=True)
@channel_check()
@commands.has_any_role("Mod", "Wife")
async def role_colour(ctx, colour: discord.Colour, *, role: discord.Role):
    role_mention = role.mention

    await role.edit(color=colour)
    embed = discord.Embed(colour=discord.Colour.magenta(), description= f"Successfully changed the colour of {role_mention} to `{colour}`",
                          timestamp=datetime.utcnow())
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@role_colour.error
async def role_colour_error(ctx, error):
    tests = ["**Ensure that: **", "- You have the `Manage Roles` permission", "- You have the correct role: `Mod`",
             "- You typed in a valid role", "- You typed in a valid colour or hex value", "- You typed the command correctly: Format: `?rolecolor <colour> <@role_name>`"]
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description="\n".join(tests))
        await ctx.send(embed=embed)


@bot.command(name="createrole")
@commands.has_permissions(manage_roles=True)
@channel_check()
@commands.has_any_role("Mod", "Wife")
async def create_role(ctx, *, role_name: str):
    await ctx.guild.create_role(name=role_name)
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    embed = discord.Embed(colour=discord.Colour.magenta(),
                          description=f"Successfully created {role.mention}",
                          timestamp=datetime.utcnow())
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@create_role.error
async def create_role_error(ctx, error):
    tests = ["**Ensure that: **", "- You have the `Manage Roles` permission", "- You have the correct role: `Mod`",
             "- You typed the command correctly: Format: `?createrole <role_name>`"]
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description="\n".join(tests))
        await ctx.send(embed=embed)


@bot.command(name="deleterole")
@commands.has_permissions(manage_roles=True)
@channel_check()
@commands.has_any_role("Mod", "Fake Owner", "Wife")
async def delete_role(ctx, *, role: discord.Role):
    role_mention = role.mention
    embed = discord.Embed(colour=discord.Colour.magenta(),
                          description=f"Successfully deleted {role_mention}",
                          timestamp=datetime.utcnow())
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    await role.delete()


@delete_role.error
async def delete_role_error(ctx, error):
    tests = ["**Ensure that: **", "- You have the `Manage Roles` permission", "- You have the correct role: `Mod`",
             "- You typed in a valid role", "- You typed the command correctly: Format: `?deleterole <@role_name>`"]
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description="\n".join(tests))
        await ctx.send(embed=embed)


@bot.command(name="ozo")
@channel_check()
async def ozo(ctx):
    await ctx.send(random.choice(bot.config["ozo"]))


@bot.command(name="cheese")
@channel_check()
async def cheese(ctx):
    rand_e = "e" * random.randint(0, 21)
    await ctx.send(f"Chee{rand_e}se <:RubyYay:601615945848324136>")


@bot.command(name="fpop")
@channel_check()
async def fpop(ctx):
    await ctx.send(
        "Fpopopopop loves his KasuNeso <:RubyYay:601615945848324136>")


@bot.command(name="wooby")
@channel_check()
async def wooby(ctx):
    rand_o = "o" * random.randint(0, 21)
    await ctx.send(f"Woo{rand_o}by <:WoobyHappy:383422093779402752>")


@bot.command(name="ganbaruby")
@channel_check()
async def ganbaruby(ctx):
    await ctx.send("<a:ganbaonechan:660602824081670163>")
@bot.command(name="apop")
@channel_check()
async def apop(ctx):
    await ctx.send("Apop" + "op" * random.randint(0,
                                                  16) + " <:Rubyhappy:722075662235467876>")


@bot.event
async def on_message(message):
    # 1. Test Server bot channel
    # 2. Rubycord bot channel
    # 3. Testing channel
    channels = [583872784497770499, 659405687008264202, 603809782742384652]

    neso_list = ["<:HonokaNeso:661033812825997353>",
                 "<:KotoriNeso:661033813077524481>",
                 "<:UmiNeso:661033923102375986>",
                 "<:HanayoNeso:661033812683390978>",
                 "<:RinNeso:661033813933162536>",
                 "<:MakiNeso:661033813333377062>",
                 "<:EliNeso:661033545032007732>",
                 "<:NozomiNeso:661033813560000517>",
                 "<:NicoNeso:661033813585035314>",
                 "<:ChikaNeso:661033545157967872>",
                 "<:YouNeso:661033922863300619>",
                 "<:RikoNeso:661033813769453591>",
                 "<:RubyNeso:661033887971147796>",
                 "<:HanamaruNeso:661033812834123776>",
                 "<:YohaneNeso:661033922892791849>",
                 "<:DiaNeso:661033526107439105>",
                 "<:MariNeso:661033813127987210>",
                 "<:KananNeso:661033813245427732>",
                 "<:LeahNeso:661033813085913123>",
                 "<:SarahNeso:661033922993324043>",
                 "<:TsubasaNeso:666099332302372871>",
                 "<:AnjuNeso:666099347854721044>",
                 "<:ErenaNeso:666099306301882373>",
                 "<:RinaNeso:666112431176810496>"]

    yay_list = ["<:ChikaYay:610687363286433802>",
                "<:YouYay:610687363257073665>",
                "<:RikoYay:610687363663790080>",
                "<:RubyYay:601615945848324136>",
                "<:MaruYay:601616957321773112>",
                "<:YohaYay:600464932382834707>",
                "<:DiaYay:610687363106078722>", "<:MariYay:610687363647275008>",
                "<:KananYay:610687363378577418>",
                "<:SarahYay:666117368535187470>",
                "<:LeahYay:666117396511064085>"]

    if message.channel.id in channels and not message.author.bot:
        if message.content.find("ouin") != -1 or \
                message.content.find("<:RubyOuin:398246657323696138>") != -1 or \
                message.content.find("<:RubyCry:322038946533998613>") != -1 or \
                message.content.find("<:RubyCry2:528722509189742613>") != -1:
            await message.channel.send("<:Rubypaint2:660609765747064834>")
        elif message.content.lower().find("hug") != -1:
            await message.channel.send("<:Rubyhug:609517213514465360>")
        elif message.content.lower() == "pigii":
            await message.channel.send("<a:aRubyPigiii:424146355326550026>")
        elif message.content.lower().find("aquors") != -1:
            await message.channel.send("**AQOURS**")
        elif message.content.lower().find("neso") != -1:
            print("Emoji sent.")
            if message.content.lower().find("honoka neso") != -1:
                await message.add_reaction(neso_list[0])
            elif message.content.lower().find("kotori neso") != -1:
                await message.add_reaction(neso_list[1])
            elif message.content.lower().find("umi neso") != -1:
                await message.add_reaction(neso_list[2])
            elif message.content.lower().find("hanayo neso") != -1:
                await message.add_reaction(neso_list[3])
            elif message.content.lower().find("rin neso") != -1:
                await message.add_reaction(neso_list[4])
            elif message.content.lower().find("maki neso") != -1:
                await message.add_reaction(neso_list[5])
            elif message.content.lower().find("eli neso") != -1:
                await message.add_reaction(neso_list[6])
            elif message.content.lower().find("nozomi neso") != -1:
                await message.add_reaction(neso_list[7])
            elif message.content.lower().find("nico neso") != -1:
                await message.add_reaction(neso_list[8])
            elif message.content.lower().find("chika neso") != -1:
                await message.add_reaction(neso_list[9])
            elif message.content.lower().find("you neso") != -1:
                await message.add_reaction(neso_list[10])
            elif message.content.lower().find("riko neso") != -1:
                await message.add_reaction(neso_list[11])
            elif message.content.lower().find("ruby neso") != -1:
                await message.add_reaction(neso_list[12])
            elif message.content.lower().find("hanamaru neso") != -1:
                await message.add_reaction(neso_list[13])
            elif message.content.lower().find("yohane neso") != -1:
                await message.add_reaction(neso_list[14])
            elif message.content.lower().find("dia neso") != -1:
                await message.add_reaction(neso_list[15])
            elif message.content.lower().find("mari neso") != -1:
                await message.add_reaction(neso_list[16])
            elif message.content.lower().find("kanan neso") != -1:
                await message.add_reaction(neso_list[17])
            elif message.content.lower().find("leah neso") != -1:
                await message.add_reaction(neso_list[18])
            elif message.content.lower().find("sarah neso") != -1:
                await message.add_reaction(neso_list[19])
            elif message.content.lower().find("tsubasa neso") != -1:
                await message.add_reaction(neso_list[20])
            elif message.content.lower().find("anju neso") != -1:
                await message.add_reaction(neso_list[21])
            elif message.content.lower().find("erena neso") != -1:
                await message.add_reaction(neso_list[22])
            elif message.content.lower().find("rina neso") != -1 or \
                    message.content.lower().find("rinaneso") != -1:
                await message.add_reaction(neso_list[23])
            else:
                await message.add_reaction(random.choice(neso_list))
        elif message.content.lower() == "yay":
            await message.channel.send(yay_list[3])
        elif message.content.lower().find("tokyo") != -1:
            await message.channel.send("<a:RubyTokyo:548351194859307023>")
        elif message.content.lower() == "bongo":
            await message.channel.send("<a:bongoruby:600470496211107840>")
        elif message.content.lower() == "cyaron":
            await message.channel.send("We are CYaRon!")
            await message.channel.send(yay_list[0] + yay_list[1] + yay_list[3])
        elif message.content.lower() == "azalea":
            await message.channel.send("AZALEA")
            await message.channel.send(yay_list[8] + yay_list[6] + yay_list[4])
        elif message.content.lower() == "guilty kiss":
            await message.channel.send("Guilty Kiss!")
            await message.channel.send(yay_list[2] + yay_list[5] + yay_list[7])
        elif message.content.lower() == "cyazalea kiss":
            await message.channel.send(yay_list[0] + yay_list[1] + yay_list[3]
                                       + yay_list[8] + yay_list[6] + yay_list[4]
                                       + yay_list[2] + yay_list[5] + yay_list[
                                           7])
        elif message.content.lower().find("saint snow") != -1:
            await message.channel.send(yay_list[9] + yay_list[10])
        elif message.content.find("<:RubyBait:399719408248946688>") != -1:
            rand = random.randint(0, 1)
            if rand == 0:
                await message.add_reaction("<:DiaNo:660685644472909836>")
            else:
                await message.add_reaction("<:RubyDeviant:443170127093956634>")
        elif message.content.lower() == "headpat":
            await message.channel.send("<a:RubyHeadpat:460504693714452480>")
        elif message.content.lower().find("kurosawa") != -1:
            await message.channel.send(yay_list[6] + yay_list[3])
        elif message.content.lower() == "aquarium ruby":
            await message.channel.send(file=discord.File("./images/Aquarium Ruby.gif"))
        elif message.content.lower() == "aquarium maru":
            await message.channel.send(file=discord.File("./images/Aquarium Maru.gif"))
        elif message.content.lower() == "aquarium yohane":
            await message.channel.send(file=discord.File("./images/Aquarium Yoha.gif"))
        elif message.content.lower() == "i love ruby":
            print("Emoji sent.")
            await message.add_reaction("<:rubyLove:545429905001807893>")

    await bot.process_commands(message)


file_object = open("ruby-key.txt", "r")
bot.run(file_object.read().strip())
