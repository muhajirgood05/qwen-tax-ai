"""
Qwen Tax AI - Backend API
AI-powered tax consultation assistant for Indonesian taxpayers.
Built with FastAPI + Qwen (Alibaba Cloud DashScope).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from services.qwen_client import QwenTaxClient
from services.tax_calculator import TaxCalculator
from services.rag_service import RAGService

app = FastAPI(
    title="Qwen Tax AI",
    description="AI-powered tax consultation assistant for Indonesian taxpayers",
    version="1.0.0",
)

# CORS middleware for Vue.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
qwen_client = QwenTaxClient()
tax_calculator = TaxCalculator()
rag_service = RAGService()


# --- Request/Response Models ---

class ChatRequest(BaseModel):
    message: str
    conversation_history: list[dict] = []


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []
    disclaimer: str = (
        "⚠️ Jawaban ini bersifat informatif dan bukan nasihat pajak resmi. "
        "Konsultasikan dengan konsultan pajak berlisensi untuk keperluan sebenarnya."
    )


class TaxCalcRequest(BaseModel):
    gross_monthly_salary: float
    status: str = "TK/0"  # TK/0, K/0, K/1, K/2, K/3
    bpjs_percentage: float = 0.01
    other_deductions: float = 0.0


class TaxCalcResponse(BaseModel):
    gross_annual: float
    biaya_jabatan: float
    bpjs_annual: float
    other_deductions_annual: float
    net_annual: float
    ptkp: float
    pkp: float
    pph21_annual: float
    pph21_monthly: float
    effective_rate: float
    breakdown: list[dict]


# --- API Endpoints ---

@app.get("/")
async def root():
    return {
        "app": "Qwen Tax AI",
        "version": "1.0.0",
        "description": "AI-powered tax consultation for Indonesian taxpayers",
        "powered_by": "Qwen (Alibaba Cloud)",
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI tax assistant.
    Uses RAG to retrieve relevant tax regulations before generating response.
    """
    try:
        # Step 1: Retrieve relevant context from knowledge base
        context = rag_service.retrieve(request.message)

        # Step 2: Generate response using Qwen
        reply = await qwen_client.chat(
            user_message=request.message,
            context=context,
            conversation_history=request.conversation_history,
        )

        # Step 3: Get source references
        sources = rag_service.get_sources(request.message)

        return ChatResponse(reply=reply, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.post("/api/calculate-pph21", response_model=TaxCalcResponse)
async def calculate_pph21(request: TaxCalcRequest):
    """
    Calculate PPh 21 (income tax) based on provided salary and status.
    """
    try:
        result = tax_calculator.calculate_pph21(
            gross_monthly_salary=request.gross_monthly_salary,
            status=request.status,
            bpjs_percentage=request.bpjs_percentage,
            other_deductions=request.other_deductions,
        )
        return TaxCalcResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/tax-info/{topic}")
async def get_tax_info(topic: str):
    """
    Get tax information on a specific topic.
    Available topics: pph21, ppn, spt
    """
    info = rag_service.get_topic_info(topic)
    if not info:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' not found")
    return {"topic": topic, "content": info}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
