from datetime import datetime
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord.ext.commands import CommandNotFound
from ..db import db
from apscheduler.triggers.cron import CronTrigger
from glob import glob
from asyncio import sleep
import tzlocal

PREFIX = "<>"
OWNER_IDS = [279958685378150400]
COGS = [path.split("\\")[-1][:-3] for path in glob("./libs/cogs/*.py")]



class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)


    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")


    def all_ready(self):
        return all([getattr(self,cog) for cog in COGS])
        


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids= OWNER_IDS, Intents = Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"libs.cogs.{cog}")
            print(f"cog {cog} loaded")
        print("setup complete")


    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./libs/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot version {}...".format(self.VERSION))
        super().run(self.TOKEN, reconnect=True)


    async def print_message(self):
        channel = self.get_channel(852961240350457866)
        await channel.send("Time")
    

    async def on_connect(self):
        print("Bot connected")


    async def on_disconnect(self):
        print("Bot disconnected")


    async def on_error(self, err, *args, **kwargs):
        channel = self.get_channel(852961240350457866)
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
        
        await channel.send("Error.")
        raise


    async def on_command_error(self, ctx, exc):
        print(exc)
        if isinstance(exc, CommandNotFound):
            await ctx.send("Wrong command")
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc
        

    async def on_ready(self):
        if not self.ready:            
            self.scheduler.start()
            #self.scheduler.add_job(self.print_message, 'interval', seconds=5) #print message every 15s CronTrigger(second="0,15,30,45")
            self.stdout = self.get_channel(852961240350457866)
            while not self.cogs_ready.all_ready():
                #print("waiting...")
                await sleep(0.5)

            self.ready = True
            print("Bot ready")
            # print("\nList of the servers where the bot is: \n")
            # for guild in bot.guilds: #on what servers bot is
            #     print(guild.name)
            self.guild = bot.guilds[1] #get guild of the 2nd server 
            await self.stdout.send("Now online!")
            # embed = Embed(title="Now online!", description="Oiw is now online!", color=0xCC0000, timestamp=datetime.utcnow())
            # fields = [("Name", "Value", True),
            # ("Another field", "Next to other one", True),
            # ("A non-inline field", "This field will appear on ti's own row.", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)

            # embed.set_author(name="Oiw02", icon_url=self.guild.icon_url)
            # embed.set_footer(text="Oiw!")
            # embed.set_thumbnail(url=bot.guilds[0].icon_url)
            # embed.set_image(url=bot.guilds[0].icon_url)
            # await channel.send(embed=embed)
            #await channel.send(file=File("./data/images/czapa.png"))
            
        else:
            print("Bot reconnected")


    async def on_message(self, message):
        pass

bot = Bot()
    
        