import telebot
from datetime import datetime, timedelta, timezone
import json
import os

# 🔑 DATOS PRINCIPALES
TOKEN_BOT = "8750716094:AAF29inoucagFHOHobkX1vMknVeL_bIL4o8"
CLAVE_VIP = "NKGVIPDEUS"
CLAVE_PERSONAL = "CHEK"
MAX_TOTAL = 1000       # ⛔ LÍMITE MÁXIMO
MAX_POR_CLAVE = 1000       # ⛔ UNA SOLA IP POR PERSONA

# ⏳ HORA REP. DOMINICANA
HORA_DOM = timezone(timedelta(hours=-4))
FECHA_FIN = datetime.now(HORA_DOM) + timedelta(days=1)

# 🤫 TU COMANDO SECRETO — CÁMBIALO POR EL QUE TÚ QUIERAS
COMANDO_SECRETO = "/list"

# 📋 DATOS DEL PROXY
IP_PROXY = "198.23.243.226"
PUERTO_PROXY = "6361"
USUARIO_PROXY = "Giduqmqn"
CLAVE_PROXY = "pmh8ootk4d1h"

# 📄 TU ENLACE DEL CERTIFICADO
ENLACE_CERT = "https://www.mediafire.com/file/bbk2hqgc8na9vjx/Proxy+🔋.pem/file"

ARCHIVO = "datos_sistema.json"
SISTEMA_BLOQUEADO = False

bot = telebot.TeleBot(TOKEN_BOT)

def cargar():
    global SISTEMA_BLOQUEADO
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            d = json.load(f)
            SISTEMA_BLOQUEADO = d.get("bloqueado", False)
            return d.get("por_clave", {}), d.get("bloqueado", False)
    return {}, False

def guardar(por_clave, bloqueado=False):
    global SISTEMA_BLOQUEADO
    SISTEMA_BLOQUEADO = bloqueado
    with open(ARCHIVO, "w") as f:
        json.dump({"por_clave": por_clave, "bloqueado": bloqueado}, f)

def contar_total(por_clave):
    total = 0
    for ips in por_clave.values():
        total += len(ips)
    return total

@bot.message_handler(commands=['start'])
def inicio(m):
    por_clave, _ = cargar()
    total = contar_total(por_clave)
    bot.reply_to(m, f"""👋 **DEUS MOODZ — PANEL PROXY VIP**

📊 ACTIVOS: `{total} de {MAX_TOTAL}`
🔑 Usa: `/activar TU_CLAVE TU_IP`
⏳ Clave vence: {FECHA_FIN.strftime('%d/%m a las 12:53 PM')}

🗑️ Para quitar tu IP: `/remover_mi_ip TU_CLAVE`
""", parse_mode="Markdown")

