#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, urllib.parse

FICHERO_ESTADO = "datos_huacho.json"
ESTADO_INICIAL = {
    "universidad_jfsc": 0,
    "colegio_indacochea": 0,
    "colegio_20318": 0,
    "hospital_regional": 0,
    "plaza_de_armas": 0,
    "atahualpa_adan_acevedo": 0,
    "plazuela_san_martin": 0,
    "plaza_del_sol": 0,
    "av_grau": 0,
    "bcp_ex_carsa": 0,
    "estadio_de_huacho": 0,
    "ovalo_de_huacho": 0,
    "restaurante_pascual": 0,
    "puente_de_huahura": 0,
}

def leer():
    try:
        if os.path.exists(FICHERO_ESTADO):
            with open(FICHERO_ESTADO, "r", encoding="utf-8") as f:
                viejo = json.load(f)
                nuevo = dict(ESTADO_INICIAL)
                for k in nuevo:
                    if k in viejo:
                        nuevo[k] = viejo[k]
                return nuevo
    except Exception as e:
        print(f"📖 Lectura: {e}")
    return ESTADO_INICIAL.copy()

def guardar(datos):
    with open(FICHERO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

class ServidorDefinitivo(BaseHTTPRequestHandler):
    def _cabecera(self, ct="application/json"):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Type", f"{ct};charset=utf-8")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cabecera()

    def ruta_pura(self):
        parte_ruta, _, _ = urllib.parse.urlparse(self.path).path.rstrip("/").partition("?")
        return parte_ruta

    # ✅ SERVIR CUALQUIER ARCHIVO HTML/CSS/JS/IMAGEN
    def servir_archivo(self, ruta):
        if ruta == "" or ruta == "/":
            ruta = "/index.html"
        archivo = ruta.lstrip("/")
        if os.path.exists(archivo) and os.path.isfile(archivo):
            ext = os.path.splitext(archivo)[1].lower()
            tipos = {
                ".html": "text/html",
                ".css": "text/css",
                ".js": "application/javascript",
                ".json": "application/json",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".svg": "image/svg+xml",
            }
            ct = tipos.get(ext, "application/octet-stream")
            try:
                with open(archivo, "rb") as f:
                    self.send_response(200)
                    self._cabecera(ct)
                    self.wfile.write(f.read())
                return True
            except:
                pass
        return False

    def do_GET(self):
        r = self.ruta_pura()
        # 📄 Servir archivos estáticos (index.html, velocidad.html, etc.)
        if self.servir_archivo(r):
            return
        # 📊 Datos del estado
        if r == "/datos":
            self.send_response(200)
            self._cabecera()
            self.wfile.write(json.dumps(leer(), ensure_ascii=False).encode())
            return
        # ❌ No encontrado
        print(f"⚠️ Ruta desconocida: {self.path}")
        self.send_response(404)
        self._cabecera("text/html")
        self.wfile.write(b"<h1>404 - No encontrado</h1>")

    def do_POST(self):
        r = self.ruta_pura()
        if r == "/cambiar":
            try:
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n))
                est = leer()
                idp = data.get("id")
                val = int(data.get("valor", -1))
                if idp in est and val in (0, 1):
                    est[idp] = val
                    guardar(est)
                    self.send_response(200)
                    self._cabecera()
                    self.wfile.write(json.dumps({"ok": True}).encode())
                    return
                self.send_response(400)
                self._cabecera()
            except Exception as e:
                print(f"❌ POST: {e}")
                self.send_response(500)
                self._cabecera()
            return
        self.send_response(404)
        self._cabecera()

def arrancar(p=8080):
    print("\n✅ HUACHO: SERVIDOR COMPLETO — ¡SIRVE TODOS LOS ARCHIVOS!")
    print(f"📂 Carpeta: {os.getcwd()}")
    archivos = [f for f in os.listdir(".") if f.endswith(".html")]
    print(f"📄 Archivos HTML disponibles: {', '.join(archivos)}")
    print(f"🌐 Principal: https://huacho-taxi.serveousercontent.com/")
    print(f"🚗 Velocímetro: https://huacho-taxi.serveousercontent.com/velocidad.html")
    print("-" * 60)
    HTTPServer(("0.0.0.0", p), ServidorDefinitivo).serve_forever()

if __name__ == "__main__":
    arrancar()

