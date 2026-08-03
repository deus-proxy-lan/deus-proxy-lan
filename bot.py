import telebot
from datetime import datetime, timedelta, timezone
import json
import os

TOKEN_BOT = "8750716094:AAF29inoucagFHOHobkX1vMknVeL_bIL4o8"
CLAVE_VIP = "NKGVIPDEUS"
ARCHIVO_IPS = "ips_autorizadas.json"
HORA_DOM = timezone(timedelta(hours=-4))

# ⏳ CLAVE DURA 24 HORAS — VENCE MAÑANA A ESTA HORA
FECHA_FIN = datetime.now(HORA_DOM) + timedelta(days=1)

bot = telebot.TeleBot(TOKEN_BOT)

def cargar_ips():
    if os.path.exists(ARCHIVO_IPS):
        with open(ARCHIVO_IPS, "r") as f:
            return set(json.load(f))
    return set()

def guardar_ips(ips):
    with open(ARCHIVO_IPS, "w") as f:
        json.dump(list(ips), f)

@bot.message_handler(commands=['start'])
def bienvenida(m):
    bot.reply_to(m, """👋 **DEUS MOODZ VIP**
🔑 Comando: `/activar NKGVIPDEUS TU_IP`
⚠️ Clave válida **SOLO POR HOY** — Vence mañana a esta hora""", parse_mode="Markdown")

@bot.message_handler(commands=['activar'])
def activar(m):
    partes = m.text.strip().split()
    if len(partes) < 3:
        bot.reply_to(m, "❌ Usa: `/activar NKGVIPDEUS TU_IP`", parse_mode="Markdown")
        return
    clave = partes[1].strip().upper()
    ip = partes[2].strip()
    ips = cargar_ips()

    if clave == CLAVE_VIP:
        if datetime.now(HORA_DOM) < FECHA_FIN:
            ips.add(ip)
            guardar_ips(ips)
            bot.reply_to(m, f"""✅ **ACTIVADO CON ÉXITO** ✅

🌐 IP autorizada: `{ip}`
⏳ Vence: MAÑANA a esta hora

📝 Tus datos:
🔹 IP: `198.23.243.226`
🔹 Puerto: `6361`
🔹 Usuario: `Giduqmqn`
🔹 Clave: `pmh8ootk4d1h`

✅ Ponlo en tu Wi-Fi → entra al FF → sal y desactiva el proxy → vuelve a entrar""", parse_mode="Markdown")
        else:
            bot.reply_to(m, "❌ **CLAVE VENCIDA**\nPide una nueva clave mañana.")
    else:
        bot.reply_to(m, "❌ **CLAVE INCORRECTA**")

print("🤖 BOT INICIADO — Clave válida 24 horas")
bot.infinity_polling()
