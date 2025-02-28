import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from tools.milvus.config import Config
from docx import Document


# 初始化模型
def init_model():
    model = SentenceTransformer(Config.MODEL_NAME)
    return model


# 提取 PDF 文本
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_doc(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text


def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


# 切分文本
def split_text(text, chunk_size):
    text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return text_chunks


# 生成文本向量
def generate_embeddings(text_chunks, model):
    embeddings = model.encode(text_chunks, normalize_embeddings=True)
    return embeddings
