import telebot
from datetime import datetime, timedelta, timezone
import json
import os

# 📌 CONFIGURACIÓN DEL BOT
TOKEN_BOT = "8750716094:AAF29inoucagFHOHobkX1vMknVeL_bIL4o8"
CLAVE_VIP = "NKGVIPDEUS"
ARCHIVO_IPS = "ips_autorizadas.json"
ARCHIVO_CLAVES = "claves_vip.json"

# Hora dominicana = UTC-4
HORA_DOM = timezone(timedelta(hours=-4))

# Fecha de vencimiento: 16 de octubre de 2026 a las 17:00 hora dominicana
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

🔑 Usa este comando para activar:
`/activar NKGVIPDEUS TU_IP`

📅 Esta clave vence el:
**16 de octubre de 2026 a las 5:00 PM**
*Hora Oficial Dominicana (UTC-4)*

Ejemplo: `/activar NKGVIPDEUS 64.32.106.75`"""
    bot.reply_to(mensaje, texto, parse_mode="Markdown")

@bot.message_handler(commands=['activar'])
def activar_clave(mensaje):
    partes = mensaje.text.strip().split()
    if len(partes) < 3:
        bot.reply_to(mensaje, "❌ Formato incorrecto.\nUsa: `/activar NKGVIPDEUS TU_IP`", parse_mode="Markdown")
        return
    clave = partes[1].strip().upper()
    ip = partes[2].strip()
    ips, claves = cargar_datos()

    if clave == CLAVE_VIP:
        ahora = datetime.now(HORA_DOM)
        if ahora < FECHA_FIN:
            claves[clave] = FECHA_FIN.isoformat()
            ips.add(ip)
            guardar_datos(ips, claves)
            tiempo_restante = FECHA_FIN - ahora
            dias = tiempo_restante.days
            horas = tiempo_restante.seconds // 3600
            minutos = (tiempo_restante.seconds % 3600) // 60

            respuesta = f"""✅ **ACTIVADO CON ÉXITO** ✅

🔑 Clave: `{clave}`
🌐 Tu IP autorizada: `{ip}`

📅 Vence el: **16 de octubre de 2026 a las 5:00 PM**
⏱️ Tiempo restante: **{dias} días, {horas} horas y {minutos} minutos**

📝 Datos para tu proxy:
🔹 Servidor: `deus-proxy-lan-1.onrender.com`
🔹 Puerto: `8080`
🔹 Usuario: `ARIFI`
🔹 Clave: `ARIFI`"""
            bot.reply_to(mensaje, respuesta, parse_mode="Markdown")
        else:
            bot.reply_to(mensaje, "❌ **CLAVE VENCIDA**\nPide una nueva clave al administrador.")
    else:
        bot.reply_to(mensaje, "❌ **CLAVE INVÁLIDA**\nRevisa que la escribas bien: `NKGVIPDEUS`")

print("🤖 BOT INICIADO CORRECTAMENTE")
bot.infinity_polling()
