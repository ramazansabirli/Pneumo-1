import gradio as gr
from app.services.ml_model import predict_treatment_from_input

def predict_fn(hasta_id, spo2, rr, hr, bp, bilinc, yas):
    result = predict_treatment_from_input(hasta_id, spo2, rr, hr, bp, bilinc, yas)
    return result["tedavi_önerisi"] if result["status"] == "success" else result["message"]

app = gr.Interface(
    fn=predict_fn,
    inputs=["text", "number", "number", "number", "number", "number", "number"],
    outputs="text",
    title="Pnömotoraks Tedavi Öneri Sistemi",
    description="Hasta ID ile video + parametre giriniz, AI önerisini sunsun"
)
