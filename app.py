import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="İngilizce Telaffuz Atölyesi", page_icon="🎤")

# --- RENKLİ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stSelectbox, .stButton, .stAudio {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 5px;
    }
    h1 { color: #2c3e50; }
    .info-note {
        font-size: 0.85rem;
        color: #555;
        text-align: center;
        margin-top: 30px;
        padding: 10px;
        border-top: 1px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UYGULAMA MANTIĞI ---
# Session State Başlangıcı
if 'yildizlar' not in st.session_state:
    st.session_state.yildizlar = 0
if 'basarilanlar' not in st.session_state:
    st.session_state.basarilanlar = set()

# Kelimeler Listesi (Baş harfleri büyük)
kelimeler_ham = [
    "the", "think", "thought", "about", "are", "refuse", "use", "she", "chat", 
    "accept", "language", "country", "umbrella", "quick", "who", "what", 
    "where", "three", "speak", "sign", "join", "jump", "location", "bathroom", 
    "today", "wednesday", "thursday", "watch", "rarely", "usually", "generally", 
    "current", "university", "choose"
]
kelimeler = [k.title() for k in kelimeler_ham]

# Yan Panel: Skor Tablosu (Anlık güncellenmesi için en üstte tutuyoruz)
st.sidebar.markdown(f"## ⭐ Yıldızların: {st.session_state.yildizlar}")
st.sidebar.divider()
st.sidebar.write("🏆 **Başarılan Kelimeler:**")
for k in sorted(st.session_state.basarilanlar):
    st.sidebar.write(f"✅ {k}")

# Ana Ekran
st.title("🎤 İngilizce Telaffuz Pratiği")
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
    audio_record = mic_recorder(
        start_prompt="Kaydı Başlat 🎙️",
        stop_prompt="Durdur ⏹️",
        key='recorder'
    )
    if audio_record:
        st.audio(audio_record['bytes'])

# Başarı Butonu ve Anlık Güncelleme
st.divider()
if st.button("Başardım! Yıldız Ver ⭐", use_container_width=True):
    if secilen_kelime not in st.session_state.basarilanlar:
        st.session_state.yildizlar += 1
        st.session_state.basarilanlar.add(secilen_kelime)
        st.balloons()
        st.rerun()  # Sayfayı anında yenileyerek yıldızı hemen sidebar'da gösterir
    else:
        st.info("Bu kelimeyi zaten başarmışsın!")

st.markdown('<div class="info-note">⚠️ Gizlilik ve İlerleme: Sayfayı yenilediğinizde tüm ses kayıtları ve yıldız ilerlemeniz sıfırlanır. Hiçbir veriniz sunucularımızda saklanmaz.</div>', unsafe_allow_html=True)

if st.sidebar.button("İlerlemeyi Elle Sıfırla"):
    st.session_state.yildizlar = 0
    st.session_state.basarilanlar = set()
    st.rerun()
