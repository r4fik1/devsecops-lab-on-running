import os
import sys
import requests

# 1. CONFIGURACIÓN: Leemos los secretos que acabas de guardar en GitHub
DOJO_URL = os.getenv("DOJO_URL")
API_KEY = os.getenv("DOJO_API_KEY")
# Usamos el Engagement ID 1 por defecto (el primero que crea DefectDojo)
ENGAGEMENT_ID = os.getenv("DOJO_ENGAGEMENT_ID", "1")

if not DOJO_URL or not API_KEY:
    print("❌ Error: Faltan las variables de entorno DOJO_URL o DOJO_API_KEY")
    sys.exit(1)

# 2. FUNCIÓN DE SUBIDA: Envía el archivo a la API
def upload_scan(file_path, scan_type):
    print(f"🚀 Subiendo {file_path} ({scan_type}) a DefectDojo...")
    
    if not os.path.exists(file_path):
        print(f"⚠️ Archivo no encontrado: {file_path}. Saltando.")
        return

    # Endpoint de importación de DefectDojo
    url = f"{DOJO_URL}/api/v2/import-scan/"
    
    headers = {
        "Authorization": f"Token {API_KEY}"
    }
    
    # Datos obligatorios para DefectDojo
    payload = {
        "engagement": ENGAGEMENT_ID,
        "scan_type": scan_type,
        "verified": True,
        "active": True,
        "minimum_severity": "Low"
    }
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        try:
            response = requests.post(url, headers=headers, data=payload, files=files)
            if response.status_code == 201:
                print("✅ Subida exitosa.")
            else:
                print(f"❌ Fallo al subir: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"💥 Error de conexión: {e}")

# 3. MAPEO: Asignamos cada archivo a su tipo de escáner en DefectDojo
# Asegúrate de que estos nombres de archivo coinciden con los que pusiste en el YAML (upload-artifact)
scans = {
    "gitleaks-report.json": "Gitleaks Scan",
    "trivy-report.json": "Trivy Scan",
    "semgrep-report.json": "Semgrep JSON Report",
    "checkov-report.json": "Checkov Scan",
    "trivy-image.json": "Trivy Scan"
}

if __name__ == "__main__":
    print(f"Conectando a: {DOJO_URL}")
    for filename, scanner_name in scans.items():
        upload_scan(filename, scanner_name)