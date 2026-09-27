import time
import torch
import timm
import torch.nn as nn
from PIL import Image
from torchvision import transforms
import numpy as np

class CustomSwinTransformer(nn.Module):
    def __init__(self, pretrained=False, num_classes=7):
        super().__init__()
        self.backbone = timm.create_model('swin_base_patch4_window7_224', pretrained=False, num_classes=0)
        self.classifier = nn.Linear(self.backbone.num_features, num_classes)
    def forward(self, x):
        x = self.backbone(x)
        x = self.classifier(x)
        return x

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Device:', device)
model = CustomSwinTransformer(pretrained=False, num_classes=7)
try:
    t0 = time.time()
    model.load_state_dict(torch.load('best_model.pth', map_location=device))
    model = model.to(device).eval()
    print('Model loaded in', round(time.time()-t0,2), 's')

    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
    ])
    img = Image.open('test_face.jpg').convert('RGB')
    t = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        t0 = time.time()
        out = model(t)
        probs = torch.softmax(out, dim=1).cpu().numpy()[0]
        dt = time.time()-t0
    idxs = np.argsort(probs)[::-1]
    print('Inference time: %.3fs' % dt)
    for i in idxs[:5]:
        print(f"{i}: {probs[i]:.4f}")
    print('probs sum', probs.sum())
except Exception as e:
    print('Error during smoke inference:', e)
