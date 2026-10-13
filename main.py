import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.environ["TOKEN"]
ADMIN_WHATSAPP = os.environ["ADMIN_WHATSAPP"]
PRICES = {
    "p1": ("1 моҳ", "20 сомонӣ"),
    "p2": ("2 моҳ", "40 сомонӣ"),
    "p3": ("6 моҳ", "70 сомонӣ"),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("✅ Ҳа", callback_data="yes"),
           InlineKeyboardButton("❌ Не", callback_data="no")]]
    await update.message.reply_text(
        "Салом! Ба боти мо хуш омадед 👋\n\nБа Шумо галочкаи Instagram даркор Ҳаст?",
        reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try:
        await q.answer()
    except Exception:
        pass
    d = q.data
    if d == "no":
        await q.edit_message_text("Хуб, агар даркор шавад, /start пахш кунед 🙌")
    elif d == "yes":
        kb = [[InlineKeyboardButton(f"{n} — {p}", callback_data=k)]
              for k, (n, p) in PRICES.items()]
        await q.edit_message_text("Нархҳои галочка:\n\nЯкеро интихоб кунед 👇",
                                  reply_markup=InlineKeyboardMarkup(kb))
    elif d in PRICES:
        n, p = PRICES[d]
        u = q.from_user
        un = f"@{u.username}" if u.username else "ном надорад"
        text = f"Салом! Ман галочкаи Instagram мехоҳам.\nТариф: {n} — {p}\nНом: {u.full_name}\nTelegram: {un}"
        link = f"https://wa.me/{ADMIN_WHATSAPP}?text={urllib.parse.quote(text)}"
        kb = [[InlineKeyboardButton("📲 Ба WhatsApp гузаштан", url=link)]]
        await q.edit_message_text(
            f"Шумо интихоб кардед: {n} — {p}\n\nШуморо бо админ пайваст менамоям 👇",
            reply_markup=InlineKeyboardMarkup(kb))

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
print("Бот кор мекунад...")
app.run_polling()
