<template>
  <div class="chat-window">
    <div class="messages" ref="messagesContainer">
      <!-- Welcome message -->
      <div v-if="messages.length === 0" class="welcome">
        <div class="welcome-icon">🤖</div>
        <h2>Halo! Saya Asisten Pajak AI</h2>
        <p>Tanyakan apa saja tentang perpajakan Indonesia. Contoh:</p>
        <div class="suggestions">
          <button @click="sendSuggestion(s)" v-for="s in suggestions" :key="s">
            {{ s }}
          </button>
        </div>
      </div>

      <!-- Message bubbles -->
      <MessageBubble
        v-for="(msg, index) in messages"
        :key="index"
        :message="msg"
      />

      <!-- Loading indicator -->
      <div v-if="isLoading" class="loading">
        <div class="typing-indicator">
          <span></span><span></span><span></span>
        </div>
        <p>Sedang berpikir...</p>
      </div>
    </div>

    <!-- Input area -->
    <div class="input-area">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="Tanyakan tentang pajak Indonesia..."
        :disabled="isLoading"
      />
      <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
        Kirim
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { sendChatMessage } from '../services/api.js'
import MessageBubble from './MessageBubble.vue'

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

const suggestions = [
  'Berapa tarif PPh 21 terbaru?',
  'Bagaimana cara lapor SPT online?',
  'Apa saja yang tidak kena PPN?',
  'Hitung PPh 21 gaji Rp 15 juta/bulan status K/1',
]

async function sendMessage() {
  const message = userInput.value.trim()
  if (!message || isLoading.value) return

  // Add user message
  messages.value.push({ role: 'user', content: message })
  userInput.value = ''
  isLoading.value = true

  await scrollToBottom()

  try {
    // Build conversation history for context
    const history = messages.value
      .filter((m) => m.role !== 'system')
      .map((m) => ({ role: m.role, content: m.content }))

    const response = await sendChatMessage(message, history.slice(0, -1))

    // Add AI response
    messages.value.push({
      role: 'assistant',
      content: response.reply,
      sources: response.sources,
      disclaimer: response.disclaimer,
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: `Maaf, terjadi kesalahan: ${error.message}. Pastikan backend sudah berjalan.`,
      isError: true,
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

function sendSuggestion(text) {
  userInput.value = text
  sendMessage()
}

async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 220px);
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.welcome {
  text-align: center;
  padding: 2rem 1rem;
}

.welcome-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.welcome h2 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.welcome p {
  color: #718096;
  margin-bottom: 1rem;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.suggestions button {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  background: #f7fafc;
  color: #4a5568;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.suggestions button:hover {
  background: #edf2f7;
  border-color: #3182ce;
  color: #3182ce;
}

.loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  color: #718096;
  font-size: 0.85rem;
}

.typing-indicator {
  display: flex;
  gap: 4px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #a0aec0;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: 0s; }
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.input-area {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  background: #f7fafc;
}

.input-area input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.input-area input:focus {
  border-color: #3182ce;
}

.input-area button {
  padding: 0.75rem 1.5rem;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s;
}

.input-area button:hover:not(:disabled) {
  background: #2c5282;
}

.input-area button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}
</style>
