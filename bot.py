import telebot
from datetime import datetime, timedelta, timezone
import json
import os

# 📌 CONFIGURACIÓN DEL BOT
TOKEN_BOT = "8786825072:AAFHMSDZ_i8Mdpm5d1MYbBKDZUvULZoQfyQ"
CLAVE_VIP = "NKGVIPDEUS"
ARCHIVO_IPS = "ips_autorizadas.json"
ARCHIVO_CLAVES = "claves_vip.json"

# Hora dominicana = UTC-4
HORA_DOM = timezone(timedelta(hours=-4))

# Fecha de vencimiento: ejemplo → 16 de octubre de 2026 a las 17:00 hora dominicana
FECHA_FIN = datetime(2026, 10, 16, 17, 0, 0, tzinfo=HORA_DOM)

bot = telebot.TeleBot(TOKEN_BOT)

def cargar_datos():
    if os.path.exists(ARCHIVO_IPS):
        with open(ARCHIVO_IPS, "r") as f:
            ips = set(json.load(f))
    else:
        ips = set()
    if os.path.exists(ARCHIVO_CLAVES):
        with open(ARCHIVO_CLAVES, "r") as f:
            claves = json.load(f)
    else:
        claves = {}
    return ips, claves

def guardar_datos(ips, claves):
    with open(ARCHIVO_IPS, "w") as f:
        json.dump(list(ips), f)
    with open(ARCHIVO_CLAVES, "w") as f:
        json.dump(claves, f)

@bot.message_handler(commands=['start'])
def bienvenida(mensaje):
    texto = """👋 Bienvenido a **DEUS MOODZ VIP** 🇩🇴

🔑 Escribe tu clave VIP para activar:
`NKGVIPDEUS`

📅 Esta clave vence el:
**16 de octubre de 2026 a las 5:00 PM**
*Hora Oficial Dominicana (UTC-4)*

Escribe tu clave para continuar."""
    bot.reply_to(mensaje, texto, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def verificar_clave(mensaje):
    clave = mensaje.text.strip().upper()
    ips, claves = cargar_datos()

    if clave == CLAVE_VIP:
        ahora = datetime.now(HORA_DOM)
        if ahora < FECHA_FIN:
            claves[clave] = FECHA_FIN.isoformat()
            guardar_datos(ips, claves)
            tiempo_restante = FECHA_FIN - ahora
            dias = tiempo_restante.days
            horas = tiempo_restante.seconds // 3600
            minutos = (tiempo_restante.seconds % 3600) // 60

            respuesta = f"""✅ **CLAVE CORRECTA** ✅

📅 Vence el: **16 de octubre de 2026 a las 5:00 PM**
⏱️ Tiempo restante: **{dias} días, {horas} horas y {minutos} minutos**

📝 Envía ahora tu IP para autorizarla:
Ejemplo: `64.233.12.45`"""
            bot.reply_to(mensaje, respuesta, parse_mode="Markdown")

            # Pasamos a esperar la IP
            bot.register_next_step_handler(mensaje, autorizar_ip)
        else:
            bot.reply_to(mensaje, "❌ **CLAVE VENCIDA**\nPide una nueva clave a tu administrador.")
    else:
        bot.reply_to(mensaje, "❌ **CLAVE INCORRECTA**\nRevisa que la hayas escrito bien.")

def autorizar_ip(mensaje):
    ip = mensaje.text.strip()
    ips, claves = cargar_datos()
    ips.add(ip)
    guardar_datos(ips, claves)

    respuesta = f"""✅ **IP AUTORIZADA** ✅

Tu IP: `{ip}`
Ya puedes usar tu proxy:
🔹 **Servidor:** Tu dirección de Render
🔹 **Puerto:** 8080
🔹 **Usuario:** ARIFI
🔹 **Clave:** ARIFI

📌 Recuerda: Desactiva el proxy antes de entrar al juego."""
    bot.reply_to(mensaje, respuesta, parse_mode="Markdown")

print("🤖 BOT INICIADO CORRECTAMENTE")
bot.infinity_polling()