#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os

ARCHIVO_ESTADO = "datos_huacho.json"
ESTADO_INICIAL = {
    "universidad": 0,
    "mercedes": 0,
    "plaza_armas": 0,
    "atahualpa": 0,
    "ovalo": 0,
    "veintiocho": 0,
    "plaza_sol": 0,
    "puente": 0
}

def leer_estados():
    try:
        if os.path.exists(ARCHIVO_ESTADO):
            with open(ARCHIVO_ESTADO, "r", encoding="utf-8") as f:
                return {**ESTADO_INICIAL, **json.load(f)}
    except Exception:
        pass
    return ESTADO_INICIAL.copy()

def guardar_estados(datos):
    with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)

class ManejadorCompleto(BaseHTTPRequestHandler):
    def _cabeceras_json(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cabeceras_json()

    def do_GET(self):
        # 🏠 PÁGINA PRINCIPAL: INTEGRA 100%
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            try:
                with open("index.html", "rb") as f:
                    self.wfile.write(f.read())
            except:
                self.send_error(500, "Falta index.html")
            return

        # 📡 ¡ESTA ES LA QUE FALTABA ANTES! RUTA DE DATOS COMPLETA
        if self.path.startswith("/datos"):
            self.send_response(200)
            self._cabeceras_json()
            self.wfile.write(json.dumps(leer_estados()).encode("utf-8"))
            return

        # 🧹 ICONO INEXISTENTE: NO LLENAR PANTALLA DE BASURA
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # ❓ CUALQUIER OTRA COSA: ERROR LIMPIO
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        # ✍️ RUTA PARA RECIBIR CAMBIOS — IGUAL DE COMPLETA
        if self.path == "/cambiar":
            try:
                largo = int(self.headers.get("Content-Length", 0))
                cuerpo = self.rfile.read(largo)
                datos_recibidos = json.loads(cuerpo)
                estado = leer_estados()
                clave = datos_recibidos.get("id")
                valor = int(datos_recibidos.get("valor", 0))
                if clave in estado:
                    estado[clave] = valor
                    guardar_estados(estado)
                    self.send_response(200)
                    self._cabeceras_json()
                    self.wfile.write(json.dumps({"ok":True}).encode())
                else:
                    self.send_response(400)
                    self._cabeceras_json()
            except Exception:
                self.send_response(500)
                self._cabeceras_json()

def arrancar(puerto=8080):
    print("\n🚔 SERVIDOR HUACHO: ✅ RUTAS /datos y /cambiar EXISTEN / COMPLETO / SIN CORTES")
    print(f"📂 Carpeta: {os.getcwd()}")
    print(f"📄 Index: {'✅ PRESENTE' if os.path.exists('index.html') else '❌ FALTA'}\n")
    HTTPServer(("0.0.0.0", puerto), ManejadorCompleto).serve_forever()

arrancar()