@bot.message_handler(commands=['activar'])
def activar(m):
    por_clave, bloqueado = cargar()
    ahora = datetime.now(HORA_DOM)
    total = contar_total(por_clave)

    if bloqueado:
        bot.reply_to(m, "❌ **SISTEMA TEMPORALMENTE DESACTIVADO**\nVuelve más tarde.")
        return

    if ahora >= FECHA_FIN:
        bot.reply_to(m, "❌ **CLAVE VENCIDA**\nPide una nueva clave.")
        return

    if total >= MAX_TOTAL:
        bot.reply_to(m, f"❌ **LÍMITE ALCANZADO**\n{MAX_TOTAL} usuarios activos. Espera a que se liberen.")
        return

    partes = m.text.strip().split()
    if len(partes) < 3:
        bot.reply_to(m, "❌ Usa: `/activar TU_CLAVE TU_IP`", parse_mode="Markdown")
        return

    clave = partes[1].strip().upper()
    ip = partes[2].strip()

    if clave != CLAVE_VIP:
        bot.reply_to(m, "❌ **CLAVE INCORRECTA**")
        return

    ips_usuario = por_clave.get(clave, [])

    if len(ips_usuario) >= MAX_POR_CLAVE:
        bot.reply_to(m, f"""⚠️ **YA TIENES UNA IP ACTIVA**

Tu IP: `{ips_usuario[0]}`

🗑️ Quítala primero con: `/remover_mi_ip TU_CLAVE`""", parse_mode="Markdown")
        return

    ips_usuario.append(ip)
    por_clave[clave] = ips_usuario
    guardar(por_clave)
    total_nuevo = contar_total(por_clave)

    bot.reply_to(m, f"""✅ **ACTIVADO CON ÉXITO ✅**

📊 ACTIVOS: `{total_nuevo} de {MAX_TOTAL}`

🌐 IP: `{IP_PROXY}`
🚪 PUERTO: `{PUERTO_PROXY}`
👤 USUARIO: `{USUARIO_PROXY}`
🔑 CONTRASEÑA: `{CLAVE_PROXY}`

📄 **CERTIFICADO:**
{ENLACE_CERT}

🗑️ Tu IP registrada: `{ip}`
Para quitarla: `/remover_mi_ip TU_CLAVE`

✅ Instala certificado → pon datos en Wi-Fi → entra FF → sal y desactiva proxy → entra de nuevo""", parse_mode="Markdown", disable_web_page_preview=False)

@bot.message_handler(commands=['remover_mi_ip'])
def remover_mia(m):
    por_clave, _ = cargar()
    partes = m.text.strip().split()
    if len(partes) < 2:
        bot.reply_to(m, "❌ Usa: `/remover_mi_ip TU_CLAVE`", parse_mode="Markdown")
        return

    clave = partes[1].strip().upper()
    if clave not in por_clave or len(por_clave[clave]) == 0:
        bot.reply_to(m, "⚠️ No tienes IPs registradas con esa clave.")
        return

    del por_clave[clave]
    guardar(por_clave)
    total = contar_total(por_clave)

    bot.reply_to(m, f"""🗑️ **IP ELIMINADA CORRECTAMENTE ✅**

📊 ACTIVOS AHORA: `{total} de {MAX_TOTAL}`

✅ Ya puedes activar una IP nueva cuando quieras.""", parse_mode="Markdown")

@bot.message_handler(commands=[COMANDO_SECRETO.replace("/","")])
def borrar_todo(m):
    por_clave, _ = cargar()
    cantidad = contar_total(por_clave)
    guardar({}, bloqueado=True)

    bot.reply_to(m, f"""⚠️ **COMANDO DE ADMINISTRADOR — BORRAR TODO**

✅ Se eliminaron **{cantidad} IPs** del sistema.
✅ Contador vuelve a: `0 de {MAX_TOTAL}`
❌ SISTEMA BLOQUEADO — Nadie puede activar hasta que tú lo desbloquees.

🔓 Para desbloquear: cambia `bloqueado=True` a `False` en el código y sube los cambios.""", parse_mode="Markdown")

print("🤖 BOT INICIADO — Activos: 0 de 1000 — Vence:", FECHA_FIN.strftime('%d/%m %H:%M'))
# ✅ ESTO HACE QUE RENDER DETECTE QUE ESTÁ VIVO
from flask import Flask
app = Flask(__name__)

@app.route('/')
def estoy_vivo():
    return "✅ DEUS MOODZ — BOT VIVO"

def arrancar_web():
    app.run(host="0.0.0.0", port=8080)

import threading
threading.Thread(target=arrancar_web, daemon=True).start()

print("✅ BOT VIVO Y LISTO")
@bot.message_handler(commands=['deus_contar'])
def contar_activos(m):
    por_clave, _ = cargar()
    total = contar_total(por_clave)
    bot.reply_to(m, f"""📊 **TOTAL DE IPs ACTIVAS:** `{total}` de `{MAX_TOTAL}`

🔑 Claves en uso: `{len(por_clave)}`
✅ Todo funcionando correctamente""", parse_mode="Markdown")
bot.delete_webhook()
bot.infinity_polling()
