import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# 🚨 FALLO 1: Secreto Hardcodeado (Cebo para Gitleaks)
AWS_ACCESS_KEY = "AKIA1234567890FAKEKEY" 
DB_PASSWORD = "password123"

@app.route('/')
def home():
    return "Welcome to the Golden Path Lab!"

@app.route('/ping')
def ping():
    # 🚨 FALLO 2: Inyección de Comandos (Cebo para SAST/Semgrep)
    address = request.args.get('address')
    cmd = "ping -c 1 " + address
    subprocess.call(cmd, shell=True)
    return "Pinging..."

if __name__ == '__main__':
    app.run(debug=True)