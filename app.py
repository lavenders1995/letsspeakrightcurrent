import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import time

# Sayfa Ayarları
st.set_page_config(page_title="İngilizce Telaffuz Alıştırması", page_icon="🎤")

# --- PASTEL RENKLİ TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Pastel Pembe-Mavi-Lila Geçişi */
    .stApp {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }
    
    /* Kartlar için Pastel Tonlar */
    .stSelectbox, .stAudio, div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 15px;
        border: 1px solid #fce4ec;
    }

    /* Yıldız Paneli */
    .yildiz-panel {
        background-color: #fff9c4;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        border: 2px dashed #ffd54f;
        margin: 20px 0;
    }

    /* Yazı ve Buton Ortalama */
    .centered-content {
        text-align: center;
    }
    
    /* Ana Başlık */
    h1 { color: #8e24aa; font-family: 'Comic Sans MS', cursive; text-align: center; }
    h3 { color: #5e35b1; text-align: center; }
    
    /* Sıfırla Butonu Özel Ortalama */
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
    }

    .info-note {
        font-size: 0.85rem;
        color: #888;
        text-align: center;
        margin-top: 30px;
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

# Yıldız Paneli
st.markdown(f"""
    <div class="yildiz-panel">
        <h2 style='margin:0; color:#fbc02d;'>⭐ Toplam Yıldızın: {st.session_state.yildizlar} ⭐</h2>
    </div>
    """, unsafe_allow_html=True)

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

st.divider()
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

# --- ORTALANMIŞ ALT KISIM ---
if st.session_state.basarilanlar:
    st.markdown("<h3 style='text-align: center;'>🏆 Başardığın Kelimeler</h3>", unsafe_allow_html=True)
    başarı_metni = ", ".join(sorted(st.session_state.basarilanlar))
    st.markdown(f"<p style='text-align: center; font-size: 1.1rem;'>{başarı_metni}</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True) # Boşluk

# Sıfırlama Butonu (CSS ile ortalandı)
if st.button("Tüm İlerlemeyi Sıfırla 🗑️"):
    st.session_state.yildizlar = 0
    st.session_state.basarilanlar = set()
    st.rerun()

st.markdown('<div class="info-note">⚠️ Sayfayı yenilerseniz ilerlemeniz sıfırlanır. Verileriniz kaydedilmez.</div>', unsafe_allow_html=True)
