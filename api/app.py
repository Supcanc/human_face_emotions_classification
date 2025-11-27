import torch
from fastapi import FastAPI, HTTPException
from torchvision import models, transforms
import os
from PIL import Image
import uvicorn

app = FastAPI()

MODEL_PATH = 'models/best_model.pth'
CLASSES_NAMES = ['Angry', 'Fear', 'Happy', 'Sad', 'Suprise']
EVAL_TRANSFORMS = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])

device = torch.accelerator.current_accelerator() if torch.accelerator.is_available() else 'cpu'
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, len(CLASSES_NAMES))
model.load_state_dict(torch.load(MODEL_PATH, weights_only=True, map_location=device))
model.to(device)
model.eval()

@app.get("/predict/{images_path:path}")
def predict(images_path:str):
    images = []
    images_names = []
    classes_names = CLASSES_NAMES

    try:
        for image_name in os.listdir(images_path):
            image_path = os.path.join(images_path, image_name)
            image = Image.open(image_path).convert('RGB')
            transformations = EVAL_TRANSFORMS
            image = transformations(image).cpu().detach().tolist()
            images_names.append(image_name)
            images.append(image)

        images = torch.tensor(images).to(device)
        probabilities = torch.softmax(model(images), dim=1).cpu().detach()
        predicted_classes = torch.argmax(probabilities, dim=1).cpu().detach().tolist()

        with open('predictions/predictions.txt', 'w') as f:
            for i in range(len(predicted_classes)):
                f.write(f'{i + 1}) Filename: {images_names[i]}\n'
                        f'Class: {classes_names[predicted_classes[i]]}\n'
                        f'Confidence in prediction: {round(float(probabilities[i, predicted_classes[i]] * 100), 2)}%\n\n')

        return {'status': 'Prediction completed.'}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)