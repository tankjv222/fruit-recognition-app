import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time

# ─────────────────────────────────────────────
#  CẤU HÌNH TRANG  
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FruitSense AI – Nhận Diện Trái Cây",
    page_icon="",
    layout="centered",
)

# ─────────────────────────────────────────────
#  CSS TUỲ CHỈNH GIAO DIỆN
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Nền gradient xanh lá nhẹ */
.stApp {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 40%, #bbf7d0 100%);
    min-height: 100vh;
}

/* Tiêu đề lớn */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #14532d;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.hero-sub {
    color: #4ade80;
    font-size: 1rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Card upload */
.upload-card {
    background: rgba(255,255,255,0.7);
    border: 2px dashed #86efac;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    backdrop-filter: blur(8px);
}

/* Badge kết quả */
.result-badge {
    display: inline-block;
    background: linear-gradient(135deg, #16a34a, #4ade80);
    color: white;
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    padding: 0.6rem 1.8rem;
    border-radius: 100px;
    margin: 0.5rem 0 1rem 0;
    box-shadow: 0 8px 24px rgba(22,163,74,0.3);
}

/* Thanh confidence */
.conf-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.5rem;
}
.conf-label {
    font-weight: 500;
    min-width: 140px;
    color: #166534;
    font-size: 0.9rem;
}
.conf-bar-wrap {
    flex: 1;
    background: #dcfce7;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #4ade80, #16a34a);
    transition: width 0.6s ease;
}
.conf-pct {
    font-size: 0.85rem;
    font-weight: 600;
    color: #15803d;
    min-width: 48px;
    text-align: right;
}

/* Divider */
.my-divider {
    border: none;
    border-top: 1.5px solid #bbf7d0;
    margin: 1.5rem 0;
}

.hero-title {
    color: #064e3b !important; /* Xanh lục sẫm */
}
.hero-sub {
    color: #059669 !important; /* Xanh ngọc đậm */
}

h4 {
    color: #064e3b !important;
}

strong {
    color: #064e3b !important;
}

.conf-label {
    color: #047857 !important;
}

.conf-pct {
    color: #047857 !important;
}

div[data-testid="stNotification"] p {
    color: #064e3b !important;
    font-weight: 600 !important;
}

div[data-testid="stSpinner"] p {
    color: #064e3b !important;
    font-weight: 600 !important;
}

div[data-testid="stNotification"] svg {
    fill: #059669 !important;
}

.footer {
    color: #059669 !important;
}

.footer {
    text-align: center;
    font-size: 0.78rem;
    color: #86efac;
    margin-top: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
VIET_HOA = {
    "APPLE":       "Táo ",
    "BANANA":      "Chuối ",
    "CHERRY":      "Cherry ",
    "CHICKOO":     "Hồng Xiêm",
    "GRAPES":      "Nho ",
    "KIWI":        "Kiwi ",
    "MANGO":       "Xoài ",
    "ORANGE":      "Cam ",
    "STRAWBERRY":  "Dâu Tây ",
    "WATERMELON":  "Dưa Hấu ",
}

def viet_hoa(raw_name: str) -> str:
    key = raw_name.replace("fruit", "").strip().upper()
    return VIET_HOA.get(key, raw_name.title())

# ─────────────────────────────────────────────
#  TẢI MODEL 
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    return YOLO("best.pt")

# ─────────────────────────────────────────────
#  GIAO DIỆN CHÍNH
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">FruitSense AI </div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Nhận Diện Trái Cây · YOLO11 · Phân Loại Tự Động</div>', unsafe_allow_html=True)

# Load model
with st.spinner("Đang tải mô hình AI..."):
    try:
        model = load_model()
    except Exception:
        st.error(" Không tìm thấy file **best.pt**. Hãy đặt file model cùng thư mục với app.py rồi chạy lại.")
        st.stop()

st.success(" Mô hình đã sẵn sàng!", icon="✅")

st.markdown('<hr class="my-divider">', unsafe_allow_html=True)

# Upload ảnh
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📸 Tải ảnh trái cây lên (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="visible"
)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  XỬ LÝ & HIỂN THỊ KẾT QUẢ
# ─────────────────────────────────────────────
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.image(image, caption="Ảnh bạn đã tải lên", use_container_width=True)

    with col2:
        with st.spinner(" AI đang phân tích..."):
            time.sleep(0.3)          # nhỏ delay cho UX mượt
            results = model(image)
            result  = results[0]
            probs   = result.probs

        top1_idx  = probs.top1
        top1_name = viet_hoa(result.names[top1_idx])
        top1_conf = float(probs.top1conf) * 100

        st.markdown("####  Kết quả nhận diện")
        st.markdown(f'<div class="result-badge">{top1_name}</div>', unsafe_allow_html=True)
        st.markdown(f"**Độ tự tin:** `{top1_conf:.1f}%`")

        st.markdown('<hr class="my-divider">', unsafe_allow_html=True)
        st.markdown("#### Top 5 phân loại")

        for idx, conf_tensor in zip(probs.top5, probs.top5conf):
            name  = viet_hoa(result.names[idx])
            pct   = float(conf_tensor) * 100
            if pct < 0.5:
                continue
            fill  = int(pct)
            st.markdown(f"""
            <div class="conf-row">
                <span class="conf-label">{name}</span>
                <div class="conf-bar-wrap">
                    <div class="conf-bar-fill" style="width:{fill}%"></div>
                </div>
                <span class="conf-pct">{pct:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="my-divider">', unsafe_allow_html=True)

    # Cảnh báo nếu confidence thấp
    if top1_conf < 60:
        st.warning(" Độ tự tin thấp — hãy thử ảnh rõ hơn, chụp gần trái cây hơn.")

st.markdown('<div class="footer">FruitSense AI · YOLO11 · Đồ án môn học · 2026</div>', unsafe_allow_html=True)
