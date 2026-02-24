import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import time

# Sayfa Ayarları
st.set_page_config(page_title="İngilizce Telaffuz Alıştırması", page_icon="🎤")

# --- ESTETİK VE ÇERÇEVELİ TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }
    
    /* Bölüm Çerçeveleri (Modern Buzlu Cam Efekti) */
    .main-card {
        background: rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Yıldız Paneli Özel Çerçeve */
    .yildiz-panel {
        background-color: rgba(255, 249, 196, 0.7);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        border: 2px dashed #ffd54f;
        box-shadow: 0 4px 10px rgba(255, 213, 79, 0.2);
        margin: 20px 0;
    }

    /* Başarılı Kelimeler Alt Çerçeve */
    .success-card {
        background: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #a5d6a7;
        text-align: center;
        margin-top: 20px;
    }
    
    /* Yazı Stilleri */
    h1 { color: #8e24aa; font-family: 'Comic Sans MS', cursive; text-align: center; }
    h3 { color: #5e35b1; text-align: center; margin-bottom: 15px; }
    
    /* Butonları Ortalama ve Güzelleştirme */
    div.stButton > button {
        border-radius: 12px;
        transition: 0.3s;
    }
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
    }

    .info-note {
        font-size: 0.85rem;
        color: #888;
        text-align: center;
        margin-top: 30px;
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
st.title("🎤 İngilizce Telaffuz Alıştırması")

# Yıldız Paneli (Çerçeveli)
st.markdown(f"""
    <div class="yildiz-panel">
        <h2 style='margin:0; color:#fbc02d;'>⭐ Toplam Yıldızın: {st.session_state.yildizlar} ⭐</h2>
    </div>
    """, unsafe_allow_html=True)

# Ana Alıştırma Alanı Çerçevesi
st.markdown('<div class="main-card">', unsafe_allow_html=True)
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

st.divider()

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

# --- ORTALANMIŞ ALT KISIM (Çerçeveli) ---
if st.session_state.basarilanlar:
    st.markdown('<div class="success-card">', unsafe_allow_html=True)
    st.markdown("<h3>🏆 Başardığın Kelimeler</h3>", unsafe_allow_html=True)
    başarı_metni = ", ".join(sorted(st.session_state.basarilanlar))
    st.markdown(f"<p style='font-size: 1.1rem; color: #2e7d32;'>{başarı_metni}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sıfırlama Butonu
if st.button("Tüm İlerlemeyi Sıfırla 🗑️"):
    st.session_state.yildizlar = 0
    st.session_state.basarilanlar = set()
    st.rerun()

st.markdown('<div class="info-note">⚠️ Sayfayı yenilerseniz ilerlemeniz sıfırlanır. Verileriniz kaydedilmez.</div>', unsafe_allow_html=True)
