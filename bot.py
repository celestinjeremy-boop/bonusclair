
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎯 Missions", callback_data="missions")],
        [InlineKeyboardButton("💰 Mon solde", callback_data="balance")],
        [InlineKeyboardButton("💸 Retraits", callback_data="retraits")],
        [InlineKeyboardButton("👥 Parrainage", callback_data="parrainage")],
        [InlineKeyboardButton("📜 Règles et assistance", callback_data="aide")],
    ]

    await update.message.reply_text(
        "🎁 Bienvenue sur BonusClair !\n\n"
        "Des missions, des récompenses et des règles transparentes.\n\n"
        "🚧 Plateforme en préparation : les gains et paiements "
        "ne sont pas encore disponibles.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def missions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 MISSIONS\n\n"
        "Les missions partenaires seront bientôt disponibles.\n"
        "Aucune récompense n'est encore activée."
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 MON SOLDE\n\n"
        "Ton portefeuille sera disponible au lancement."
    )

async def retraits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 RETRAITS\n\n"
        "Seuil prévu : 10 €.\n"
        "Les paiements ne sont pas encore activés."
    )

async def parrainage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👥 PARRAINAGE\n\n"
        "Bonus prévu : 1 € après la première mission "
        "validée de ton filleul.\n"
        "Le système sera activé ultérieurement."
    )

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 RÈGLES ET ASSISTANCE\n\n"
        "Les règles, conditions des missions et modalités "
        "de retrait seront publiées avant le lancement.\n\n"
        "Une assistance sera également mise en place."
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "missions": "🎯 Les missions partenaires arrivent bientôt.",
        "balance": "💰 Ton portefeuille sera disponible au lancement.",
        "retraits": "💸 Seuil prévu : 10 €. Paiements non activés.",
        "parrainage": "👥 Bonus prévu : 1 € après une mission validée.",
        "aide": "📜 Les règles et l'assistance seront bientôt disponibles.",
    }

    await query.message.reply_text(messages.get(query.data, "Rubrique indisponible."))

def main():
    if not BOT_TOKEN:
        raise RuntimeError("Le token BOT_TOKEN n'est pas configuré.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("missions", missions))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("retraits", retraits))
    app.add_handler(CommandHandler("parrainage", parrainage))
    app.add_handler(CommandHandler("help", aide))
    app.add_handler(CommandHandler("aide", aide))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("BonusClair est lancé !")
    app.run_polling()

if __name__ == "__main__":
    from telegram.ext import CallbackQueryHandler
    main()
