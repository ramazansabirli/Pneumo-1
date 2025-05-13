from fpdf import FPDF

def generate_pdf_report(patient_id: str, data: dict, shap_fig_html: str, save_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Pnömotoraks AI Raporu - Hasta: {patient_id}", ln=True)
    for key, val in data.items():
        pdf.cell(200, 10, txt=f"{key}: {val}", ln=True)

    pdf.output(save_path)
