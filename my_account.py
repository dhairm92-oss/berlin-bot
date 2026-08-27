import os
import asyncio
from aiohttp import web
from telethon import TelegramClient, events
from google import genai

# قراءة البيانات الأساسية بأمان
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

    # برومبت صارم يمنع التكرار والحشو ويجعل الرد بشرياً بحتاً
    prompt = f"""
أنت الوكيل الرقمي للمهندس محمد ضهير (مطور تطبيقات Flutter بخبرة تزيد عن 5 سنوات).
قواعد الرد الصارمة جداً:
1. لا تكرر أبداً أي جمل ترحيبية أو تعريفية (مثل "معك مستشار برلين...") إلا إذا كان السياق يحتم ذلك في أول تواصل فقط. كونك تتحدث مع عميل رد على سؤاله مباشرة بدون مقدمات.
2. كن طبيعياً، بشرياً، ومختصراً جداً (في حدود سطر أو سطرين).
3. إذا طلب المستخدم موعداً، اطلب منه بأسلوب راقي تحديد وقت الموعد والتفاصيل ليتم إبلاغ المهندس محمد بها فوراً.
4. استخدم رموزاً أنيقة باعتدال (مثل ♠️، 💎).
5. رد على رسالة العميل التالية بذكاء وواقعية: "{msg}"
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        reply = response.text if response and response.text else "أهلاً بك، تفضل بطرح تفاصيل طلبك لنعرضها على المهندس محمد ♠️."
    except Exception as e:
        reply = "أهلاً بك ♠️. تفضل بطرح تفاصيل استفسارك أو موعدك وسأقوم بإبلاغ المهندس محمد ضهير فوراً 💎."

    print(f"✨ رد البوت: {reply}")
    
    # 1. الرد على العميل مباشرة
    await event.reply(reply)

    # 2. إرسال تنبيه فوري لك في الرسائل المحفوظة
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
        print(f"⚠️ لم يتم إرسال التنبيه الشخصي: {e}")

# بورت الويب الوهمي لضمان استقرار السيرفر 24/7
async def handle_web(request):
    return web.Response(text="Berlin Agent is running 24/7 perfectly! ♠️")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_web)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 الويب سيرفر الوهمي يعمل بنجاح على البورت {port}")

async def main():
    print("==================================================")
    print(" 🏛️ مستشار برلين (النسخة النقية الخالية من التكرار)")
    print("==================================================")
    
    await start_web_server()
    await bot.start()
    print("البوت جاهز وبأفضل أداء بشري!")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())