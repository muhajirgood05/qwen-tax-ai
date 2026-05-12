/**
 * API service for Qwen Tax AI backend.
 */

const API_BASE = '/api'

/**
 * Send a chat message to the AI tax assistant.
 * @param {string} message - User's question
 * @param {Array} conversationHistory - Previous messages
 * @returns {Promise<{reply: string, sources: string[], disclaimer: string}>}
 */
export async function sendChatMessage(message, conversationHistory = []) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      conversation_history: conversationHistory,
    }),
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

/**
 * Calculate PPh 21 income tax.
 * @param {Object} params - Calculation parameters
 * @returns {Promise<Object>} Tax calculation result
 */
export async function calculatePPh21(params) {
  const response = await fetch(`${API_BASE}/calculate-pph21`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

/**
 * Get tax information on a specific topic.
 * @param {string} topic - Topic name (pph21, ppn, spt_guide)
 * @returns {Promise<{topic: string, content: string}>}
 */
export async function getTaxInfo(topic) {
  const response = await fetch(`${API_BASE}/tax-info/${topic}`)

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}
