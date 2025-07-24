from app.models import Regional, Programa
from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()
connect(host=os.getenv("MONGODB_URI"))

regionales = ["Cauca", "Huila", "Antioquia", "Cundinamarca", "Atlántico", "Nariño"]
programas = ["Desarrollo de Software", "Textilería", "Sistemas", "Contabilidad", "Mecatrónica", "Gestión Empresarial"]

for nombre in regionales:
    if not Regional.objects(nombre=nombre).first():
        Regional(nombre=nombre).save()

for nombre in programas:
    if not Programa.objects(nombre=nombre).first():
        Programa(nombre=nombre).save()

print("Datos cargados correctamente.")
