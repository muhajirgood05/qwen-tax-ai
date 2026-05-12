<template>
  <div :class="['message', message.role, { error: message.isError }]">
    <div class="avatar">
      {{ message.role === 'user' ? '👤' : '🤖' }}
    </div>
    <div class="bubble">
      <div class="content" v-html="formatContent(message.content)"></div>
      <div v-if="message.sources?.length" class="sources">
        <strong>📚 Sumber:</strong>
        <span v-for="(src, i) in message.sources" :key="i">
          {{ src }}{{ i < message.sources.length - 1 ? ' · ' : '' }}
        </span>
      </div>
      <div v-if="message.disclaimer" class="disclaimer">
        {{ message.disclaimer }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: Object,
    required: true,
  },
})

function formatContent(text) {
  if (!text) return ''
  // Basic markdown-like formatting
  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
}
</script>

<style scoped>
.message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  align-items: flex-start;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.bubble {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  line-height: 1.5;
  font-size: 0.9rem;
}

.message.user .bubble {
  background: #3182ce;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .bubble {
  background: #f7fafc;
  border: 1px solid #e2e8f0;
  border-bottom-left-radius: 4px;
}

.message.error .bubble {
  background: #fff5f5;
  border-color: #fc8181;
  color: #c53030;
}

.content :deep(code) {
  background: rgba(0, 0, 0, 0.06);
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-size: 0.85em;
}

.sources {
  margin-top: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e2e8f0;
  font-size: 0.8rem;
  color: #718096;
}

.disclaimer {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #a0aec0;
  font-style: italic;
}
</style>
