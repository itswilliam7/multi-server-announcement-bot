from CopperUI import *
from ext.config import *
import interactions

token = open("token.txt").readline()
bot = interactions.Client(token=token, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

@bot.event
async def on_ready():
    """what to do when the bot starts up (happens upon API refresh too)"""
    print(""" 
              ____   ___  _ __     _______   ____   ___ _____
             / ___| / _ \| |\ \   / / ____| | __ ) / _ \_   _|
             \___ \| | | | | \ \ / /|  _|   |  _ \| | | || |
              ___) | |_| | |__\ V / | |___  | |_) | |_| || |
             |____/ \___/|_____\_/  |_____| |____/ \___/ |_|

             made with ❤️  by Morgandri1
            """)
    for guild in bot.guilds:
        server_data[guild.id] = load(guild)

@bot.event
async def on_guild_join(ctx):
    """what to do when the bot joins a guild"""
    await ctx.get_guild()
    server_data[int(ctx.guild.id)] = DefData
    save()

@bot.command(
    name="redeem",
    description="redeem your license key",
    default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    options=[
        interactions.Option(
            name="type",
            description="the type of license key you want to redeem",
            type=interactions.OptionType.STRING,
            required=True,
            choices=[
                interactions.Choice(name="Alpha Calls", value="alpha"),
                interactions.Choice(name="Crypto News", value="crypto"),
            ]
        ),
        interactions.Option(
            name="key",
            description="your license key you want to redeem",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def redeem(ctx, type, key):
    """redeem your license key"""
    keylist = keys()
    if type == "alpha":
        await ctx.send("Redeeming Alpha Calls...")
        if key in keylist["alpha"] and keylist["alpha"][key] == "unused":
            keylist["alpha"][key] = "used"
            update()
            server_data[int(ctx.guild.id)]["license"] = "alpha"
            server_data[int(ctx.guild.id)]["key"] = key
            save()
            await ctx.send("activated! welcome to the network!")
        elif key in keylist["alpha"] and keylist["alpha"][key] == "used":
            await ctx.send("already used! try again")
        elif key not in keylist["alpha"]:
            await ctx.send("invalid key! *did you try to redeem a crypto news key?*")
    elif type == "crypto":
        await ctx.send("Redeeming Crypto News...")
        if key in keylist["alpha"] and keylist["alpha"][key] == "unused":
            keylist["alpha"][key] = "used"
            update()
            server_data[int(ctx.guild.id)]["license"] = "alpha"
            server_data[int(ctx.guild.id)]["key"] = key
            save()
            await ctx.send("activated! welcome to the network!")
        if key in keylist["alpha"] and keylist["alpha"][key] == "used":
            await ctx.send("already used! try again")
        if key not in keylist["alpha"]:
            await ctx.send("invalid key! *did you try to redeem a crypto news key?*")

@bot.command(
    name="subscribe",
    description="subscribe to the S◎Lve network",
    default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    options=[
        interactions.Option(
            name="channel",
            description="the channel to send the S◎Lve feed to",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ]
)
async def subscribe(ctx, channel: str()):
    """subscribe to the S◎Lve network"""
    channel = int(channel.removeprefix("<#").removesuffix(">"))
    await ctx.send(f"subscription set to <#{channel}>")
    await ctx.get_guild()
    print(channel)
    server_data[int(ctx.guild.id)]['channel'] = "123"
    server_data[int(ctx.guild.id)]['subscribed'] = "True"
    print(server_data)
    save()

@bot.command(
    name="call",
    description="call a message to the subscribers",
    default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    options=[
                interactions.Option(
                    name="type",
                    description="which type of announcement to make?",
                    type=interactions.OptionType.STRING,
                    required=True,
                    choices=[
                        interactions.Choice(name="Alpha call", value="AC"), 
                        interactions.Choice(name="Crypto news", value="CN")
                    ],
                ),
    ]
)
async def call(ctx):
    """announce a message to the subscribers"""
    modal = interactions.Modal(
        title="Announcement",
        custom_id="announcement_form",
        components=[
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                custom_id="message_title",
                label="Announcement title",
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.PARAGRAPH,
                custom_id="message_body",
                label="Announcement Body",
            ),
        ],
    )
    await ctx.popup(modal)

@bot.modal("announcement_form")
async def modal_response(ctx, title: str, body: str):
    embed = interactions.Embed(title=title, description=f"{body}\na message from the S◎Lve network", color=0x00ff00)
    await ctx.send("your message:", ephemeral=True, embed=embed)
    for guild in bot.guilds:
        await ctx.get_guild()
        print(guild.id)
        if str(guild.id) in server_data:
            if server_data[str(guild.id)]["subscribed"] == True:
                channel = await interactions.get(bot, interactions.Channel, object_id=server_data[str(guild.id)]["channel"])
                await channel.send(embeds=embed)

bot.start()