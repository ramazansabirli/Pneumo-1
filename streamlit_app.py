import streamlit as st
import requests

st.title("Pnömotoraks AI Karar Destek Paneli")

st.subheader("📥 Vaka Yükleme ve Analiz")

with st.form("upload_form"):
    hasta_id = st.text_input("Hasta ID")
    file = st.file_uploader("Video (.avi)", type=["avi"])
    spo2 = st.number_input("SpO2", 0, 100)
    rr = st.number_input("RR", 0, 60)
    hr = st.number_input("HR", 0, 200)
    bp = st.number_input("BP", 0, 300)
    bilinc = st.selectbox("Bilinç Durumu", [0, 1])
    yas = st.number_input("Yaş", 0, 120)

    submitted = st.form_submit_button("Gönder ve Tahmin Al")
    if submitted and file is not None:
        files = {"file": file}
        data = {
            "hasta_id": hasta_id, "spo2": spo2, "rr": rr, "hr": hr,
            "bp": bp, "bilinc": bilinc, "yas": yas
        }
        upload = requests.post("http://localhost:10000/upload/", files=files, data=data)
        pred = requests.post("http://localhost:10000/predict/", data=data)
        st.success(f"Model Önerisi: {pred.json().get('tedavi_önerisi', '---')}")
