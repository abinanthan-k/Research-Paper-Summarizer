from langchain_text_splitters import RecursiveCharacterTextSplitter
import io
import pdfplumber
from fastapi import UploadFile

async def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    file_bytes = await pdf_file.read()
    
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text: 
                text += page_text + "\n"
    
    return text



def split_into_chunks(text, chunk_size: int = 10000, chunk_overlap: int = 500):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.create_documents([text])
    return chunks
