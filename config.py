from torchvision import transforms

MODEL_PATH = '../models/best_model.pth'
CLASSES_NAMES = ['Angry', 'Fear', 'Happy', 'Sad', 'Suprise']
EVAL_TRANSFORMS = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])