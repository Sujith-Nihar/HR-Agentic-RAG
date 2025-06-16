import pdfplumber
from docx import Document

class FileLoader:
    def load(self, filepath):
        if filepath.endswith(".txt"):
            return self._load_txt(filepath)
        elif filepath.endswith(".pdf"):
            return self._load_pdf(filepath)
        elif filepath.endswith(".docx"):
            return self._load_docx(filepath)
        else:
            raise ValueError("Unsupported file format.")

    def _load_txt(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _load_docx(self, path):
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
