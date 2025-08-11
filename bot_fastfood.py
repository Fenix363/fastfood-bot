import json
import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from urllib.parse import quote, unquote
from functools import wraps

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

FILE_PATH = "Buyurtma.json"
HISTORY_FILE = "Eski.json"


from telegram.ext import MessageHandler, filters

menu = {
    "Lavash": {
        "🌯Obichniy": {"narx": 35000, "original_price": 35000, "son": 0}
    },
    "Donar": {
        "🍔 Donar": {"narx": 30000, "original_price": 30000, "son": 0}

    },
    "Hotdog": {
        "🌭 Mesnoy kichkina": {"narx": 10000, "original_price": 10000, "son": 0},
        "🌭 Mesnoy o'rtacha": {"narx": 15000, "original_price": 15000, "son": 0},
        "🌭 Mesnoy katta": {"narx": 20000, "original_price": 20000, "son": 0},
        "🌭 Mesnoy qazili": {"narx": 25000, "original_price": 25000, "son": 0}
    },
    "Ichimlik": {
        "🥤  0.5 L Cola": {"narx": 8000, "original_price": 8000, "son": 0},
        "🥤  0.5 L fanta": {"narx": 8000, "original_price": 8000, "son": 0},
        "🥤  1 L Cola": {"narx": 13000, "original_price": 13000, "son": 0},
        "🥤  1 L fanta": {"narx": 13000, "original_price": 13000, "son": 0},
        "🥤  1.5 L Cola": {"narx": 15000, "original_price": 15000, "son": 0},
        "🥤  1.5 L fanta": {"narx": 15000, "original_price": 15000, "son": 0},
        "🥤⚡ Flesh": {"narx": 13000, "original_price": 13000, "son": 0},
        "🥤⚡ Gorila": {"narx": 13000, "original_price": 13000, "son": 0},
        "🥤⚡ 18+": {"narx": 13000, "original_price": 13000, "son": 0},
        "🧋  Moxito laym": {"narx": 13000, "original_price": 13000, "son": 0},
        "🧋  Moxito Qulubnika": {"narx": 13000, "original_price": 13000, "son": 0},
        "🧋  Moxito ananas": {"narx": 13000, "original_price": 13000, "son": 0},
        "🧊🍹0.5 L Ays tea": {"narx": 6000, "original_price": 6000, "son": 0},
        "🧊🍹1.25 L Ays tea": {"narx": 12000, "original_price": 12000, "son": 0},
        "🧃  1 L Dena sok": {"narx": 15000, "original_price": 15000, "son": 0}
    },
    "Non kabob": {
        "Non kabob": {"narx": 35000, "original_price": 35000, "son": 0}
    }
}

def main():
    global menu
    menu_from_file = load_menu()
    if menu_from_file:
        # Har bir mahsulotga original_price ni tekshirib qo'shish
        for cat, items in menu_from_file.items():
            for name, info in items.items():
                if "original_price" not in info:
                    info["original_price"] = info.get("narx", 0)
                if "available" not in info:
                    info["available"] = True
        menu = menu_from_file
    else:
        menu = {
            "🌯Lavash": {
                "🌯Obichniy": {
                    "narx": 35000,
                    "original_price": 35000,
                    "son": 0,
                    "available": True
                }
            },
            "🍔Donar": {
                "🍔 Donar": {
                    "narx": 30000,
                    "original_price": 30000,
                    "son": 0,
                    "available": True
                }
            },
            "🌭Hotdog": {
                "🌭 Mesnoy kichkina": {
                    "narx": 10000,
                    "original_price": 10000,
                    "son": 0,
                    "available": True
                },
                "🌭 Mesnoy o'rtacha": {
                    "narx": 15000,
                    "original_price": 15000,
                    "son": 0,
                    "available": True
                },
                "🌭 Mesnoy katta": {
                    "narx": 20000,
                    "original_price": 20000,
                    "son": 0,
                    "available": True
                },
                "🌭 Mesnoy qazili": {
                    "narx": 25000,
                    "original_price": 25000,
                    "son": 0,
                    "available": True
                }
            },
            "🥤Ichimlik": {
                "🥤  0.5 L Cola": {
                    "narx": 8000,
                    "original_price": 8000,
                    "son": 0,
                    "available": True
                },
                # ... qolgan ichimliklar ...
            },
            "🥙Non kabob": {
                "🥙Non kabob": {
                    "narx": 35000,
                    "original_price": 35000,
                    "son": 0,
                    "available": True
                }
            }
        }

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ✅ Admin tugmalari uchun handlerlar — AVVAL turishi kerak
    app.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^admin_"))
    app.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^toggle_"))  # toggle tugmalar uchun

    # 🔁 Foydalanuvchi tugmalari (admin tugmalaridan keyin)
    app.add_handler(CallbackQueryHandler(tugma_qabul))

    # 🧾 Xabar va buyruqlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menyu", menyu))
    app.add_handler(CommandHandler("help", unknown))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_message_handler))

    app.run_polling()

