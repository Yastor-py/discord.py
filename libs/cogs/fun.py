
from discord.ext.commands import Cog


class Fun(Cog):
    def __init__(self,bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
        await self.bot.stdout.send("Fun cog ready.")
        

def setup(bot):
    bot.add_cog(Fun(bot))
    