# 🚨 FALLO: Imagen base antigua con muchas vulnerabilidades
FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# 🚨 FALLO: No definimos USER, por lo que corre como ROOT
# 🚨 FALLO: Exponemos puerto pero no lo usamos bien
EXPOSE 5000

CMD ["python", "src/app.py"]