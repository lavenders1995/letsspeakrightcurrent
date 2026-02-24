import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import time

# Sayfa Ayarları
st.set_page_config(page_title="İngilizce Telaffuz Atölyesi", page_icon="🎤")

# --- RENKLİ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* Mobil uyumlu büyük butonlar */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
    }
    .yildiz-kutusu {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #FFD700;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'yildizlar' not in st.session_state:
    st.session_state.yildizlar = 0
if 'basarilanlar' not in st.session_state:
    st.session_state.basarilanlar = set()

# --- ANA EKRAN (MOBİL İÇİN YILDIZLAR EN ÜSTTE) ---
st.title("🎤 Telaffuz Pratiği")

# Yıldızları yan panel yerine ana ekranda en üste taşıdık
st.markdown(f"""
    <div class="yildiz-kutusu">
        <h2 style='margin:0;'>⭐ Toplam Yıldız: {st.session_state.yildizlar}</h2>
    </div>
    """, unsafe_allow_html=True)

# Kelime Listesi
kelimeler_ham = ["the", "think", "thought", "about", "are", "refuse", "use", "she", "chat", "accept", "language", "country", "umbrella", "quick", "who", "what", "where", "three", "speak", "sign", "join", "jump", "location", "bathroom", "today", "wednesday", "thursday", "watch", "rarely", "usually", "generally", "current", "university", "choose"]
kelimeler = [k.title() for k in kelimeler_ham]

secilen_kelime = st.selectbox("Bir kelime seçin:", kelimeler)

# Ses ve Kayıt Alanı
col1, col2 = st.columns(2)
with col1:
    if st.button(f"🔊 {secilen_kelime} Dinle"):
        tts = gTTS(text=secilen_kelime, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

with col2:
    audio_record = mic_recorder(start_prompt="🎙️ Kaydet", stop_prompt="⏹️ Durdur", key='recorder')
    if audio_record:
        st.audio(audio_record['bytes'])

# BAŞARI BUTONU
st.divider()
if st.button("BAŞARDIM! YILDIZ VER ⭐"):
    if secilen_kelime not in st.session_state.basarilanlar:
        st.session_state.yildizlar += 1
        st.session_state.basarilanlar.add(secilen_kelime)
        st.balloons() # Balonlar artık daha net görünecek
        time.sleep(0.5) # Balonların görünmesi için yarım saniye bekleme
        st.rerun()
    else:
        st.info("Bu kelimeyi zaten başarmışsın!")

# Başarılan kelimeleri alt kısma ekledik (Mobilde görünür olması için)
if st.session_state.basarilanlar:
    with st.expander("✅ Başardığın Kelimeleri Gör"):
        st.write(", ".join(sorted(st.session_state.basarilanlar)))

st.markdown('<div style="font-size:0.8rem; color:grey; text-align:center; margin-top:50px;">⚠️ Sayfa yenilenirse ilerleme silinir.</div>', unsafe_allow_html=True)

# Sıfırlama Butonu
if st.button("İlerlemeyi Sıfırla 🗑️"):
    st.session_state.yildizlar = 0
    st.session_state.basarilanlar = set()
    st.rerun()
