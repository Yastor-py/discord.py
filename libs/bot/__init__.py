from datetime import datetime
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents


PREFIX = "<>"
OWNER_IDS = [279958685378150400]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX, owner_ids= OWNER_IDS, Intents = Intents.all())

    def run(self, version):
        self.VERSION = version

        with open("./libs/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot version {}...".format(self.VERSION))
        super().run(self.TOKEN, reconnect = True)
    
    async def on_connect(self):
        print("Bot connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print("Bot ready")

            print("\nList of the servers where the bot is: \n")
            for guild in bot.guilds: #on what servers bot is
                print(guild.name)

            self.guild = bot.guilds[1] #get guild of the 2nd server 

            channel = self.get_channel(852961240350457866)
            await channel.send("Now online!")

            embed = Embed(title="Now online!", description="Oiw is now online!", color=0xCC0000, timestamp=datetime.utcnow())
            fields = [("Name", "Value", True),
            ("Another field", "Next to other one", True),
            ("A non-inline field", "This field will appear on ti's own row.", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_author(name="Oiw02", icon_url=self.guild.icon_url)
            embed.set_footer(text="Oiw!")
            embed.set_thumbnail(url=bot.guilds[0].icon_url)
            embed.set_image(url=bot.guilds[0].icon_url)

            await channel.send(embed=embed)
            #await channel.send(file=File("./data/images/czapa.png"))
            

            



        else:
            print("Bot reconnected")


    async def on_message(self, message):
        pass

bot = Bot()
    
        