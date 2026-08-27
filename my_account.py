import os
import asyncio
from aiohttp import web
from telethon import TelegramClient, events
from google import genai

API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = TelegramClient('my_personal_session', API_ID, API_HASH)

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_msg(event):
    sender = await event.get_sender()
    if sender and sender.bot:
        return

    msg = event.raw_text
    if not msg:
        return

    sender_name = sender.first_name if sender else "مستخدم مجهول"
    sender_username = f"@{sender.username}" if sender and sender.username else "لا يوجد معرف"
    
    print(f"📩 رسالة العميل من ({sender_name}): {msg}")

    # برومبت يطلب من الـ AI أن يكون ذكياً ومتفاعلاً حسب رسالة الشخص بالضبط
    prompt = f"""
أنت مساعد شخصي ذكي للمهندس محمد ضهير (مبرمج ومطور تطبيقات). 
قم بالرد على رسالة الشخص التالي بأسلوب بشري، طبيعي، ومرن جداً (في حدود سطر أو سطرين)، وتفاعل مع محتوى رسالته مباشرة بدون تكرار أو جمود:
رسالة العميل: "{msg}"
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        reply = response.text.strip() if response and response.text else "أهلاً بك، وصلني كلامك وسأبلغ المهندس محمد فوراً ♠️."
    except Exception as e:
        print(f"AI Error: {e}")
        # ردود متنوعة وديناميكية حسب الكلمة بدلاً من جملة واحدة مملة
        if "موعد" in msg or "حجز" in msg:
            reply = "أهلاً بك ♠️. تفضل بتحديد الوقت المناسب للموعد وسأقوم بتسجيله وإبلاغ المهندس محمد فوراً 💎."
        elif "مين" in msg or "من أنت" in msg:
            reply = "أنا المساعد الرقمي الخاص بالمهندس محمد ضهير، مبرمج ومطور تطبيقات Flutter ⚡."
        else:
            reply = "أهلاً بك ♠️. تفضل بطرح تفاصيل طلبك وسأقوم بعرضها على المهندس محمد."

    print(f"✨ رد البوت: {reply}")
    
    # 1. الرد على العميل
    await event.reply(reply)

    # 2. إرسال تنبيه لك في الرسائل المحفوظة
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

async def handle_web(request):
    return web.Response(text="Bot is running smoothly 24/7!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_web)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_web_server()
    await bot.start()
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())