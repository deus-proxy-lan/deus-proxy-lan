from mitmproxy import http
import json
import os

ARCHIVO_IPS = "ips_autorizadas.json"
IPS_PERMITIDAS = set()

def cargar_ips():
    global IPS_PERMITIDAS
    if os.path.exists(ARCHIVO_IPS):
        with open(ARCHIVO_IPS, "r") as f:
            IPS_PERMITIDAS = set(json.load(f))

cargar_ips()

def request(flow: http.HTTPFlow):
    ip_usuario = flow.client_conn.address[0]
    cargar_ips()

    if ip_usuario not in IPS_PERMITIDAS:
        flow.response = http.Response.make(
            403,
            b"""<html><body style="background:#000;color:#0f0;text-align:center;padding-top:50px;font-size:22px">
            <h2>❌ IP NO AUTORIZADA</h2>
            <p>Activa tu IP primero con el bot de Telegram</p>
            </body></html>""",
            {"Content-Type": "text/html"}
        )
        return

    if "freefire" in flow.request.pretty_host or "garena" in flow.request.pretty_host:
        flow.response = http.Response.make(
            200,
            b"""<html><body style="background:#001a00;color:#0f0;text-align:center;padding-top:50px;font-size:24px">
            <h2>✅ IP AUTORIZADA ✅</h2>
            <p style="color:#fff">DESACTIVA EL PROXY Y VUELVE A ENTRAR AL FREE FIRE</p>
            <p style="color:#0f0;font-size:18px;margin-top:20px">AIMBOT ACTIVO → PECHO</p>
            </body></html>""",
            {"Content-Type": "text/html"}
        )
        return
