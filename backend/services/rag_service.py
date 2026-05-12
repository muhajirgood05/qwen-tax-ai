"""
Simple RAG (Retrieval Augmented Generation) Service.
Retrieves relevant tax regulation context from the knowledge base.
"""

import os
from pathlib import Path


class RAGService:
    """Simple keyword-based RAG service for tax knowledge retrieval."""

    def __init__(self):
        self.knowledge_dir = Path(__file__).parent.parent / "knowledge"
        self.documents = self._load_documents()

    def _load_documents(self) -> dict[str, str]:
        """Load all markdown documents from knowledge directory."""
        docs = {}
        if not self.knowledge_dir.exists():
            return docs

        for file_path in self.knowledge_dir.glob("*.md"):
            with open(file_path, "r", encoding="utf-8") as f:
                docs[file_path.stem] = f.read()

        return docs

    def retrieve(self, query: str, top_k: int = 2) -> str:
        """
        Retrieve relevant context based on keyword matching.

        Args:
            query: User's question
            top_k: Number of top documents to return

        Returns:
            Combined relevant context string
        """
        query_lower = query.lower()

        # Keyword mapping to documents
        keyword_map = {
            "pph21": ["pph", "penghasilan", "gaji", "salary", "tarif", "ptkp",
                      "karyawan", "pegawai", "potong", "21"],
            "ppn": ["ppn", "pertambahan nilai", "vat", "faktur", "pkp",
                    "keluaran", "masukan", "11%"],
            "spt_guide": ["spt", "lapor", "pelaporan", "efiling", "djp online",
                          "1770", "tahunan", "batas waktu", "deadline"],
        }

        # Score each document
        scores = {}
        for doc_name, keywords in keyword_map.items():
            if doc_name in self.documents:
                score = sum(1 for kw in keywords if kw in query_lower)
                if score > 0:
                    scores[doc_name] = score

        # Sort by score and get top_k
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_docs = sorted_docs[:top_k]

        # Combine context
        context_parts = []
        for doc_name, _ in top_docs:
            context_parts.append(f"--- {doc_name.upper()} ---\n{self.documents[doc_name]}")

        return "\n\n".join(context_parts) if context_parts else ""

    def get_sources(self, query: str) -> list[str]:
        """Get source references for the query."""
        query_lower = query.lower()
        sources = []

        source_map = {
            "pph": "UU No. 7/2021 (UU HPP) - Pajak Penghasilan",
            "ppn": "UU No. 7/2021 (UU HPP) - PPN",
            "spt": "PER-02/PJ/2019 - Tata Cara Penyampaian SPT",
            "ptkp": "PMK No. 101/PMK.010/2016 - PTKP",
            "tarif": "PP No. 58/2023 - Tarif Pemotongan PPh 21",
        }

        for keyword, source in source_map.items():
            if keyword in query_lower and source not in sources:
                sources.append(source)

        return sources if sources else ["Regulasi Perpajakan Indonesia"]

    def get_topic_info(self, topic: str) -> str | None:
        """Get full information on a specific topic."""
        return self.documents.get(topic)