def load_menu():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for taom, variants in data.items():
                    for variant, details in variants.items():
                        if "son" not in details:
                            details["son"] = 0
                return data
            except json.JSONDecodeError:
                pass  # JSON yaroqsiz bo‘lsa — quyidagi default qaytadi
    return

def save_menu(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_to_history(user_id, taom, variant, son):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []
    else:
        history = []

    # Yangi buyurtmani tayyorlaymiz
    new_order = {
        "user_id": user_id,
        "taom": taom,
        "variant": variant,
        "son": son
    }

    # Yangi buyurtmani history ga qo'shamiz
    history.append(new_order)

    # Yangilangan tarixni faylga yozamiz
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    contact = update.message.contact
    user_id = user.id

    # Buyurtma tarixi
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

    user_history = [item for item in history if item.get("user_id") == user_id]

    if not user_history:
        await update.message.reply_text("🛒 Sizda buyurtma mavjud emas.")
        return

    context.user_data["user_phone"] = contact.phone_number  # saqlab qo'yamiz


    # Agar yetkazib berish bo‘lsa, joylashuv so‘rash
    if context.user_data.get("yetkazib_berish"):
        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton("📍 Manzilni yuborish", request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await update.message.reply_text(
            "📍 Iltimos, manzilingizni yuboring (location tugmasini bosib):",
            reply_markup=reply_markup
        )

    else:
        # Olib ketish — adminga yuboriladi
        text = (
            f"🆕 Yangi buyurtma (🚶 Olib ketish)!\n"
            f"👤 ID: {user_id}\n"
            f"📞 Telefon: {contact.phone_number}\n\n"
            f"🛒 Buyurtmalar:\n"
        )
        jami_summa = 0
        for item in user_history:
            narx = menu.get(item['taom'], {}).get(item['variant'], {}).get('narx', 0)
            summa = item['son'] * narx
            jami_summa += summa
            text += f"• {item['taom']} — {item['variant']} × {item['son']} = {summa:,} so‘m\n"
        text += f"\n💰 Umumiy summa: {jami_summa:,} so‘m"

        # Admin uchun
        await context.bot.send_message(chat_id=ADMIN_ID, text=text)

        # Foydalanuvchi uchun
        await update.message.reply_location(latitude=41.163266, longitude=69.010759)
        await update.message.reply_text(
            "📍 Do‘kon manzili: Toshkent viloyati, Yangiyol tumani, Halqobod",
            reply_markup=ReplyKeyboardRemove()
        )
        await update.message.reply_text(
            "✅ Buyurtmangiz muvaffaqiyatli rasmiylashtirildi!\nTez orada siz bilan bog‘lanamiz.",
            reply_markup=ReplyKeyboardRemove()
        )

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    location = update.message.location
    phone = context.user_data.get("user_phone", "Noma'lum")

    if not context.user_data.get("yetkazib_berish"):
        return  # agar yetkazib berish rejimi bo'lmasa — chiqib ketamiz

    if not location:
        await update.message.reply_text("❗ Manzil topilmadi.")
        return

    # Buyurtmalar
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

    user_history = [item for item in history if item.get("user_id") == user_id]
    if not user_history:
        await update.message.reply_text("🛒 Buyurtmalar topilmadi.")
        return

    text = (
        f"🆕 Yangi buyurtma (🚚 Yetkazib berish)!\n"
        f"👤 ID: {user_id}\n"
        f"📞 Telefon: {phone}\n\n"
        f"🛒 Buyurtmalar:\n"
    )
    jami_summa = 0
    for item in user_history:
        narx = menu.get(item['taom'], {}).get(item['variant'], {}).get('narx', 0)
        summa = item['son'] * narx
        jami_summa += summa
        text += f"• {item['taom']} — {item['variant']} × {item['son']} = {summa:,} so‘m\n"
    text += f"\n💰 Umumiy summa: {jami_summa:,} so‘m"

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    await context.bot.send_location(chat_id=ADMIN_ID, latitude=location.latitude, longitude=location.longitude)

    await update.message.reply_text("✅ Buyurtmangiz muvaffaqiyatli rasmiylashtirildi! Tez orada siz bilan bog‘lanamiz.", reply_markup=ReplyKeyboardRemove())

    # tozalash
    context.user_data["yetkazib_berish"] = False

def main_menu_keyboard():
    keyboard = []
    categories = list(menu.keys())
    row = []
    for cat in categories:
        if any(info.get("available", True) for info in menu.get(cat, {}).values()):
            row.append(InlineKeyboardButton(f"{cat}", callback_data=f"menu_{cat}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("🛒 Buyurtmalarni olish", callback_data="menu_Buyurtmalar")])
    return InlineKeyboardMarkup(keyboard)

def variants_keyboard(taom):
    keyboard = []
    for variant, data in menu.get(taom, {}).items():
        if data.get("available", True):  # Faqat mavjud mahsulotlar ko'rsin
            narx = data["narx"]
            keyboard.append([InlineKeyboardButton(f"{variant} - {narx} so'm", callback_data=f"item_{taom}_{quote(variant)}")])
    if not keyboard:
        keyboard.append([InlineKeyboardButton("⛔ Mahsulot mavjud emas", callback_data="menu_Orqaga")])
    keyboard.append([InlineKeyboardButton("⬅ Orqaga", callback_data="menu_Orqaga")])
    return InlineKeyboardMarkup(keyboard)

def count_keyboard(taom, variant, son, narx):
    jami = son * narx
    keyboard = [
        [
            InlineKeyboardButton("➖", callback_data=f"count_{taom}_{quote(variant)}_-"),
            InlineKeyboardButton(f"{variant}: {son} ta", callback_data="none"),
            InlineKeyboardButton("➕", callback_data=f"count_{taom}_{quote(variant)}_+")
        ],
        [InlineKeyboardButton(f"💵 Narxi: {jami:,} so'm", callback_data="none")],
        [
            InlineKeyboardButton("✅ Qabul qilish", callback_data=f"qabul_{taom}_{quote(variant)}"),
            InlineKeyboardButton("⬅ Orqaga", callback_data=f"menu_{taom}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Buyurtmalar tarixidan ushbu user_id ga tegishli buyurtmalarni olib tashlaymiz
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

        # Foydalanuvchining barcha buyurtmalarini o'chiramiz
        history = [item for item in history if item.get("user_id") != user_id]

        # Yangilangan ro'yxatni faylga yozamiz
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    # Menyuni boshlash xabari
    await update.message.reply_text("🌟Assalomu alaykom! Friends food botga xush kelibsiz.\nBuyurtma berish uchun /menyu buyrug'ini yuboring.")

async def menyu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Bu flag oldindan boshqa joyda o‘rnatilgan bo‘lishi kerak (masalan, "qayta tanlash" bosilganda)
    if context.user_data.pop("clear_menu_on_next_menyu", False):
        clear_user_order(user_id)

    reply_markup = main_menu_keyboard()
    if update.message:
        await update.message.reply_text("🌟 Menyuga xush kelibsiz! Taomni tanlang:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("🌟 Menyuga xush kelibsiz! Taomni tanlang:", reply_markup=reply_markup)

def clear_user_order(user_id):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

        # Foydalanuvchiga tegishli buyurtmalarni olib tashlaymiz
        history = [item for item in history if item.get("user_id") != user_id]

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

async def tugma_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global menu
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_Buyurtmalar":
        user_id = query.from_user.id
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except:
                    history = []
        else:
            history = []

        user_history = [item for item in history if item.get("user_id") == user_id]

        if not user_history:
            await query.edit_message_text("🛒 Sizning buyurtmalaringiz mavjud emas.")
            return

        matn = f"🛒 Sizning buyurtmalaringiz:\n👤 User ID: {user_id}\n"
        jami_summa=0
        for item in user_history:
           jami_summa=0
        for item in user_history:
            narx = 0
            try:
                narx = menu[item['taom']][item['variant']]['narx']
            except KeyError:
                narx = 0  # Narx topilmasa 0 bo'ladi
            summa = item['son'] * narx
            jami_summa += summa
            matn += f"{item['variant']}: {item['son']} ta = {summa:,} so'm\n"

        matn += f"\n💰 Umumiy summa: {jami_summa:,} so'm"

        tugma = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Buyurtmani rasmiylashtirish", callback_data="rasmiylashtir")],
            [InlineKeyboardButton("❌ Buyurtmani bekor qilish", callback_data="bekor_qilish")],
            [InlineKeyboardButton("🔄 Buyurtmani qayta tanlash", callback_data="qayta_tanlash")],
            [InlineKeyboardButton("⬅ Menyuga qaytish", callback_data="menu_Orqaga")]
        ])

        await query.edit_message_text(matn, reply_markup=tugma)
        return

    if data == "menu_Orqaga":
        reply_markup = main_menu_keyboard()
        await query.edit_message_text("🌟 Menyuga xush kelibsiz! Taomni tanlang:", reply_markup=reply_markup)
        return

    if data.startswith("menu_"):
        taom_nomi = data.split("_")[1]
        variantlar = menu.get(taom_nomi)
        if not variantlar:
            await query.edit_message_text("Variantlar topilmadi.")
            return
        reply_markup = variants_keyboard(taom_nomi)
        await query.edit_message_text(f"{taom_nomi} bo'limi. Variantni tanlang:", reply_markup=reply_markup)
        return

    if data.startswith("item_"):
        _, taom_nomi, variant_enc = data.split("_", 2)
        variant_nomi = unquote(variant_enc)
        son = menu[taom_nomi][variant_nomi]["son"]
        narx = menu[taom_nomi][variant_nomi]["narx"]
        reply_markup = count_keyboard(taom_nomi, variant_nomi, son, narx)
        jami = son * narx
        await query.edit_message_text(
            f"{variant_nomi}\nSoni: {son} ta\nUmumiy narxi: {jami:,} so'm",
            reply_markup=reply_markup
        )
        return

    if data.startswith("count_"):
        _, taom_nomi, variant_enc, amal = data.split("_", 3)
        variant_nomi = unquote(variant_enc)
        son = menu[taom_nomi][variant_nomi]["son"]

        if amal == "+":
            menu[taom_nomi][variant_nomi]["son"] += 1
        elif amal == "-" and son > 0:
            menu[taom_nomi][variant_nomi]["son"] -= 1

        save_menu(menu)

        son = menu[taom_nomi][variant_nomi]["son"]
        narx = menu[taom_nomi][variant_nomi]["narx"]

        reply_markup = count_keyboard(taom_nomi, variant_nomi, son, narx)
        jami = son * narx
        await query.edit_message_text(
            f"{taom_nomi} > {variant_nomi}\nSoni: {son} ta\nUmumiy narxi: {jami:,} so'm",
            reply_markup=reply_markup
        )
        return

    if data.startswith("qabul_"):
        _, taom_nomi, variant_enc = data.split("_", 2)
        variant_nomi = unquote(variant_enc)
        son = menu[taom_nomi][variant_nomi]["son"]

        if son > 0:
            save_to_history(query.from_user.id, taom_nomi, variant_nomi, son)
            menu[taom_nomi][variant_nomi]["son"] = 0
            save_menu(menu)

            await query.edit_message_text(
                f"✅ Buyurtma qabul qilindi:\n{taom_nomi} > {variant_nomi}\nSoni: {son} ta\nMenyuga qaytish uchun kuting..."
            )
            await asyncio.sleep(1)
            reply_markup = main_menu_keyboard()
            await query.edit_message_text("🌟 Menyuga xush kelibsiz! Taomni tanlang:", reply_markup=reply_markup)
        else:
            await query.answer("Iltimos, buyurtma miqdorini 0 dan katta qiling!", show_alert=True)
        return

    elif data == "rasmiylashtir":
        user_id = query.from_user.id
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except:
                    history = []

        user_history = [item for item in history if item.get("user_id") == user_id]

        if not user_history:
            await query.answer("Buyurtmalar topilmadi!", show_alert=True)
            return

        jami_summa = 0
        matn = "📋 Buyurtma ro'yxati:\n"
        for item in user_history:
            narx = menu.get(item['taom'], {}).get(item['variant'], {}).get('narx', 0)
            original = menu.get(item['taom'], {}).get(item['variant'], {}).get('original_price', narx)
            summa = item['son'] * narx
            jami_summa += summa

            if narx < original:
                chegirma_foiz = round((original - narx) / original * 100)
                matn += f"🔻 {item['taom']} — {item['variant']} {item['son']} ta = {summa:,} so‘m (−{chegirma_foiz}%)\n"
            else:
                matn += f"• {item['taom']} — {item['variant']} {item['son']} ta = {summa:,} so‘m\n"

        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton("📞 Telefonni yuborish", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await query.message.reply_text(matn, reply_markup=reply_markup)

        choice_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚶‍♂️ Kelib olib ketish", callback_data="olib_ketish")],
            [InlineKeyboardButton("🚚 Yetkazib berish", callback_data="yetkazib_berish")]
        ])
        await query.message.reply_text("Iltimos, yetkazib berish usulini tanlang:", reply_markup=choice_keyboard)
        return
    elif data == "olib_ketish":
        user_id = query.from_user.id

        # Raqam so'rash uchun tugma
        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await context.bot.send_message(chat_id=user_id,
                                       text="📲 Iltimos, telefon raqamingizni yuboring:",
                                       reply_markup=reply_markup
                                       )

        await query.message.delete()  # Tugmani o'chirish
        return
    elif data == "yetkazib_berish":
        user_id = query.from_user.id

        # Telefon raqam so‘rash
        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await context.bot.send_message(chat_id=user_id,
                                       text="📲 Iltimos, telefon raqamingizni yuboring (yetkazib berish uchun):",
                                       reply_markup=reply_markup
                                       )

        # Holatni belgilab qo'yish uchun context ichida flag saqlash
        context.user_data["yetkazib_berish"] = True
        await query.message.delete()
        return



    elif data == "yetkazib_berish":
        user_id = query.from_user.id
        await context.bot.send_message(chat_id=user_id,
                                       text="✅ Buyurtmangiz yetkazib berish uchun qabul qilindi!\nIltimos, yetkazib berish manzilingizni yozing."
                                       )
        await query.message.delete()  # Oldingi tugmalarni o'chirish (ixtiyoriy)
        return
    if data == "bekor_qilish":
        user_id = query.from_user.id
        # Buyurtmalar tarixidan ushbu user_id ga tegishli buyurtmalarni o'chirish
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except:
                    history = []
            history = [item for item in history if item.get("user_id") != user_id]
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)

        # Foydalanuvchiga xabar yuborish
        await query.edit_message_text(
            "❌ Buyurtmangiz bekor qilindi. Yangi buyurtma berish uchun /menyu buyrug'ini yuboring.")
        return

    elif data == "qayta_tanlash":
        user_id = query.from_user.id

        # Tarix faylidan foydalanuvchining buyurtmalarini o‘chirish
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except:
                    history = []

            # Faqat boshqa foydalanuvchilarning buyurtmalarini qoldirish
            history = [item for item in history if item.get("user_id") != user_id]

            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)

        # Menyuga qaytarish
        reply_markup = main_menu_keyboard()
        await query.edit_message_text("🌟 Buyurtmalar o‘chirildi. Yangi tanlov uchun taomni tanlang:",
                                      reply_markup=reply_markup)
        return

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            if update.message:
                await update.message.reply_text("⛔ Siz admin emassiz.")
            elif update.callback_query:
                await update.callback_query.answer("⛔ Siz admin emassiz.", show_alert=True)
            return
        return await func(update, context)
    return wrapper

@admin_only
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("➕ Mahsulot qo‘shish", callback_data="admin_add_product")],
        [InlineKeyboardButton("🗑 Mahsulotni o‘chirish", callback_data="admin_delete_product")],
        [InlineKeyboardButton("✏️ Narxni tahrirlash", callback_data="admin_edit_price")],
        [InlineKeyboardButton("📦 Mahsulotlarga chegirma", callback_data='admin_discount')],
        [InlineKeyboardButton("👁 Mahsulot mavjudligini boshqarish", callback_data="admin_toggle_availability")],
        [InlineKeyboardButton("❌ Chegrimani bekor qilish", callback_data='admin_remove_discount')],
        [InlineKeyboardButton("📄 Buyurtmalarni ko‘rish", callback_data='admin_orders')]
    ]
    if query:
        await query.edit_message_text(
            "🛠 Admin panelga xush kelibsiz!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            "🛠 Admin panelga xush kelibsiz!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

@admin_only
async def admin_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global menu
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "admin_discount":
        text = "📦 Mahsulotlar ro'yxati:\n"
        idx = 1
        discount_map = {}

        for cat, items in menu.items():
            for name, info in items.items():
                narx = info.get('narx', 0)
                text += f"{idx}. {cat} - {name} | {narx:,} so'm\n"
                discount_map[str(idx)] = (cat, name)
                idx += 1

        if not discount_map:
            await query.edit_message_text("❌ Mahsulotlar topilmadi.")
            return

        context.user_data["discount_map"] = discount_map
        context.user_data["awaiting_discount_id"] = True
        await query.edit_message_text(
            text + "\n\nQaysi mahsulotga chegirma qo‘shmoqchisiz? (raqamini yozing):"
        )

    elif data == "admin_remove_discount":
        # Chegrimalarni bekor qilish uchun menyuni asl narxlarga tiklaymiz
        reset_count = 0
        for cat, items in menu.items():
            for name, info in items.items():
                # Agar asl narx saqlangan bo‘lsa, narxni asl holatga qaytaramiz
                if "original_price" in info:
                    info["narx"] = info["original_price"]
                    reset_count += 1
        save_menu(menu)
        await query.edit_message_text(f"✅ Barcha mahsulotlarning chegirmalari bekor qilindi. ({reset_count} ta mahsulot)")

    elif data == "admin_orders":
        if not os.path.exists(HISTORY_FILE):
            await query.edit_message_text("Buyurtmalar mavjud emas.")
            return

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

        if not history:
            await query.edit_message_text("Buyurtmalar mavjud emas.")
            return

        text = "📄 Buyurtmalar ro'yxati:\n"
        for item in history[-10:]:
            text += (
                f"👤 {item['user_id']}\n"
                f"• {item['taom']} - {item['variant']} × {item['son']}\n\n"
            )

        await query.edit_message_text(text)
    elif data == "admin_edit_price":
        text = "✏️ Narxni o‘zgartirish uchun mahsulotni tanlang:\n"
        idx = 1
        edit_map = {}

        for cat, items in menu.items():
            for name, info in items.items():
                narx = info.get('narx', 0)
                text += f"{idx}. {cat} - {name} | {narx:,} so‘m\n"
                edit_map[str(idx)] = (cat, name)
                idx += 1

        if not edit_map:
            await query.edit_message_text("⚠️ Hech qanday mahsulot topilmadi.")
            return

        context.user_data["edit_map"] = edit_map
        context.user_data["awaiting_edit_id"] = True

        await query.edit_message_text(
            text + "\n\nQaysi mahsulot narxini o‘zgartirmoqchisiz? (raqam bilan yuboring):"
        )

    elif data == "admin_add_product":
        categories = list(menu.keys())
        category_buttons = [
            [InlineKeyboardButton(cat, callback_data=f"admin_add_cat_{cat}")]
            for cat in categories
        ]
        reply_markup = InlineKeyboardMarkup(category_buttons)
        await query.edit_message_text("🗂 Bo‘lim tanlang (yangi mahsulotni qayerga qo‘shamiz?):",
                                      reply_markup=reply_markup)

    elif data.startswith("admin_add_cat_"):
        cat = data.replace("admin_add_cat_", "")
        context.user_data["adding_product_category"] = cat
        context.user_data["awaiting_new_product_name"] = True
        await query.edit_message_text(f"✍️ '{cat}' bo‘limiga mahsulot nomini kiriting:")

    elif data == "admin_delete_product":
        idx = 1
        delete_map = {}
        text = "🗑 Qaysi mahsulotni o‘chirmoqchisiz? Raqamini kiriting:\n"

        for cat, items in menu.items():
            for name in items:
                text += f"{idx}. {cat} - {name}\n"
                delete_map[str(idx)] = (cat, name)
                idx += 1

        if not delete_map:
            await query.edit_message_text("⚠️ Hech qanday mahsulot topilmadi.")
            return

        context.user_data["delete_map"] = delete_map
        context.user_data["awaiting_delete_id"] = True

        await query.edit_message_text(text)

    elif data == "admin_toggle_availability":
        idx = 1
        toggle_map = {}
        buttons = []
        for cat, items in menu.items():
            for name, info in items.items():
                status = "✅ mavjud" if info.get("available", True) else "❌ mavjud emas"
                buttons.append(
                    [InlineKeyboardButton(f"{idx}. {cat} - {name} ({status})", callback_data=f"toggle_{idx}")])
                toggle_map[str(idx)] = (cat, name)
                idx += 1
        context.user_data["toggle_map"] = toggle_map
        await query.edit_message_text(
            "🔃 Mahsulot holatini o‘zgartirish uchun tugmani bosing:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("toggle_"):
        idx = data.split("_")[1]
        toggle_map = context.user_data.get("toggle_map", {})

        if idx not in toggle_map:
            await query.answer("⚠️ Xatolik: mahsulot topilmadi.")
            return

        cat, name = toggle_map[idx]
        info = menu[cat][name]
        info["available"] = not info.get("available", True)
        save_menu(menu)

        # Yangi holatni ko‘rsatish uchun barcha tugmalarni yangilaymiz
        idx = 1
        new_map = {}
        buttons = []
        for c, items in menu.items():
            for n, i in items.items():
                status = "✅ mavjud" if i.get("available", True) else "❌ mavjud emas"
                buttons.append([
                    InlineKeyboardButton(f"{idx}. {c} - {n} ({status})", callback_data=f"toggle_{idx}")
                ])
                new_map[str(idx)] = (c, n)
                idx += 1

        # 🔙 Ortga tugmasini oxiriga qo‘shamiz
        buttons.append([
            InlineKeyboardButton("🔙 Ortga", callback_data="admin_panel")
        ])

        context.user_data["toggle_map"] = new_map
        await query.edit_message_text(
            "🔄 Yangilandi. Yana bir mahsulotni tanlang:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "admin_panel":
        await admin_panel(update, context)

@admin_only
async def admin_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Agar mahsulot raqami so‘ralayotgan bo‘lsa
    if context.user_data.get("awaiting_discount_id"):
        if text in context.user_data.get("discount_map", {}):
            cat, name = context.user_data["discount_map"][text]
            context.user_data["selected_discount_item"] = (cat, name)
            context.user_data["awaiting_discount_id"] = False
            context.user_data["awaiting_discount_value"] = True
            await update.message.reply_text(
                f"{cat} - {name} tanlandi. Chegirma foizini kiriting (0-100). "
                f"0 ni kiritsangiz, chegirma bekor qilinadi."
            )
        else:
            await update.message.reply_text("❌ Noto‘g‘ri raqam. Qaytadan urinib ko‘ring.")
        return

    # Agar chegirma foizi kiritilishi kutilayotgan bo‘lsa
    if context.user_data.get("awaiting_discount_value"):
        try:
            value = int(text)
            if 0 <= value <= 100:
                cat, name = context.user_data["selected_discount_item"]
                old_price = menu[cat][name]["narx"]

                if value == 0:
                    # Chegirma bekor qilish uchun asl narxga qaytarish:
                    if "original_price" in menu[cat][name]:
                        menu[cat][name]["narx"] = menu[cat][name]["original_price"]

                    await update.message.reply_text(
                        f"ℹ {cat} - {name} uchun chegirma bekor qilindi. Narx o'zgarmadi: {menu[cat][name]['narx']} so'm"
                    )

                else:
                    # Chegirma hisoblash uchun asl narx kerak
                    # Agar asl narx o‘zgargan bo‘lsa, uni saqlab qo‘yganingiz ma’qul (masalan, 'original_price')
                    # Misol uchun biz hozir yangi kalit qo‘shamiz:

                    if "original_price" not in menu[cat][name]:
                        menu[cat][name]["original_price"] = old_price
                    original_price = menu[cat][name]["original_price"]

                    new_price = original_price * (100 - value) // 100
                    menu[cat][name]["narx"] = new_price

                    await update.message.reply_text(
                        f"✅ {cat} - {name} uchun {value}% chegirma qo‘llandi. Yangi narx: {new_price} so‘m"
                    )

                # O‘zgarishlarni saqlash
                save_menu(menu)

                # Holatlarni tozalash
                context.user_data["awaiting_discount_value"] = False
                context.user_data.pop("selected_discount_item", None)
            else:
                await update.message.reply_text("❗ Chegirma 0 dan 100 gacha bo'lishi kerak.")
        except ValueError:
            await update.message.reply_text("❗ Iltimos, faqat raqam kiriting.")
        return

    if context.user_data.get("awaiting_edit_id"):
        if not text.isdigit():
            await update.message.reply_text("⚠️ Iltimos, raqam kiriting.")
            return

        edit_map = context.user_data.get("edit_map", {})
        selected = edit_map.get(text)
        if not selected:
            await update.message.reply_text("❌ Noto‘g‘ri raqam.")
            return

        taom, variant = selected
        context.user_data["edit_mahsulot"] = {
            "taom": taom,
            "variant": variant
        }
        context.user_data["awaiting_edit_id"] = False
        context.user_data["awaiting_edit_value"] = True

        await update.message.reply_text(f"✏️ {taom} > {variant} uchun yangi narxni kiriting:")
        return
    elif context.user_data.get("awaiting_edit_value"):
        try:
            yangi_narx = int(text)
        except ValueError:
            await update.message.reply_text("⚠️ Raqam kiriting.")
            return

        info = context.user_data.pop("edit_mahsulot")
        context.user_data["awaiting_edit_value"] = False

        taom = info["taom"]
        variant = info["variant"]
        mahsulot = menu[taom][variant]

        mahsulot["narx"] = yangi_narx
        save_menu(menu)

        await update.message.reply_text(f"✅ {taom} > {variant} narxi yangilandi: {yangi_narx:,} so‘m")
        return

    if context.user_data.get("awaiting_new_product_name"):
        name = text.strip()
        if not name:
            await update.message.reply_text("❌ Mahsulot nomi bo‘sh bo‘lishi mumkin emas.")
            return

        context.user_data["new_product_name"] = name
        context.user_data["awaiting_new_product_name"] = False
        context.user_data["awaiting_new_product_price"] = True

        await update.message.reply_text(f"💰 '{name}' uchun narxni kiriting (so‘mda):")
        return
    elif context.user_data.get("awaiting_new_product_price"):
        try:
            narx = int(text.strip())
        except ValueError:
            await update.message.reply_text("❌ Iltimos, narxni faqat raqam bilan kiriting.")
            return

        cat = context.user_data.pop("adding_product_category")
        name = context.user_data.pop("new_product_name")
        context.user_data["awaiting_new_product_price"] = False

        # Yangi mahsulotni qo‘shamiz
        if cat not in menu:
            menu[cat] = {}

        menu[cat][name] = {
            "narx": narx,
            "original_price": narx,
            "son": 0
        }

        save_menu(menu)

        await update.message.reply_text(
            f"✅ Yangi mahsulot qo‘shildi:\n📂 Bo‘lim: {cat}\n📌 Nomi: {name}\n💰 Narxi: {narx:,} so‘m"
        )
        return

    if context.user_data.get("awaiting_delete_id"):
        delete_map = context.user_data.get("delete_map", {})
        selected = delete_map.get(text.strip())

        if not selected:
            await update.message.reply_text("❌ Noto‘g‘ri raqam. Qayta urinib ko‘ring.")
            return

        cat, name = selected
        del menu[cat][name]

        # Agar kategoriya bo‘sh qolsa, uni ham o‘chirish mumkin (ixtiyoriy)
        if not menu[cat]:
            del menu[cat]

        save_menu(menu)

        context.user_data["awaiting_delete_id"] = False
        context.user_data.pop("delete_map", None)

        await update.message.reply_text(f"🗑 Mahsulot o‘chirildi:\n📂 {cat} > 📌 {name}")
        return
    if context.user_data.get("awaiting_toggle_id"):
        toggle_map = context.user_data.get("toggle_map", {})
        selected = toggle_map.get(text.strip())

        if not selected:
            await update.message.reply_text("❌ Noto‘g‘ri raqam.")
            return

        cat, name = selected
        mahsulot = menu[cat][name]
        current = mahsulot.get("available", True)
        mahsulot["available"] = not current
        save_menu(menu)

        holat = "✅ mavjud" if mahsulot["available"] else "❌ mavjud emas"
        await update.message.reply_text(f"📌 {cat} > {name} endi: {holat}")
        context.user_data["awaiting_toggle_id"] = False
        return

def remove_all_discounts():
    global menu
    count = 0
    for cat, items in menu.items():
        for name, info in items.items():
            if "original_price" in info:
                info["narx"] = info["original_price"]
                count += 1
    save_menu(menu)  # O'zgarishlarni saqlash
    return count

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Noma'lum buyruq. /menyu orqali menyuni ko'ring.")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 5000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    main()
