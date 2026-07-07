import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_resume_text(file_path: str):

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    if file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    return ""
