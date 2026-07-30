import os
from dotenv import load_dotenv
from groq import Groq
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

async def solve_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    print("Received:", question)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Solve data analysis questions. Reply only valid JSON."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    await update.message.reply_text(answer)


app = Application.builder().token(
    os.getenv("TELEGRAM_TOKEN")
).build()

app.add_handler(
    MessageHandler(filters.TEXT, solve_question)
)

print("Bot running...")
app.run_polling()