import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")

questions = [
    {
        "q": "বাংলাদেশের রাজধানী কোনটি?",
        "options": ["চট্টগ্রাম", "ঢাকা", "রাজশাহী", "খুলনা"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশ স্বাধীন হয় কত সালে?",
        "options": ["১৯৬৯", "১৯৭০", "১৯৭১", "১৯৭২"],
        "answer": 2
    },
    {
        "q": "বাংলাদেশের জাতীয় ফুল কোনটি?",
        "options": ["গোলাপ", "শাপলা", "পদ্ম", "বকুল"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশের মুক্তিযুদ্ধে কতজন শহীদ হন?",
        "options": ["১০ লাখ", "২০ লাখ", "৩০ লাখ", "৪০ লাখ"],
        "answer": 2
    },
    {
        "q": "বাংলাদেশের জাতীয় পাখি কোনটি?",
        "options": ["ময়না", "দোয়েল", "শালিক", "কোকিল"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশের সংবিধান কত সালে প্রণীত হয়?",
        "options": ["১৯৭১", "১৯৭২", "১৯৭৩", "১৯৭৪"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশের প্রথম রাষ্ট্রপতি কে?",
        "options": ["জিয়াউর রহমান", "শেখ মুজিবুর রহমান", "আবু সাঈদ চৌধুরী", "মোশতাক আহমেদ"],
        "answer": 1
    },
    {
        "q": "পদ্মা নদীর উৎপত্তি কোথায়?",
        "options": ["হিমালয়", "গঙ্গা নদী", "ব্রহ্মপুত্র", "মেঘনা"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশের জাতীয় সংসদে আসন সংখ্যা কত?",
        "options": ["২৫০", "৩০০", "৩৫০", "৪০০"],
        "answer": 1
    },
    {
        "q": "সুন্দরবন কোন জেলায় অবস্থিত?",
        "options": ["বরিশাল", "খুলনা", "পটুয়াখালী", "সাতক্ষীরা"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশের জাতীয় ফল কোনটি?",
        "options": ["আম", "কাঁঠাল", "কলা", "লিচু"],
        "answer": 1
    },
    {
        "q": "ছয় দফা দাবি কত সালে উত্থাপিত হয়?",
        "options": ["১৯৬৪", "১৯৬৬", "১৯৬৮", "১৯৭০"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশের কোন নদী সবচেয়ে দীর্ঘ?",
        "options": ["পদ্মা", "মেঘনা", "যমুনা", "সুরমা"],
        "answer": 1
    },
    {
        "q": "বাংলাদেশের জাতীয় মাছ কোনটি?",
        "options": ["রুই", "কাতলা", "ইলিশ", "চিংড়ি"],
        "answer": 2
    },
    {
        "q": "বাংলাদেশের প্রথম প্রধানমন্ত্রী কে?",
        "options": ["তাজউদ্দীন আহমদ", "শেখ মুজিবুর রহমান", "মনসুর আলী", "নজরুল ইসলাম"],
        "answer": 0
    },
]

user_scores = {}
user_current_q = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"""🎓 *BCS গুরু বটে স্বাগতম, {user.first_name}!*

আমি তোমাকে BCS পরীক্ষার প্রস্তুতিতে সাহায্য করবো।

📚 *কমান্ড লিস্ট:*
/quiz - MCQ প্র্যাকটিস শুরু করো
/score - তোমার স্কোর দেখো
/help - সাহায্য

চলো শুরু করি! 💪"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    q_index = random.randint(0, len(questions) - 1)
    user_current_q[user_id] = q_index
    
    q = questions[q_index]
    keyboard = []
    for i, option in enumerate(q["options"]):
        keyboard.append([InlineKeyboardButton(f"{['ক', 'খ', 'গ', 'ঘ'][i]}) {option}", callback_data=str(i))])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"❓ *প্রশ্ন:*\n\n{q['q']}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    selected = int(query.data)
    
    if user_id not in user_current_q:
        await query.edit_message_text("❌ আগে /quiz দিয়ে প্রশ্ন শুরু করো!")
        return
    
    q_index = user_current_q[user_id]
    q = questions[q_index]
    correct = q["answer"]
    
    if user_id not in user_scores:
        user_scores[user_id] = {"correct": 0, "total": 0}
    
    user_scores[user_id]["total"] += 1
    
    if selected == correct:
        user_scores[user_id]["correct"] += 1
        result = f"✅ *সঠিক উত্তর!* 🎉\n\nউত্তর: {q['options'][correct]}"
    else:
        result = f"❌ *ভুল উত্তর!*\n\nসঠিক উত্তর: {q['options'][correct]}"
    
    score = user_scores[user_id]
    result += f"\n\n📊 স্কোর: {score['correct']}/{score['total']}"
    result += "\n\n➡️ আরেকটি প্রশ্নের জন্য /quiz লিখো"
    
    await query.edit_message_text(result, parse_mode='Markdown')

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_scores or user_scores[user_id]["total"] == 0:
        await update.message.reply_text("❌ এখনো কোনো quiz দাওনি!\n\n/quiz দিয়ে শুরু করো।")
        return
    
    s = user_scores[user_id]
    percent = (s['correct'] / s['total']) * 100
    
    if percent >= 80:
        grade = "🏆 অসাধারণ!"
    elif percent >= 60:
        grade = "👍 ভালো!"
    elif percent >= 40:
        grade = "📚 আরো পড়তে হবে"
    else:
        grade = "💪 চেষ্টা চালিয়ে যাও"
    
    text = f"""📊 *তোমার স্কোর কার্ড*

✅ সঠিক: {s['correct']}
❌ ভুল: {s['total'] - s['correct']}
📝 মোট: {s['total']}
📈 শতকরা: {percent:.1f}%

{grade}"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """📚 *BCS গুরু - সাহায্য*

/start - বট শুরু করো
/quiz - নতুন MCQ প্রশ্ন পাও
/score - তোমার স্কোর দেখো
/help - এই মেনু দেখো

💡 *টিপস:* প্রতিদিন কমপক্ষে ১০টি প্রশ্ন দাও!"""
    await update.message.reply_text(text, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(answer))
    print("BCS গুরু বট চালু হয়েছে! ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
