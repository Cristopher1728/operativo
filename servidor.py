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
    "puente_de_huahura": 0
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
        print(f"📄 Lectura: {e}")
    return ESTADO_INICIAL.copy()

def guardar(datos):
    with open(FICHERO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

class ServidorDefinitivo(BaseHTTPRequestHandler):
    def _cab(self, ct="application/json"):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Type", f"{ct};charset=utf-8")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200);self._cab()

    def ruta_pura(self):
        # 🎯 CLAVE: separar ruta pura y tirar parámetros ?t=...
        parte_ruta, _, _ = urllib.parse.urlparse(self.path).path.rstrip("/"), "", ""
        return parte_ruta

    def do_GET(self):
        r = self.ruta_pura()
        if r == "":
            try:
                self.send_response(200)
                self._cab("text/html")
                with open("index.html", "rb") as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_response(404);self._cab();print(f"❌ Sin HTML: {e}")
        elif r == "/datos":
            self.send_response(200);self._cab()
            self.wfile.write(json.dumps(leer(), ensure_ascii=False).encode())
        else:
            print(f"⚠️ Ruta desconocida: {self.path} → limpia: '{r}'")
            self.send_response(404);self._cab()

    def do_POST(self):
        r = self.ruta_pura()
        if r == "/cambiar":
            try:
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n))
                est = leer()
                idp, val = data.get("id"), int(data.get("valor", -1))
                if idp in est and val in (0, 1):
                    est[idp] = val;guardar(est)
                    self.send_response(200);self._cab()
                    self.wfile.write(json.dumps({"ok":True}).encode())
                else:
                    self.send_response(400);self._cab()
            except Exception as e:
                print(f"❌ POST: {e}")
                self.send_response(500);self._cab()

def arrancar(p=8080):
    print("\n✅ HUACHO: SEPARA RUTA DE PARÁMETROS ? — ¡NUNCA FALLA!")
    print(f"📂 {os.getcwd()} | index.html: {'✅'if os.path.exists('index.html')else'❌'}")
    HTTPServer(("0.0.0.0",p),ServidorDefinitivo).serve_forever()

if __name__=="__main__":arrancar()

