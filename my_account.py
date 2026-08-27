import os
from telethon import TelegramClient, events
from google import genai
import random

# قراءة البيانات الأساسية بأمان
API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = TelegramClient('my_personal_session', API_ID, API_HASH)

# ردود فخمة ومتنوعة تتضمن اسمك ومستشار برلين بوضوح
SMART_FALLBACKS = [
    "أهلاً بك ♠️. معك مستشار برلين الخاص بالمهندس محمد ضهير (مطور تطبيقات Flutter بخبرة تزيد عن 5 سنوات). تفضل بطرح تفاصيل مشروعك لنعرضه على طاولته 💎.",
    "تحية طيبة ⚡. معك مستشار برلين، الوكيل الرقمي للمهندس محمد ضهير. كيف يمكننا تحويل أفكارك التقنية إلى واقع برمجي مبهر اليوم؟ ♠️",
    "أهلاً بك 🏛️. معك مستشار برلين ممثلاً عن المهندس محمد ضهير. نحن هنا لإدارة تطلعاتك البرمجية باحترافية مطلقة، تفضل بطرح استفسارك 💎.",
    "معك مستشار برلين الخاص بالمهندس محمد ضهير ♠️. نتشرف باستقبال أفكارك ومشاريعك لنرسم معاً خارطة طريق نجاحك التقني ⚡."
]

last_used_reply = ""

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_msg(event):
    global last_used_reply
    sender = await event.get_sender()
    if sender and sender.bot:
        return

    msg = event.raw_text
    if not msg:
        return

    print(f"📩 رسالة العميل: {msg}")

    prompt = f"""
أنت "مستشار برلين"، الوكيل الرقمي الخاص بالمهندس محمد ضهير (مبرمج ومطور تطبيقات Flutter بخبرة تزيد عن 5 سنوات).
قواعد الرد الصارمة:
1. اذكر دائماً بأسلوب فخم أنك "مستشار برلين الخاص بالمهندس محمد ضهير".
2. رد بأسلوب نخبوي، ومختصر جداً (في حدود سطرين).
3. استخدم رموزاً أنيقة مثل (♠️، 💎).
4. تفاعل بذكاء فريد مع رسالة العميل التالية: "{msg}"
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        reply = response.text if response and response.text else None
        if not reply:
            raise Exception("Empty response")
    except Exception as e:
        available_choices = [r for r in SMART_FALLBACKS if r != last_used_reply]
        reply = random.choice(available_choices)
        print(f"⚠️ تم استخدام الرد البديل المتنوع.")

    last_used_reply = reply
    print(f"✨ رد البوت: {reply}")
    await event.reply(reply)

def main():
    print("==================================================")
    print(" 🏛️ مستشار برلين (النسخة النهائية المحدثة تعمل)")
    print("==================================================")
    bot.start()
    print("البوت جاهز للرد مع ذكر اسمك بكل فخامة!")
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()