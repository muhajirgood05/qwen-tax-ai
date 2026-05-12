<template>
  <div class="app">
    <header class="app-header">
      <div class="header-content">
        <h1>🇮🇩 Qwen Tax AI</h1>
        <p class="subtitle">Asisten Pajak Indonesia berbasis AI</p>
      </div>
      <nav class="tabs">
        <button
          :class="{ active: activeTab === 'chat' }"
          @click="activeTab = 'chat'"
        >
          💬 Konsultasi
        </button>
        <button
          :class="{ active: activeTab === 'calculator' }"
          @click="activeTab = 'calculator'"
        >
          🧮 Kalkulator PPh 21
        </button>
      </nav>
    </header>

    <main class="app-main">
      <ChatWindow v-if="activeTab === 'chat'" />
      <TaxCalculator v-else-if="activeTab === 'calculator'" />
    </main>

    <footer class="app-footer">
      <p>
        Powered by <a href="https://qwen.ai" target="_blank">Qwen AI</a> (Alibaba Cloud)
        · Built by <a href="https://github.com/muhajirgood05" target="_blank">Ahmad Muhajir</a>
      </p>
      <p class="disclaimer">
        ⚠️ Aplikasi ini untuk tujuan edukasi. Bukan nasihat pajak resmi.
      </p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatWindow from './components/ChatWindow.vue'
import TaxCalculator from './components/TaxCalculator.vue'

const activeTab = ref('chat')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f4f8;
  color: #1a202c;
  min-height: 100vh;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

.app-header {
  text-align: center;
  padding: 1.5rem 0 1rem;
}

.app-header h1 {
  font-size: 1.8rem;
  color: #2d3748;
}

.subtitle {
  color: #718096;
  margin-top: 0.25rem;
  font-size: 0.95rem;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-top: 1rem;
}

.tabs button {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  background: #e2e8f0;
  color: #4a5568;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.tabs button.active {
  background: #3182ce;
  color: white;
}

.tabs button:hover:not(.active) {
  background: #cbd5e0;
}

.app-main {
  flex: 1;
  padding: 1rem 0;
}

.app-footer {
  text-align: center;
  padding: 1rem 0;
  font-size: 0.8rem;
  color: #718096;
}

.app-footer a {
  color: #3182ce;
  text-decoration: none;
}

.app-footer a:hover {
  text-decoration: underline;
}

.disclaimer {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #a0aec0;
}
</style>
