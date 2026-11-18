import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

telegram_app = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Bienvenue sur BonusClair ! 🎁\n\n"
        "Le bot est en cours de préparation. "
        "Les missions et les récompenses arriveront bientôt."
    )


async def missions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📋 Les missions BonusClair seront bientôt disponibles."
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💰 Ton solde sera affiché ici lorsque le système de récompenses sera activé."
    )


async def retraits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💳 Les informations de retrait seront bientôt disponibles."
    )


async def parrainage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤝 Le parrainage BonusClair sera bientôt disponible."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commandes BonusClair :\n"
        "/start — Accueil\n"
        "/missions — Voir les missions\n"
        "/balance — Voir ton solde\n"
        "/retraits — Informations sur les retraits\n"
        "/parrainage — Parrainage\n"
        "/help — Aide"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    global telegram_app

    if not BOT_TOKEN:
        raise RuntimeError("La variable BOT_TOKEN est absente dans Render.")
    if not RENDER_EXTERNAL_URL:
        raise RuntimeError("La variable RENDER_EXTERNAL_URL est absente.")

    telegram_app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("missions", missions))
    telegram_app.add_handler(CommandHandler("balance", balance))
    telegram_app.add_handler(CommandHandler("retraits", retraits))
    telegram_app.add_handler(CommandHandler("parrainage", parrainage))
    telegram_app.add_handler(CommandHandler("help", help_command))

    await telegram_app.initialize()
    await telegram_app.start()

    webhook_url = f"{RENDER_EXTERNAL_URL.rstrip('/')}/telegram"
    await telegram_app.bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET if WEBHOOK_SECRET else None,
        allowed_updates=Update.ALL_TYPES,
    )
    logger.info("Webhook Telegram configuré.")

    try:
        yield
    finally:
        if telegram_app:
            await telegram_app.bot.delete_webhook()
            await telegram_app.stop()
            await telegram_app.shutdown()
            telegram_app = None


app = FastAPI(title="BonusClair", lifespan=lifespan)


@app.get("/")
async def health():
    return {"status": "BonusClair en ligne"}


@app.post("/telegram")
async def telegram_webhook(request: Request):
    if telegram_app is None:
        raise HTTPException(status_code=503, detail="Bot non initialisé")

    if WEBHOOK_SECRET:
        received_secret = request.headers.get(
            "X-Telegram-Bot-Api-Secret-Token"
        )
        if received_secret != WEBHOOK_SECRET:
            raise HTTPException(status_code=403, detail="Secret invalide")

    try:
        payload = await request.json()
        update = Update.de_json(payload, telegram_app.bot)
        await telegram_app.process_update(update)
    except Exception:
        logger.exception("Erreur lors du traitement d'une mise à jour Telegram.")
        raise HTTPException(status_code=500, detail="Erreur de traitement")

    return {"ok": True}
