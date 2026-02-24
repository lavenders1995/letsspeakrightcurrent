import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import time

# Sayfa Ayarları
st.set_page_config(page_title="İngilizce Telaffuz Atölyesi", page_icon="⭐")

# --- GELİŞMİŞ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* Yıldız Butonu Stili */
    .stButton>button[kind="secondary"] {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border: 2px solid #b8860b;
        border-radius: 20px;
    }
    /* Bilgi Notu */
    .info-note {
        font-size: 0.8rem;
        color: #666;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'yildizlar' not in st.session_state:
    st.session_state.yildizlar = 0
if 'basarilanlar' not in st.session_state:
    st.session_state.basarilanlar = set()

# --- YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.header("🌟 Başarı Tablon")
    st.metric(label="Toplam Yıldız", value=st.session_state.yildizlar)
    st.divider()
    st.subheader("✅ Başarılanlar:")
    for k in sorted(st.session_state.basarilanlar):
        st.write(f"⭐ {k}")
    
    if st.button("İlerlemeyi Sıfırla"):
        st.session_state.yildizlar = 0
        st.session_state.basarilanlar = set()
        st.rerun()

# --- ANA EKRAN ---
st.title("🎤 Telaffuz Pratiği")

# MOBİL İÇİN ÖZEL BUTON: Yan paneli açmaya yönlendirir
if st.button("📊 YILDIZLARIMI VE LİSTEMİ GÖR"):
    st.info("Sol üstteki menü açıldı (veya telefonunuzun sol kenarından çekin)!")
    # Bu buton aslında bir hatırlatıcıdır, sidebar zaten oradadır.

# Kelime Listesi
kelimeler_ham = ["the", "think", "thought", "about", "are", "refuse", "use", "she", "chat", "accept", "language", "country", "umbrella", "quick", "who", "what", "where", "three", "speak", "sign", "join", "jump", "location", "bathroom", "today", "wednesday", "thursday", "watch", "rarely", "usually", "generally", "current", "university", "choose"]
kelimeler = [k.title() for k in kelimeler_ham]

secilen_kelime = st.selectbox("Bir kelime seçin:", kelimeler)

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

# BAŞARI BUTONU VE BALONLAR
st.divider()
if st.button("✅ BAŞARDIM, YILDIZIMI VER!", use_container_width=True):
    if secilen_kelime not in st.session_state.basarilanlar:
        # Önce veriyi güncelle
        st.session_state.yildizlar += 1
        st.session_state.basarilanlar.add(secilen_kelime)
        
        # BALONLAR BURADA ÇIKIYOR
        st.balloons()
        
        # Balonların ekranda kalması için minik bir mesaj gösterip bekliyoruz
        st.success(f"Tebrikler! {secilen_kelime} kelimesini başardın!")
        time.sleep(1.5) # Balonların bitmesini bekle
        st.rerun()
    else:
        st.warning("Bu kelimeyi zaten listene eklemişsin!")

st.markdown('<div class="info-note">⚠️ Sayfayı yenilerseniz yıldızlar silinir. Verileriniz kaydedilmez.</div>', unsafe_allow_html=True)
