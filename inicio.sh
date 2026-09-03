#!/data/data/com.termux/files/usr/bin/bash
clear
# 🚔 HUACHO-TAXI: DIRECCIÓN FIJA + REGISTRO + AUTO-REINTENTO
cd "$HOME/Operativo" || { echo "❌ Carpeta no hallada"; exit 1; }

# ⚙️ CONFIGURACIÓN QUE YA ES NUESTRA:
NOMBRE="huacho-taxi"
CLAVE_SSH="./serveo_clave"
ARCHIVO_LOG="tiempo_tunel.log"

hora_actual() { date "+%Y-%m-%d %H:%M:%S"; }

echo -e "🏁 SISTEMA INICIADO — NOMBRE FIJO: $NOMBRE"
echo "🔑 Identidad: $CLAVE_SSH"
echo "📂 Espacio trabajo: $(pwd)"

# 🔁 BUCLE ETERNO DE ESTABILIDAD
while true; do
  INICIO=$(date +%s)
  echo -e "\n=============================================="
  echo "🚀 CONECTANDO → $(hora_actual)"
  echo "🔗 DOMINIO: $NOMBRE.serveousercontent.com"
  echo "=============================================="

  # 🧹 Mata cualquier cosa vieja suelta
  pkill -f servidor.py 2>/dev/null
  sleep 0.4
  # 🧠 Arranca tu cerebro/tablero
  python servidor.py &
  PID_SERVIDOR=$!
  echo "✅ Servidor activo (PID: $PID_SERVIDOR)"

  # 🌐 CORAZÓN DEL TÚNEL — PIDE Y MANTIENE TU NOMBRE ÚNICO
  ssh -R "$NOMBRE:80:localhost:8080" \
    -i "$CLAVE_SSH" \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=12 \
    -o TCPKeepAlive=yes \
    serveo.net

  # ⏱️ Cuando cae/recorta: MEDICIÓN EXACTA
  FIN=$(date +%s)
  DURACION=$((FIN - INICIO))
  HORAS=$((DURACION / 3600))
  MINUTOS=$(( (DURACION % 3600) / 60 ))
  SEGUNDOS=$((DURACION % 60))

  echo -e "\n⚠️  DESCONEXIÓN / FIN → $(hora_actual)"
  echo "⏱️  TIEMPO CONECTADO: ${HORAS}h ${MINUTOS}m ${SEGUNDOS}s"
  echo "$(hora_actual) | ⏳ Duró: ${HORAS}h:${MINUTOS}m:${SEGUNDOS}s" >> "$ARCHIVO_LOG"

  # 🧼 Limpieza ordenada antes de repetir
  kill $PID_SERVIDOR 2>/dev/null
  echo -e "\n🔁 ESPERA 6 SEGUNDOS PARA VOLVER CON $NOMBRE..."
  sleep 6
done

