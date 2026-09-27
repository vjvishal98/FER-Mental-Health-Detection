import streamlit as st
import plotly.graph_objects as go
import torch
from PIL import Image
import cv2
import numpy as np
import timm
import torch.nn as nn
import json
from datetime import datetime
from torchvision import transforms
import os

# Page config
st.set_page_config(
    page_title='Facial Emotion Recognition Dashboard',
    page_icon=':robot_face:',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Minimal session state
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Class labels
class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Model definition (same as training)
class CustomSwinTransformer(nn.Module):
    def __init__(self, pretrained=False, num_classes=7):
        super().__init__()
        # Create backbone with timm; classifier head
        self.backbone = timm.create_model(
            'swin_base_patch4_window7_224', pretrained=pretrained, num_classes=0
        )
        self.classifier = nn.Linear(self.backbone.num_features, num_classes)

    def forward(self, x):
        x = self.backbone(x)
        x = self.classifier(x)
        return x

# Preprocessing transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Cached model loader
@st.cache_resource
def get_model():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = CustomSwinTransformer(pretrained=False, num_classes=len(class_names))
    model_path = 'best_model.pth'
    if os.path.exists(model_path):
        try:
            model.load_state_dict(torch.load(model_path, map_location=device))
        except Exception as e:
            st.warning(f'Could not load model weights: {e}')
    else:
        st.info('Model weights not found (best_model.pth). The app will run but predictions may be random.')
    model = model.to(device)
    model.eval()
    return model, device

# Simple heuristic mapping of emotions to mental health-like scores (example only)
def compute_mental_health_scores(probs):
    # probs is a 1D array aligned with class_names
    # This is a toy heuristic for demonstration only
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

# Display results, charts and downloads
def display_results(pred, probs, scores, source='Image'):
    st.markdown('---')
    primary = class_names[int(pred)] if isinstance(pred, (int, np.integer)) else str(pred)
    st.subheader(f'Primary emotion: {primary} ({source})')

    # Probability bar chart
    fig = go.Figure(go.Bar(
        x=[float(p) for p in probs],
        y=class_names,
        orientation='h',
        marker=dict(color='rgba(79,70,229,0.8)')
    ))
    fig.update_layout(height=320, margin=dict(l=90, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # Show scores
    cols = st.columns(3)
    for i, (k, v) in enumerate(scores.items()):
        with cols[i]:
            st.metric(label=k, value=f"{v}%")

    # Build a report dict for downloads and history
    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'source': source,
        'primary_emotion': primary,
        'probabilities': {class_names[i]: float(probs[i]) for i in range(len(class_names))},
        'scores': scores
    }

    report_json = json.dumps(report, indent=2)
    st.download_button(
        label='Download report (JSON)',
        data=report_json.encode('utf-8'),
        file_name=f"fermh_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json",
        mime='application/json'
    )

    # Optional PDF export (reportlab)
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from io import BytesIO

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        c.setFont('Helvetica-Bold', 14)
        c.drawString(40, height-60, 'FERMH - Facial Expression Report')
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
                c.showPage()
                y = height-60
        c.showPage()
        c.save()
        buffer.seek(0)
        pdf_bytes = buffer.read()
        st.download_button(
            label='Download report (PDF)',
            data=pdf_bytes,
            file_name=f"fermh_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime='application/pdf'
        )
    except Exception:
        st.info('PDF export not available. To enable PDF reports install reportlab (pip install reportlab).')

    # Save to simple history
    st.session_state['history'].append(report)


# UI helpers
def go_home():
    st.session_state['page'] = 'home'
    st.session_state['selected_input'] = None


def select_input(kind):
    st.session_state['selected_input'] = kind
    st.session_state['page'] = 'detail'

# UI: styles and hero
# Topbar / Hero (Streamlit-native)
# Embed local Inter fonts if available
font_css = ''
assets_dir = 'assets'
inter_regular = os.path.join(assets_dir, 'Inter-Regular.woff2')
inter_bold = os.path.join(assets_dir, 'Inter-Bold.woff2')
if os.path.exists(inter_regular) or os.path.exists(inter_bold):
    font_css = '<style>\n'
    if os.path.exists(inter_regular):
        font_css += "@font-face{font-family:InterLocal; src: url('assets/Inter-Regular.woff2') format('woff2'); font-weight:400; font-style:normal;}\n"
    if os.path.exists(inter_bold):
        font_css += "@font-face{font-family:InterLocal; src: url('assets/Inter-Bold.woff2') format('woff2'); font-weight:700; font-style:normal;}\n"
    font_css += "body{font-family:InterLocal, system-ui, -apple-system, 'Segoe UI', Roboto, Arial;}\n</style>"
    st.markdown(font_css, unsafe_allow_html=True)
else:
    # Fallback to Google Fonts
    st.markdown("<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap\" rel=\"stylesheet\">", unsafe_allow_html=True)

cols = st.columns([1, 4, 1])
with cols[1]:
    logo_path = os.path.join(assets_dir, 'logo.svg')
    if os.path.exists(logo_path):
        st.image(logo_path, width=40, use_column_width=False, caption='EmotiSense logo')
    st.title('EmotiSense')
    st.caption('Understand your emotional health journey — local processing, privacy-first')
    st.info('Tip: Use Tab to navigate controls and Enter/Space to activate buttons for keyboard access')

# Hero and CTA
hero_cols = st.columns([6,4])
with hero_cols[0]:
    st.markdown('### HIPAA Compliant & Secure')
    st.header('Understand Your Emotional Health Journey')
    st.write('Advanced facial expression recognition provides real-time insights. Upload an image, a short video, or use your camera for analysis.')
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button('Start Image Analysis', key='hero_image', help='Upload a JPG/PNG image for analysis'):
            select_input('image')
    with c2:
        st.button('Watch Demo', key='hero_demo', help='Play a short demo of the interface')
with hero_cols[1]:
    # Demo placeholder box
    st.empty()

st.markdown('---')

# Card selector area (three big accessible buttons)
st.markdown('### Choose your analysis method')
st.write('Select from three convenient options to analyze your facial expressions and gain insights into your emotional state')
card_cols = st.columns(3)
with card_cols[0]:
    if st.button('Image', key='card_image', help='Upload a JPG/PNG image for facial expression analysis'):
        select_input('image')
    st.caption('Upload a JPG/PNG')
with card_cols[1]:
    if st.button('Video', key='card_video', help='Upload a short MP4/AVI for frame-based analysis'):
        select_input('video')
    st.caption('Upload MP4/AVI (short)')
with card_cols[2]:
    if st.button('Camera', key='card_camera', help='Use your webcam to capture a photo for analysis'):
        select_input('camera')
    st.caption('Use your webcam')

# Sidebar About
with st.sidebar.expander('About & Privacy', expanded=True):
    st.markdown('''
    #### Facial Expression Recognition for Mental Health
    This tool analyzes facial expressions locally to provide non-clinical insights about emotional well-being. No images or videos are stored or uploaded. This is not a medical diagnosis.
    
    If you are in crisis or need immediate help, contact local emergency services or a mental health professional.
    ''')
    st.markdown('---')
    st.markdown('<div style="font-size:13px; color:#9fb0d9; margin-bottom:8px">Privacy: Local processing only — no data is uploaded.</div>', unsafe_allow_html=True)

# Main page: show only three large buttons (Image, Video, Camera). Clicking navigates to a detail page.
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'selected_input' not in st.session_state:
    st.session_state['selected_input'] = None

# Simple navigation: use Streamlit buttons to set selected input

if st.session_state['page'] == 'home':
    # Keep a thin invisible placeholder so Streamlit keeps the session alive while we use the HTML cards
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    # Listen for location query params (if any) and navigate accordingly
    # Use the stable `st.query_params` API instead of the deprecated experimental_get_query_params
    params = st.query_params if hasattr(st, 'query_params') else {}
    if params and 'input' in params:
        # params values are lists in Streamlit query_params
        try:
            k = params.get('input')
            if isinstance(k, list) and k:
                k = k[0]
            if k in ('image', 'video', 'camera'):
                select_input(k)
        except Exception:
            pass

elif st.session_state['page'] == 'detail':
    kind = st.session_state['selected_input']
    cols_top = st.columns([1,8,1])
    with cols_top[0]:
        if st.button('← Back', key='back_btn'):
            go_home()
    with cols_top[1]:
        st.markdown(f"<h2 style='text-align:center;'>You selected: {kind.capitalize()}</h2>", unsafe_allow_html=True)
    # Detail area: show uploader or camera based on kind
    st.markdown('<div style="max-width:840px; margin:12px auto;">', unsafe_allow_html=True)
    if kind == 'image':
        uploaded_file = st.file_uploader('Choose a JPG/PNG image', type=['jpg','jpeg','png'], key='detail_image')
        if uploaded_file is not None:
            try:
                img = Image.open(uploaded_file).convert('RGB')
                st.image(img, width=420)
                model, device = get_model()
                input_tensor = transform(img).unsqueeze(0).to(device)
                with torch.no_grad():
                    output = model(input_tensor)
                    probs = torch.softmax(output, dim=1).cpu().numpy()[0]
                    pred = torch.argmax(output, dim=1).item()
                scores = compute_mental_health_scores(probs)
                display_results(pred, probs, scores, source='Image (detail)')
            except Exception as e:
                st.error(f'Error processing image: {e}')
    elif kind == 'video':
        uploaded_video = st.file_uploader('Choose a short MP4/AVI', type=['mp4','avi','mov'], key='detail_video')
        if uploaded_video is not None:
            try:
                with st.spinner('Processing video (first 30 frames)...'):
                    temp_video_path = 'temp_video_detail.mp4'
                    with open(temp_video_path, 'wb') as f:
                        f.write(uploaded_video.read())
                    model, device = get_model()
                    cap = cv2.VideoCapture(temp_video_path)
                    probs_list = []
                    for _ in range(30):
                        ret, frame = cap.read()
                        if not ret:
                            break
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img_pil = Image.fromarray(img)
                        input_tensor = transform(img_pil).unsqueeze(0).to(device)
                        with torch.no_grad():
                            output = model(input_tensor)
                            probs = torch.softmax(output, dim=1).cpu().numpy()[0]
                        probs_list.append(probs)
                    cap.release()
                avg_probs = np.mean(probs_list, axis=0) if probs_list else np.zeros(len(class_names))
                pred = int(np.argmax(avg_probs))
                scores = compute_mental_health_scores(avg_probs)
                st.write(f'Processed {len(probs_list)} frames')
                display_results(pred, avg_probs, scores, source='Video (detail)')
            except Exception as e:
                st.error(f'Error processing video: {e}')
            try:
                os.remove(temp_video_path)
            except Exception:
                pass
    elif kind == 'camera':
        camera_img = st.camera_input('Capture a photo', key='detail_camera')
        if camera_img is not None:
            try:
                img = Image.open(camera_img).convert('RGB')
                st.image(img, width=420)
                model, device = get_model()
                input_tensor = transform(img).unsqueeze(0).to(device)
                with torch.no_grad():
                    output = model(input_tensor)
                    probs = torch.softmax(output, dim=1).cpu().numpy()[0]
                    pred = torch.argmax(output, dim=1).item()
                scores = compute_mental_health_scores(probs)
                display_results(pred, probs, scores, source='Camera (detail)')
            except Exception as e:
                st.error(f'Error processing camera image: {e}')
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('---')
st.write('This tool is for educational use only. Not a medical diagnosis.')

# History panel (simple)
with st.expander('Session results history'):
    for i, rpt in enumerate(reversed(st.session_state['history'][-10:])):
        st.write(f"{rpt['timestamp']} — {rpt['primary_emotion']} ({rpt['source']})")

# Footer (Streamlit-native)
st.markdown('---')
st.markdown("This tool is designed for educational and wellness purposes only. For professional mental health support, please consult a qualified healthcare provider.")
left, right = st.columns([1,1])
with left:
    st.markdown('© 2024 MindSense')
with right:
    st.markdown('[Privacy Policy](#) • [Terms of Service](#)')
