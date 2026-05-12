"""
Qwen API Client for Tax AI Assistant.
Uses OpenAI-compatible API via Alibaba Cloud DashScope.
"""

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """Kamu adalah Asisten Pajak AI Indonesia yang ahli dan ramah. 
Kamu membantu wajib pajak Indonesia memahami regulasi perpajakan dengan bahasa yang mudah dipahami.

ATURAN:
1. Jawab dalam Bahasa Indonesia kecuali diminta dalam bahasa lain.
2. Selalu berikan referensi regulasi yang relevan (UU, PP, PMK, dll).
3. Jika pertanyaan di luar domain perpajakan Indonesia, tolak dengan sopan.
4. Jangan pernah memberikan nasihat untuk menghindari pajak secara ilegal.
5. Jika tidak yakin, katakan bahwa pengguna sebaiknya berkonsultasi dengan konsultan pajak.
6. Gunakan format yang rapi dengan bullet points dan penomoran.
7. Untuk perhitungan, tunjukkan langkah-langkah secara detail.

KONTEKS REGULASI:
- UU No. 7 Tahun 2021 tentang Harmonisasi Peraturan Perpajakan (UU HPP)
- UU No. 36 Tahun 2008 tentang Pajak Penghasilan (sebagaimana diubah UU HPP)
- PP No. 58 Tahun 2023 tentang Tarif Pemotongan PPh 21 (TER)
- PMK No. 168 Tahun 2023 tentang Petunjuk Pelaksanaan Pemotongan PPh 21

TARIF PPh 21 PROGRESIF (Pasal 17 UU PPh, diubah UU HPP):
- 0 - Rp 60.000.000: 5%
- > Rp 60.000.000 - Rp 250.000.000: 15%
- > Rp 250.000.000 - Rp 500.000.000: 25%
- > Rp 500.000.000 - Rp 5.000.000.000: 30%
- > Rp 5.000.000.000: 35%

PTKP (Penghasilan Tidak Kena Pajak) 2024:
- TK/0 (Tidak Kawin, tanpa tanggungan): Rp 54.000.000
- K/0 (Kawin, tanpa tanggungan): Rp 58.500.000
- K/1 (Kawin, 1 tanggungan): Rp 63.000.000
- K/2 (Kawin, 2 tanggungan): Rp 67.500.000
- K/3 (Kawin, 3 tanggungan): Rp 72.000.000
"""


class QwenTaxClient:
    """Client for interacting with Qwen API for tax consultation."""

    def __init__(self):
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError(
                "DASHSCOPE_API_KEY environment variable is required. "
                "Get your API key from https://www.alibabacloud.com/help/en/model-studio/"
            )

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        self.model = os.getenv("QWEN_MODEL", "qwen-plus")

    async def chat(
        self,
        user_message: str,
        context: str = "",
        conversation_history: list[dict] = None,
    ) -> str:
        """
        Send a message to Qwen and get a tax-related response.

        Args:
            user_message: The user's question about taxes
            context: Retrieved context from RAG knowledge base
            conversation_history: Previous messages for multi-turn conversation

        Returns:
            AI-generated response about Indonesian taxation
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history for multi-turn
        if conversation_history:
            for msg in conversation_history[-6:]:  # Keep last 6 messages for context
                messages.append(msg)

        # Build user message with RAG context
        if context:
            enhanced_message = (
                f"KONTEKS DARI KNOWLEDGE BASE:\n{context}\n\n"
                f"PERTANYAAN PENGGUNA:\n{user_message}"
            )
        else:
            enhanced_message = user_message

        messages.append({"role": "user", "content": enhanced_message})

        # Call Qwen API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,  # Lower temperature for factual tax answers
            max_tokens=2048,
        )

        return response.choices[0].message.content
