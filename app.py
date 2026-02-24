import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import time

# Sayfa Ayarları
st.set_page_config(page_title="İngilizce Telaffuz Alıştırması", page_icon="🎤")

# --- PROFESYONEL ESTETİK DOKUNUŞLAR (CSS) ---
st.markdown("""
    <style>
    /* Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }
    
    /* Bölüm Çerçeveleri (Glassmorphism) */
    .pro-card {
        background: rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        backdrop-filter: blur(4px);
        margin-bottom: 20px;
        text-align: center;
    }

    /* Yıldız Paneli Özel Çerçeve */
    .yildiz-panel {
        background: rgba(255, 249, 196, 0.6);
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        border: 2px solid #ffd54f;
        box-shadow: 0 4px 15px rgba(255, 213, 79, 0.3);
        margin: 20px 0;
    }

    /* Başarılı Kelimeler Çerçevesi */
    .success-box {
        background: rgba(232, 245, 233, 0.6);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #a5d6a7;
        margin-top: 15px;
    }

    /* Butonları ve Yazıları Güzelleştirme */
    h1 { color: #6a1b9a; font-family: 'Segoe UI', sans-serif; text-align: center; font-weight: 700; }
    h3 { color: #4527a0; text-align: center; font-weight: 600; margin-bottom: 15px; }
    
    /* Sıfırla Butonu Ortalama */
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
        border-radius: 12px;
    }

    .info-note {
        font-size: 0.8rem;
        color: #9e9e9e;
        text-align: center;
        margin-top: 40px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UYGULAMA MANTIĞI ---
if 'yildizlar' not in st.session_state:
    st.session_state.yildizlar = 0
if 'basarilanlar' not in st.session_state:
    st.session_state.basarilanlar = set()

# Kelimeler Listesi
kelimeler_ham = [
    "the", "think", "thought", "about", "are", "refuse", "use", "she", "chat", 
    "accept", "language", "country", "umbrella", "quick", "who", "what", 
    "where", "three", "speak", "sign", "join", "jump", "location", "bathroom", 
    "today", "wednesday", "thursday", "watch", "rarely", "usually", "generally", 
    "current", "university", "choose"
]
kelimeler = [k.title() for k in kelimeler_ham]

# Başlık
st.markdown("<h1>🎤 İngilizce Telaffuz Alıştırması</h1>", unsafe_allow_html=True)

# Yıldız Paneli (Çerçeveli)
st.markdown(f"""
    <div class="yildiz-panel">
        <h2 style='margin:0; color:#fbc02d; font-size: 1.8rem;'>⭐ Toplam Yıldızın: {st.session_state.yildizlar} ⭐</h2>
    </div>
    """, unsafe_allow_html=True)

# Ana Çalışma Alanı Çerçevesi
st.markdown('<div class="pro-card">', unsafe_allow_html=True)
secilen_kelime = st.selectbox("Bir kelime seçin:", kelimeler)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 1. Doğru Ses")
    if st.button(f"🔊 '{secilen_kelime}' Dinle"):
        tts = gTTS(text=secilen_kelime, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

with col2:
    st.markdown("### 2. Senin Sesin")
    audio_record = mic_recorder(start_prompt="Kaydı Başlat 🎙️", stop_prompt="Durdur ⏹️", key='recorder')
    if audio_record:
        st.audio(audio_record['bytes'])
st.markdown('</div>', unsafe_allow_html=True)

# Başarı Butonu
if st.button("Başardım! Yıldız Ver ⭐", use_container_width=True):
    if secilen_kelime not in st.session_state.basarilanlar:
        st.session_state.yildizlar += 1
        st.session_state.basarilanlar.add(secilen_kelime)
        st.balloons()
        st.success(f"Tebrikler! {secilen_kelime} kelimesini başardın!")
        time.sleep(3) 
        st.rerun()
    else:
        st.info("Bu kelimeyi zaten başarmışsın!")

# --- ALT KISIM (Çerçeveli) ---
if st.session_state.basarilanlar:
    st.markdown('<div class="pro-card" style="background: rgba(232, 245, 233, 0.5);">', unsafe_allow_html=True)
    st.markdown("<h3>🏆 Başardığın Kelimeler</h3>", unsafe_allow_html=True)
    başarı_metni = ", ".join(sorted(st.session_state.basarilanlar))
    st.markdown(f"<p style='color: #2e7d32; font-weight: 500;'>{başarı_metni}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sıfırlama Butonu
if st.button("Tüm İlerlemeyi Sıfırla 🗑️"):
    st.session_state.yildizlar = 0
    st.session_state.basarilanlar = set()
    st.rerun()

st.markdown('<div class="info-note">⚠️ Gizlilik: Sayfayı yenilediğinizde veriler silinir.</div>', unsafe_allow_html=True)
