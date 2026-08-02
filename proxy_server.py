from mitmproxy import http
import json
import os
from datetime import datetime, timedelta, timezone

# 📌 CONFIGURACIÓN GENERAL
USUARIO_VALIDO = "ARIFI"
CLAVE_VALIDA = "ARIFI"
PUERTO = 8080
ARCHIVO_IPS = "ips_autorizadas.json"
ARCHIVO_CLAVES = "claves_vip.json"

# Zona horaria: Hora dominicana = UTC-4
HORA_DOM = timezone(timedelta(hours=-4))

# Cargar datos guardados
ips_autorizadas = set()
claves_vip = {}

def cargar_datos():
    global ips_autorizadas, claves_vip
    if os.path.exists(ARCHIVO_IPS):
        try:
            with open(ARCHIVO_IPS, "r") as f:
                ips_autorizadas = set(json.load(f))
        except:
            ips_autorizadas = set()
    if os.path.exists(ARCHIVO_CLAVES):
        try:
            with open(ARCHIVO_CLAVES, "r") as f:
                claves_vip = json.load(f)
        except:
            claves_vip = {}

def guardar_datos():
    with open(ARCHIVO_IPS, "w") as f:
        json.dump(list(ips_autorizadas), f)
    with open(ARCHIVO_CLAVES, "w") as f:
        json.dump(claves_vip, f)

def validar_clave(clave_ingresada):
    clave_ingresada = clave_ingresada.strip().upper()
    if clave_ingresada in claves_vip:
        fecha_fin = datetime.fromisoformat(claves_vip[clave_ingresada]).replace(tzinfo=HORA_DOM)
        ahora = datetime.now(HORA_DOM)
        if ahora < fecha_fin:
            return True, fecha_fin
        else:
            return False, fecha_fin
    return False, None

cargar_datos()

def request(flow: http.HTTPFlow) -> None:
    ip_usuario = flow.client_conn.address[0]

    # Verificar credenciales de proxy
    auth = flow.request.headers.get("Proxy-Authorization", "")
    if not auth.startswith("Basic "):
        flow.response = http.Response.make(407, b"", {"Proxy-Authenticate": 'Basic realm="DEUS MOODZ VIP"'})
        return

    # Verificar IP autorizada
    if ip_usuario not in ips_autorizadas:
        html_rojo = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif}}
        body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#000;color:#fff}}
        .caja{{padding:50px 30px;border:3px solid #ff3333;border-radius:20px;box-shadow:0 0 30px #ff333380;text-align:center;max-width:400px}}
        h1{{font-size:32px;margin-bottom:20px;color:#ff3333}}
        .ip{{font-size:22px;margin-bottom:25px;color:#ff6666}}
        .msg{{font-size:18px;line-height:1.6}}
    </style>
</head>
<body>
    <div class="caja">
        <h1>⚠️ IP NO AUTORIZADA</h1>
        <div class="ip">TU IP: {ip_usuario}</div>
        <div class="msg">Usa el bot de Telegram para activar tu clave VIP.</div>
    </div>
</body>
</html>"""
        flow.response = http.Response.make(403, html_rojo.encode("utf-8"), {"Content-Type": "text/html; charset=utf-8"})
        return

    # Mensaje de activación en Free Fire
    if "ff.garena.com" in flow.request.pretty_url:
        html_verde = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif}}
        body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#000;color:#fff}}
        .caja{{padding:50px 30px;border:3px solid #00ff88;border-radius:20px;box-shadow:0 0 30px #00ff8880;text-align:center;max-width:400px}}
        h1{{font-size:32px;margin-bottom:20px;color:#00ff88}}
        .ip{{font-size:22px;margin-bottom:25px;color:#88ffcc}}
        .msg{{font-size:18px;line-height:1.6}}
    </style>
</head>
<body>
    <div class="caja">
        <h1>✅ ACTIVADO CON EXITO</h1>
        <div class="ip">DEUS MOODZ VIP</div>
        <div class="msg">Desactiva el proxy y entra al Free Fire.</div>
    </div>
</body>
</html>"""
        flow.response = http.Response.make(200, html_verde.encode("utf-8"), {"Content-Type": "text/html; charset=utf-8"})

print(f"✅ SERVIDOR LISTO | PUERTO {PUERTO} | USUARIO {USUARIO_VALIDO}")