import os
import asyncio
import threading
from aiohttp import web
from telethon import TelegramClient, events
from google import genai
from google.genai import types
import random

API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = TelegramClient('my_personal_session', API_ID, API_HASH)

processed_messages = set()

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_msg(event):
    msg_id = event.id
    if msg_id in processed_messages:
        return
    processed_messages.add(msg_id)
    if len(processed_messages) > 100:
        processed_messages.clear()

    sender = await event.get_sender()
    if sender and sender.bot:
        return

    msg = event.raw_text
    if not msg:
        return

    sender_name = sender.first_name if sender else "مستخدم مجهول"
    sender_username = f"@{sender.username}" if sender and sender.username else "لا يوجد معرف"
    
    print(f"📩 رسالة العميل من ({sender_name}): {msg}")

    prompt = f"""
أنت مساعد شخصي ذكي للمهندس محمد ضهير (مبرمج ومطور تطبيقات Flutter). 
الرجاء الرد على رسالة العميل التالية بأسلوب بشري متجدد، قصير (سطر أو سطرين)، ومباشر جداً بدون أي تكرار أو جمود:
"{msg}"
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9,
                max_output_tokens=100,
            )
        )
        reply = response.text.strip() if response and response.text else None
    except Exception as e:
        print(f"AI Error: {e}")
        reply = None

    if not reply:
        fallbacks = [
            f"أهلاً بك يا غالي ♠️. وصلني سؤالك عن ({msg}) وسيتم إبلاغ المهندس محمد ضهير فوراً 💎.",
            f"تحية طيبة ⚡. تم تسجيل طلبك بخصوص '{msg}' وإرساله مباشرة للمهندس محمد.",
            "أهلاً بك ♠️. تفضل بتوضيح التفاصيل أكثر وسأقوم بعرضها على طاولة المهندس محمد فوراً 💎."
        ]
        reply = random.choice(fallbacks)

    print(f"✨ رد البوت المتجدد: {reply}")
    
    await event.reply(reply)

    try:
        notification_text = f"""
🚨 **تنبيه رسالة جديدة يا مهندس محمد!** ♠️

👤 **المرسل:** {sender_name} ({sender_username})
💬 **الرسالة:** 
> {msg}

🤖 **رد البوت:** 
> {reply}
        """
        await bot.send_message('me', notification_text)
    except Exception as e:
        print(f"⚠️ خطأ في الإشعار: {e}")

# تعريف تطبيق aiohttp ليعمل بانسجام تام مع Gunicorn
routes = web.RouteTableDef()

@routes.get("/")
async def handle_web(request):
    return web.Response(text="Bot is running smoothly 24/7!", status=200)

@routes.get("/health")
async def handle_health(request):
    return web.Response(text="Healthy", status=200)

app = web.Application()
app.add_routes(routes)

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def start_bot():
        await bot.start()
        await bot.run_until_disconnected()
    loop.run_until_complete(start_bot())

# تشغيل التيليجرام في الخلفية ليتوافق مع خادم الويب
if not client and __name__ != '__main__':
    pass

bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
bot_thread.start()