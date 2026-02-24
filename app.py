import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io

# Sayfa Ayarları ve Renkli Tema
st.set_page_config(page_title="İngilizce Telaffuz Atölyesi", page_icon="🎤")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #ff4b4b;
        color: white;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎤 İngilizce Telaffuz Pratiği")
st.write("Kelimeyi seç, dinle ve kendi sesini kaydederek karşılaştır!")

# Kelime Listesi
kelimeler = [
    "the", "think", "thought", "about", "are", "refuse", "use", "she", "chat", 
    "accept", "language", "country", "umbrella", "quick", "who", "what", 
    "where", "three", "speak", "sign", "join", "jump", "location", "bathroom", 
    "today", "wednesday", "thursday", "watch", "rarely", "usually", "generally", 
    "current", "university", "choose"
]

# Session State (Yıldızları ve durumu tutmak için - Yenileyince silinir)
if 'yildizlar' not in st.session_state:
    st.session_state.yildizlar = 0
if 'basarilanlar' not in st.session_state:
    st.session_state.basarilanlar = set()

# Yan Panel: Skor Tablosu
st.sidebar.header(f"⭐ Toplam Yıldız: {st.session_state.yildizlar}")
st.sidebar.write("Başarılan Kelimeler:")
for k in st.session_state.basarilanlar:
    st.sidebar.write(f"✅ {k}")

# Ana Ekran: Kelime Seçimi
secilen_kelime = st.selectbox("Çalışmak istediğin kelimeyi seç:", kelimeler)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Dinle")
    if st.button(f"'{secilen_kelime}' Telaffuzunu Çal"):
        tts = gTTS(text=secilen_kelime, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

with col2:
    st.subheader("2. Kaydet")
    st.write("Kendi sesini kaydet:")
    audio_record = mic_recorder(
        start_prompt="Kaydı Başlat 🎙️",
        stop_prompt="Durdur ⏹️",
        key='recorder'
    )
    
    if audio_record:
        st.audio(audio_record['bytes'])
        st.info("Kendi sesinle orijinali karşılaştır!")

# Başarı İşaretleme
st.divider()
if st.button("Başardım! Yıldızımı Ver ⭐"):
    if secilen_kelime not in st.session_state.basarilanlar:
        st.session_state.yildizlar += 1
        st.session_state.basarilanlar.add(secilen_kelime)
        st.balloons()
        st.success(f"Harika! '{secilen_kelime}' kelimesi için bir yıldız kazandın!")
    else:
        st.warning("Bu kelimeden zaten yıldız aldın!")

# Temizleme Butonu
if st.sidebar.button("Tüm İlerlemeyi Sıfırla"):
    st.session_state.yildizlar = 0
    st.session_state.basarilanlar = set()
    st.rerun()
