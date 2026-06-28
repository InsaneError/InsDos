from telethon import events
from asyncio import sleep, create_task
from .. import loader, utils

@loader.tds
class SmertBotov(loader.Module):
    """Убийца ботов от @InsModule"""
    strings = {'name': 'smertbotov'}

    async def worker(self, message, count):
        for _ in range(count):
            sent = await message.reply("<b>/start</b>")
            await sent.delete()

    @loader.command()
    async def ins(self, message):
        """[кол-во >10]"""
        try:
            count = int(utils.get_args_raw(message))
            if count <= (-1): return
        except: return

        await message.delete()
        workers = [create_task(self.worker(message, count//10)) for _ in range(10)]
        [await t for t in workers]
