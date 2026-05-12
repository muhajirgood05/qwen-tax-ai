# Building an AI Tax Assistant for Indonesia with Qwen

## How I Used Alibaba Cloud's Qwen LLM to Create a Smart Tax Consultation Tool

![Qwen Tax AI Banner](https://img.shields.io/badge/Powered%20by-Qwen%20AI-blue)

---

As a **tax auditor** in Indonesia's government with a background in both Accounting and Information Systems, I've always seen the gap between complex tax regulations and public understanding. Most taxpayers struggle with basic questions: *"How much income tax do I owe?"* or *"How do I file my annual tax return?"*

That's why I built **Qwen Tax AI** — an AI-powered tax consultation assistant that uses Alibaba Cloud's Qwen large language model to help Indonesian taxpayers understand their obligations.

## Why Qwen?

I chose Qwen for several reasons:

1. **Multilingual excellence** — Qwen handles Bahasa Indonesia naturally, understanding tax terminology and responding in clear, accessible language
2. **OpenAI-compatible API** — Easy integration via DashScope with familiar SDK patterns
3. **Cost-effective** — Free tier with 1M tokens is more than enough for development and demos
4. **Open-source ecosystem** — Aligns with my goal of making tax knowledge accessible to everyone

## Architecture

The application uses a simple but effective stack:

```
Vue.js 3 (Frontend) → FastAPI (Backend) → Qwen API (DashScope)
                              ↓
                    Tax Knowledge Base (RAG)
```

### Key Components:

- **RAG (Retrieval Augmented Generation)** — Before sending questions to Qwen, the system retrieves relevant tax regulations from a curated knowledge base. This ensures answers are grounded in actual Indonesian tax law.
- **PPh 21 Calculator** — A deterministic tax calculator that computes income tax based on UU HPP progressive rates, PTKP status, and deductions.
- **Conversational AI** — Multi-turn chat with context awareness for follow-up questions.

## The Tax Domain Challenge

Tax consultation is a unique AI challenge because:

- **Accuracy is critical** — Wrong tax advice can lead to penalties
- **Regulations change frequently** — UU HPP (2021), PP 58/2023, PMK 168/2023
- **Context matters** — The same question has different answers depending on taxpayer status

My solution combines Qwen's language understanding with a structured knowledge base and explicit disclaimers. The system prompt is carefully engineered to:

1. Always cite relevant regulations (UU, PP, PMK)
2. Refuse to give advice on tax avoidance
3. Recommend professional consultation for complex cases
4. Show calculation steps transparently

## Code Highlights

### Qwen API Integration

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

response = await client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    temperature=0.3,  # Low temperature for factual tax answers
)
```

### Progressive Tax Calculation

```python
TAX_BRACKETS = [
    (60_000_000, 0.05),    # 5% for first Rp 60M
    (250_000_000, 0.15),   # 15% for Rp 60M - 250M
    (500_000_000, 0.25),   # 25% for Rp 250M - 500M
    (5_000_000_000, 0.30), # 30% for Rp 500M - 5B
    (float("inf"), 0.35),  # 35% above Rp 5B
]
```

## Results

The assistant accurately handles:

- ✅ PPh 21 tariff explanations with UU HPP references
- ✅ PTKP calculations for all status categories
- ✅ Step-by-step SPT filing guidance
- ✅ PPN (VAT) regulations and exemptions
- ✅ Multi-turn conversations with context retention

**Example interaction:**

> **User:** "Berapa tarif PPh 21 untuk penghasilan Rp 100 juta per tahun?"
>
> **AI:** "Berdasarkan UU HPP Pasal 17, penghasilan kena pajak Rp 100 juta dikenakan tarif progresif:
> - Rp 0 - 60 juta: 5% = Rp 3.000.000
> - Rp 60 juta - 100 juta: 15% = Rp 6.000.000
> - **Total PPh 21: Rp 9.000.000**"

## What I Learned

1. **Prompt engineering matters** — A well-crafted system prompt with embedded tax knowledge dramatically improves response quality
2. **RAG adds reliability** — Grounding responses in actual regulation text reduces hallucination
3. **Domain expertise + AI = powerful combination** — My tax auditing background helped me validate AI responses and design better prompts
4. **Qwen's multilingual capability is impressive** — It handles Indonesian tax jargon (PKP, PTKP, SPT, e-Filing) naturally

## What's Next

- [ ] Add TER (Tarif Efektif Rata-rata) calculation per PP 58/2023
- [ ] Integrate with e-Filing deadline reminders
- [ ] Add document upload for Bukti Potong analysis
- [ ] Deploy as a public demo on Vercel/Railway

## Try It Yourself

The project is open-source: [github.com/muhajirgood05/qwen-tax-ai](https://github.com/muhajirgood05/qwen-tax-ai)

---

*Built with Qwen by Alibaba Cloud. This project demonstrates how AI can make government services more accessible to citizens.*

---

**About the Author**

Ahmad Muhajir is a tax auditor in Indonesia's civil service with dual degrees in Accounting and Information Systems. He's passionate about applying AI to improve public services and is currently pursuing opportunities in AI/IT graduate studies.

- GitHub: [@muhajirgood05](https://github.com/muhajirgood05)
- LinkedIn: [Ahmad Muhajir](https://www.linkedin.com/in/ahmad-muhajir-a64506221/)

---

*Tags: #Qwen #AI #Indonesia #Tax #OpenSource #AlibabaCloud #LLM #FastAPI #VueJS*
