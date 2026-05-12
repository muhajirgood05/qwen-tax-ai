<template>
  <div class="calculator">
    <div class="calc-card">
      <h2>🧮 Kalkulator PPh 21</h2>
      <p class="calc-desc">Hitung pajak penghasilan karyawan berdasarkan UU HPP</p>

      <form @submit.prevent="calculate" class="calc-form">
        <div class="form-group">
          <label>Gaji Bruto per Bulan (Rp)</label>
          <input
            v-model.number="form.gross_monthly_salary"
            type="number"
            placeholder="15000000"
            required
            min="1"
          />
        </div>

        <div class="form-group">
          <label>Status PTKP</label>
          <select v-model="form.status">
            <option value="TK/0">TK/0 - Tidak Kawin, 0 tanggungan</option>
            <option value="TK/1">TK/1 - Tidak Kawin, 1 tanggungan</option>
            <option value="TK/2">TK/2 - Tidak Kawin, 2 tanggungan</option>
            <option value="TK/3">TK/3 - Tidak Kawin, 3 tanggungan</option>
            <option value="K/0">K/0 - Kawin, 0 tanggungan</option>
            <option value="K/1">K/1 - Kawin, 1 tanggungan</option>
            <option value="K/2">K/2 - Kawin, 2 tanggungan</option>
            <option value="K/3">K/3 - Kawin, 3 tanggungan</option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Iuran BPJS (%)</label>
            <input
              v-model.number="form.bpjs_percentage"
              type="number"
              step="0.001"
              min="0"
              max="0.1"
            />
          </div>
          <div class="form-group">
            <label>Potongan Lain/Bulan (Rp)</label>
            <input
              v-model.number="form.other_deductions"
              type="number"
              min="0"
              placeholder="0"
            />
          </div>
        </div>

        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Menghitung...' : 'Hitung PPh 21' }}
        </button>
      </form>
    </div>

    <!-- Results -->
    <div v-if="result" class="result-card">
      <h3>📊 Hasil Perhitungan</h3>

      <div class="result-summary">
        <div class="summary-item highlight">
          <span class="label">PPh 21 per Bulan</span>
          <span class="value">{{ formatCurrency(result.pph21_monthly) }}</span>
        </div>
        <div class="summary-item highlight">
          <span class="label">PPh 21 per Tahun</span>
          <span class="value">{{ formatCurrency(result.pph21_annual) }}</span>
        </div>
        <div class="summary-item">
          <span class="label">Tarif Efektif</span>
          <span class="value">{{ result.effective_rate }}%</span>
        </div>
      </div>

      <details class="breakdown">
        <summary>📋 Detail Perhitungan</summary>
        <table>
          <tbody>
            <tr>
              <td>Penghasilan Bruto/Tahun</td>
              <td class="right">{{ formatCurrency(result.gross_annual) }}</td>
            </tr>
            <tr>
              <td>(-) Biaya Jabatan</td>
              <td class="right">{{ formatCurrency(result.biaya_jabatan) }}</td>
            </tr>
            <tr>
              <td>(-) Iuran BPJS/Tahun</td>
              <td class="right">{{ formatCurrency(result.bpjs_annual) }}</td>
            </tr>
            <tr v-if="result.other_deductions_annual > 0">
              <td>(-) Potongan Lain/Tahun</td>
              <td class="right">{{ formatCurrency(result.other_deductions_annual) }}</td>
            </tr>
            <tr class="bold">
              <td>Penghasilan Neto/Tahun</td>
              <td class="right">{{ formatCurrency(result.net_annual) }}</td>
            </tr>
            <tr>
              <td>(-) PTKP</td>
              <td class="right">{{ formatCurrency(result.ptkp) }}</td>
            </tr>
            <tr class="bold">
              <td>PKP (Penghasilan Kena Pajak)</td>
              <td class="right">{{ formatCurrency(result.pkp) }}</td>
            </tr>
          </tbody>
        </table>

        <h4>Perhitungan Progresif:</h4>
        <table v-if="result.breakdown.length">
          <thead>
            <tr>
              <th>Lapisan</th>
              <th>Tarif</th>
              <th>PKP di Lapisan</th>
              <th>Pajak</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(b, i) in result.breakdown" :key="i">
              <td>{{ b.bracket }}</td>
              <td>{{ b.rate }}</td>
              <td class="right">{{ formatCurrency(b.taxable_amount) }}</td>
              <td class="right">{{ formatCurrency(b.tax) }}</td>
            </tr>
          </tbody>
        </table>
      </details>
    </div>

    <!-- Error -->
    <div v-if="error" class="error-card">
      <p>❌ {{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { calculatePPh21 } from '../services/api.js'

const form = ref({
  gross_monthly_salary: 15000000,
  status: 'K/1',
  bpjs_percentage: 0.01,
  other_deductions: 0,
})

const result = ref(null)
const error = ref('')
const isLoading = ref(false)

async function calculate() {
  isLoading.value = true
  error.value = ''
  result.value = null

  try {
    result.value = await calculatePPh21(form.value)
  } catch (err) {
    error.value = err.message || 'Terjadi kesalahan saat menghitung'
  } finally {
    isLoading.value = false
  }
}

function formatCurrency(value) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}
</script>

<style scoped>
.calculator {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.calc-card,
.result-card,
.error-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.calc-card h2 {
  margin-bottom: 0.25rem;
}

.calc-desc {
  color: #718096;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.calc-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
}

.form-group input,
.form-group select {
  padding: 0.6rem 0.8rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #3182ce;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.calc-form button {
  padding: 0.75rem;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 0.5rem;
}

.calc-form button:hover:not(:disabled) {
  background: #2c5282;
}

.calc-form button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

.result-card h3 {
  margin-bottom: 1rem;
}

.result-summary {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.summary-item {
  text-align: center;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
}

.summary-item.highlight {
  background: #ebf8ff;
  border: 1px solid #bee3f8;
}

.summary-item .label {
  display: block;
  font-size: 0.8rem;
  color: #718096;
  margin-bottom: 0.25rem;
}

.summary-item .value {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  color: #2d3748;
}

.breakdown {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.breakdown summary {
  cursor: pointer;
  font-weight: 600;
  color: #3182ce;
  margin-bottom: 1rem;
}

.breakdown table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

.breakdown th,
.breakdown td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid #edf2f7;
}

.breakdown th {
  background: #f7fafc;
  font-weight: 600;
}

.breakdown .right {
  text-align: right;
}

.breakdown .bold td {
  font-weight: 700;
  background: #f7fafc;
}

.breakdown h4 {
  margin: 1rem 0 0.5rem;
  font-size: 0.9rem;
  color: #4a5568;
}

.error-card {
  background: #fff5f5;
  border: 1px solid #fc8181;
  color: #c53030;
}
</style>
