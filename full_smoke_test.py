import time
import torch
import timm
import torch.nn as nn
from PIL import Image
from torchvision import transforms
import numpy as np
import os
import json
from datetime import datetime

class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

class CustomSwinTransformer(nn.Module):
    def __init__(self, pretrained=False, num_classes=7):
        super().__init__()
        self.backbone = timm.create_model('swin_base_patch4_window7_224', pretrained=False, num_classes=0)
        self.classifier = nn.Linear(self.backbone.num_features, num_classes)
    def forward(self, x):
        x = self.backbone(x)
        x = self.classifier(x)
        return x

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

def compute_mental_health_scores(probs):
    idx_happy = class_names.index('Happy')
    idx_neutral = class_names.index('Neutral')
    idx_sad = class_names.index('Sad')
    happy_score = float(probs[idx_happy]) * 100
    neutral_score = float(probs[idx_neutral]) * 100
    sad_score = float(probs[idx_sad]) * 100
    anxiety = max(0, (100 - happy_score) * 0.3 + sad_score * 0.4)
    depression = max(0, sad_score * 0.6 + (100 - happy_score) * 0.2)
    stress = max(0, (100 - neutral_score) * 0.4 + sad_score * 0.3)
    return {
        'Anxiety': round(anxiety, 1),
        'Depression': round(depression, 1),
        'Stress': round(stress, 1)
    }

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('Device:', device)
    model = CustomSwinTransformer(pretrained=False, num_classes=len(class_names))
    model_path = 'best_model.pth'
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
    else:
        print('Model weights not found:', model_path)
    model = model.to(device).eval()

    img_path = 'test_face.jpg'
    if not os.path.exists(img_path):
        print('Test image not found:', img_path)
        return

    img = Image.open(img_path).convert('RGB')
    t = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        t0 = time.time()
        out = model(t)
        dt = time.time() - t0
        probs = torch.softmax(out, dim=1).cpu().numpy()[0]
        pred = int(np.argmax(probs))

    print('Inference time: %.3fs' % dt)
    print('Top probs:')
    for i in np.argsort(probs)[::-1][:5]:
        print(f"  {class_names[i]}: {probs[i]:.4f}")

    scores = compute_mental_health_scores(probs)
    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'source': 'Image (smoke_test)',
        'primary_emotion': class_names[pred],
        'probabilities': {class_names[i]: float(probs[i]) for i in range(len(class_names))},
        'scores': scores
    }

    out_dir = 'smoke_outputs'
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
    with open(json_path, 'w', encoding='utf8') as f:
        json.dump(report, f, indent=2)
    print('Wrote JSON report to', json_path)

    # Optional PDF
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from io import BytesIO
        pdf_path = os.path.join(out_dir, f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf")
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        c.setFont('Helvetica-Bold', 14)
        c.drawString(40, height-60, 'FERMH - Facial Expression Report (smoke test)')
        c.setFont('Helvetica', 10)
        c.drawString(40, height-80, f"Timestamp: {report['timestamp']}")
        c.drawString(40, height-100, f"Source: {report['source']}")
        c.drawString(40, height-120, f"Primary emotion: {report['primary_emotion']}")
        c.drawString(40, height-140, 'Scores:')
        y = height-160
        for k, v in report['scores'].items():
            c.drawString(56, y, f"{k}: {v}%")
            y -= 16
        c.drawString(40, y-6, 'Probabilities:')
        y -= 26
        for k, v in report['probabilities'].items():
            c.drawString(56, y, f"{k}: {v:.3f}")
            y -= 14
            if y < 60:
                c.showPage(); y = height-60
        c.showPage(); c.save()
        buffer.seek(0)
        with open(pdf_path, 'wb') as pf:
            pf.write(buffer.read())
        print('Wrote PDF report to', pdf_path)
    except Exception as e:
        print('PDF generation not available:', e)

if __name__ == '__main__':
    main()
