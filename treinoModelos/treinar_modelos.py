
from ultralytics import YOLO
import os

# Caminhos relativos aos datasets
datasets = {
    "modeloSemDataAugmentation": "modeloSemDataAugmentation/data.yaml",
    "modeloComDataAugmentation90Grau": "modeloComDataAugmentation90Grau/data.yaml"
}

# Nome do modelo base
modelo_base = "yolov8n.pt"

# Parâmetros de treino
EPOCHS = 100
IMG_SIZE = 640

for nome, caminho_yaml in datasets.items():
    print(f"🔧 A treinar modelo: {nome}")
    
    if not os.path.exists(caminho_yaml):
        print(f"❌ Ficheiro não encontrado: {caminho_yaml}")
        continue

    modelo = YOLO(modelo_base)
    modelo.train(
        data=caminho_yaml,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        project="runs",
        name=nome,
        exist_ok=True
    )

print("✅ Treino completo!")
