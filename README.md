# 🇮🇩 Qwen Tax AI - Asisten Pajak Indonesia

> AI-powered tax consultation assistant for Indonesian taxpayers, built with Qwen LLM by Alibaba Cloud.

[![Powered by Qwen](https://img.shields.io/badge/Powered%20by-Qwen%20AI-blue)](https://qwen.ai)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-brightgreen)](https://vuejs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Overview

**Qwen Tax AI** adalah asisten pajak berbasis AI yang membantu wajib pajak Indonesia memahami regulasi perpajakan, menghitung kewajiban pajak, dan menjawab pertanyaan umum seputar pajak penghasilan (PPh), PPN, dan administrasi perpajakan.

Proyek ini dibangun menggunakan **Qwen** (Large Language Model dari Alibaba Cloud) melalui OpenAI-compatible API, menunjukkan bagaimana LLM dapat diaplikasikan di domain perpajakan pemerintahan.

## ✨ Features

- 💬 **Chat Konsultasi Pajak** — Tanya jawab interaktif seputar regulasi pajak Indonesia
- 🧮 **Kalkulator PPh 21** — Hitung pajak penghasilan karyawan otomatis
- 📋 **Panduan Pelaporan SPT** — Step-by-step guide pelaporan SPT Tahunan
- 🔍 **RAG (Retrieval Augmented Generation)** — Jawaban akurat berbasis dokumen regulasi pajak
- 🌐 **Bilingual** — Mendukung Bahasa Indonesia dan English

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Vue.js 3      │────▶│   FastAPI        │────▶│   Qwen API      │
│   Frontend      │◀────│   Backend        │◀────│   (DashScope)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │  Tax Knowledge   │
                        │  Base (JSON/MD)  │
                        └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Qwen API Key (get from [Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/what-is-model-studio))

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your DASHSCOPE_API_KEY
python main.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

```env
DASHSCOPE_API_KEY=your_api_key_here
QWEN_MODEL=qwen-plus
```

## 📖 Use Cases

### 1. Konsultasi Pajak Umum
```
User: "Berapa tarif PPh 21 untuk penghasilan Rp 100 juta per tahun?"
AI: "Berdasarkan UU HPP, penghasilan kena pajak Rp 100 juta dikenakan tarif progresif:
     - Rp 0 - 60 juta: 5% = Rp 3.000.000
     - Rp 60 juta - 100 juta: 15% = Rp 6.000.000
     Total PPh 21: Rp 9.000.000"
```

### 2. Kalkulator Pajak
```
User: "Hitung PPh 21 saya: gaji Rp 15 juta/bulan, status K/1, BPJS 1%"
AI: [Menghitung dengan detail lengkap termasuk PTKP, biaya jabatan, dll]
```

### 3. Panduan SPT
```
User: "Bagaimana cara lapor SPT 1770S online?"
AI: [Step-by-step guide dengan screenshot references]
```

## 🧠 How It Works

1. **User Input** — Pengguna mengetik pertanyaan pajak
2. **Context Retrieval** — Sistem mencari regulasi pajak yang relevan dari knowledge base
3. **Prompt Engineering** — Pertanyaan + konteks dikirim ke Qwen dengan system prompt khusus perpajakan
4. **AI Response** — Qwen menghasilkan jawaban yang akurat dan mudah dipahami
5. **Disclaimer** — Setiap jawaban disertai disclaimer bahwa ini bukan pengganti konsultan pajak resmi

## 📁 Project Structure

```
qwen-tax-ai/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── services/
│   │   ├── qwen_client.py   # Qwen API client
│   │   ├── tax_calculator.py # PPh calculation logic
│   │   └── rag_service.py   # RAG retrieval service
│   ├── knowledge/
│   │   ├── pph21.md         # PPh 21 regulations
│   │   ├── ppn.md           # PPN regulations
│   │   └── spt_guide.md    # SPT filing guide
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── components/
│   │   │   ├── ChatWindow.vue
│   │   │   ├── TaxCalculator.vue
│   │   │   └── MessageBubble.vue
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── vite.config.js
├── README.md
└── LICENSE
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Aplikasi ini dibuat untuk tujuan edukasi dan demonstrasi. Jawaban yang diberikan oleh AI **bukan merupakan nasihat pajak resmi**. Untuk keperluan perpajakan yang sebenarnya, silakan konsultasikan dengan konsultan pajak berlisensi atau kunjungi [pajak.go.id](https://pajak.go.id).

## 👤 Author

**Ahmad Muhajir** — Tax Auditor & IT Enthusiast
- GitHub: [@muhajirgood05](https://github.com/muhajirgood05)
- LinkedIn: [Ahmad Muhajir](https://www.linkedin.com/in/ahmad-muhajir-a64506221/)

---

*Built with ❤️ using [Qwen](https://qwen.ai) by Alibaba Cloud*
