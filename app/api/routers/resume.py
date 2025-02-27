from fastapi import APIRouter, UploadFile, File, Depends
from app.models.text import Text
from app.services.llm_service import LlamaService, get_llm_service

from pydantic import BaseModel
import pdfplumber
import uuid
import io

router=APIRouter()

# Añade estos modelos Pydantic
class QuestionRequest(BaseModel):
    question: str
    pdf_id: str

pdf_cache = {}  # Diccionario simple para almacenar PDFs procesados    
    

@router.post('/ask_question/')
async def ask_question(request: QuestionRequest, llm: LlamaService = Depends(get_llm_service)):
    """
    Responde preguntas sobre un contexto específico usando el modelo Llama 2
    """
    response = llm.generate_response(f"Contexto: {request.context}\n\nPregunta: {request.question}")
    return {"answer": response}

@router.post('/analyze_pdf/')
async def analyze_pdf(file: UploadFile = File(...), llm: LlamaService = Depends(get_llm_service)):
    """
    Sube un PDF, extrae su texto y genera un análisis usando Llama 2
    """
    try:
        contents = await file.read()
        text = ""
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Página {page_number} ---\n{page_text}\n"
                else:
                    text += f"--- Página {page_number} (sin texto) ---\n"
        
        # Prompt más específico para el resumen
        summary_prompt = f"Resume el siguiente texto en unas pocas oraciones, extrayendo la información más importante: {text}"
        summary = llm.generate_response(summary_prompt, max_new_tokens=200)

        # Limpiar las etiquetas del resumen
        summary = summary.replace("<s>", "").replace("</s>", "")

        pdf_id = str(uuid.uuid4())  # Genera un ID único
        pdf_cache[pdf_id] = text  # Guarda el texto del PDF
        
        
        return {
            "filename": file.filename,
            "content": text[:1000] + "..." if len(text) > 1000 else text,  # Truncar el contenido para la respuesta
            "summary": summary,
            "pdf_id": pdf_id, "summary": summary
        }
    
    except Exception as e:
        return {"error": f"Error al procesar el PDF: {str(e)}"}
    


# En analyze_pdf:


# Nuevo endpoint:
@router.post('/ask_pdf_question/')
async def ask_pdf_question(
    request: QuestionRequest,
    llm: LlamaService = Depends(get_llm_service)
):
    pdf_id = request.pdf_id
    question = request.question

    if pdf_id not in pdf_cache:
        return {"error": "PDF no encontrado. Procésalo primero con analyze_pdf"}

    context = pdf_cache[pdf_id]

      # Mejor prompt para respuestas más limpias
    prompt = f"""Basándote en el siguiente documento:

    {context}

    Responde esta pregunta de forma concisa y directa: {question}
    Usa solo la información del documento. Si la información no está en el documento, indica que no está disponible.
    """

    response = llm.generate_response(prompt)

    cleaned_response = response.replace("<s>", "").replace("</s>", "")

    # Extrae solo la parte después de "Respuesta:" si existe
    if "Respuesta:" in cleaned_response:
        final_response = cleaned_response.split("Respuesta:")[-1].strip()
    else:
        final_response = cleaned_response.strip()
    
    return {"answer": final_response}