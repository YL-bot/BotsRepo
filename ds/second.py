import asyncio
import discord
from discord.ext import commands
import logging


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class TimerBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set_timer', past_context=True)
    async def set_timer(self, ctx, *msg):
        s = m = h = 0
        
        if len(msg) == 1 and msg[0].isdigit():
            s = int(msg[0])
            
        else:
            if "hours" in msg:
                h = int(msg[msg.index("hours") - 1])
                if "minutes" in msg:
                    m = int(msg[msg.index("minutes") - 1])
                    if "seconds" in msg:
                        s = int(msg[msg.index("seconds") - 1])
        try:
            time = s + m * 60 + h * 3600
            if time < 0:
                await ctx.send('Value must be positive number')
            else:
                message = await ctx.send(time)
                while time:
                    time -= 1
                    await message.edit(content=time)
                    await asyncio.sleep(0.95)
                await message.edit(content='Time X! MOMI IS COMING TO BEAT UR A.....')

        except ValueError:
            await ctx.send("set a timer with command with !set_timer (X) hours (y) minutes (z) seconds ")
            await ctx.send('Time must be a number')


bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = "MTEwMDg2ODIyMjg1ODgyMTY4Mw.GxrMnx.8B0ANmn8FLOSpZK0DHAB-7GVjAHkftcfjtDPi0"


async def main():
    await bot.add_cog(TimerBot(bot))
    await bot.start(TOKEN)


asyncio.run(main())