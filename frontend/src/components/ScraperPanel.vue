<template>
  <div class="panel scraper-panel">
    <!-- Header -->
    <div class="scraper-header">
      <div class="header-info">
        <h3 class="panel-title">Ground Truth Scraper & Auto-Calibration Engine</h3>
        <p class="panel-desc">
          Pipeline pengumpulan data benchmark riil (NotebookCheck, TechPowerUp) dan kalibrasi otomatis formula matematis berbasis RapidFuzz & Least Squares.
        </p>
      </div>
      <div class="header-actions">
        <button 
          class="btn-primary" 
          :disabled="isSyncing" 
          @click="runGroundTruthScraper"
        >
          {{ isSyncing ? 'Mengkalibrasi...' : '🔄 Scrape & Auto-Kalibrasi' }}
        </button>
      </div>
    </div>

    <!-- Statistical Evaluation Metrics Grid -->
    <div v-if="metrics" class="calib-stats-grid">
      <div class="stat-card">
        <span class="stat-lbl">TINGKAT AKURASI MODEL</span>
        <span class="stat-val stat-green">{{ metrics.accuracy_pct }}%</span>
        <span class="stat-sub">Validasi vs Ground Truth</span>
      </div>

      <div class="stat-card">
        <span class="stat-lbl">MAPE (PERCENTAGE ERROR)</span>
        <span class="stat-val stat-blue">{{ metrics.mape_pct }}%</span>
        <span class="stat-sub">Target KPI: &lt; 8.0%</span>
      </div>

      <div class="stat-card">
        <span class="stat-lbl">KOEFISIEN DETERMINASI (R²)</span>
        <span class="stat-val stat-purple">{{ metrics.r2_score }}</span>
        <span class="stat-sub">Target KPI: &gt; 0.92</span>
      </div>

      <div class="stat-card">
        <span class="stat-lbl">RMSE (RESIDUAL ERROR)</span>
        <span class="stat-val stat-amber">{{ metrics.rmse_fps }} FPS</span>
        <span class="stat-sub">Sampel: {{ metrics.sample_count }} Benchmark Riil</span>
      </div>
    </div>

    <!-- Ground Truth Reference Dataset Table -->
    <div v-if="metrics && metrics.samples && metrics.samples.length" class="gt-table-wrap">
      <div class="gt-table-header">
        <h4 class="gt-title">Sampel Ground Truth Terkalibrasi (RapidFuzz Entity Match)</h4>
        <span class="gt-count">{{ metrics.samples.length }} Pengujian Riil</span>
      </div>
      <div class="table-responsive">
        <table class="gt-table">
          <thead>
            <tr>
              <th>Game Target</th>
              <th>Hardware (CPU & GPU)</th>
              <th>Resolusi</th>
              <th>FPS Riil</th>
              <th>FPS Estimasi</th>
              <th>Deviasi</th>
              <th>Sumber Benchmark</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in metrics.samples" :key="s.id">
              <td class="cell-bold">{{ s.game }}</td>
              <td>
                <div class="hw-stack">
                  <span class="hw-cpu">{{ s.cpu }}</span>
                  <span class="hw-gpu">{{ s.gpu }}</span>
                </div>
              </td>
              <td><span class="res-tag">{{ s.resolution }} {{ s.preset }}</span></td>
              <td class="cell-num">{{ s.real_fps }} FPS</td>
              <td class="cell-num cell-calc">{{ s.calc_fps }} FPS</td>
              <td>
                <span class="err-tag" :class="s.error_pct <= 10 ? 'err-good' : (s.error_pct <= 20 ? 'err-mid' : 'err-warn')">
                  ±{{ s.error_pct }}%
                </span>
              </td>
              <td class="cell-source">{{ s.source }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pipeline Log Console -->
    <div class="console-box">
      <div class="console-title">Log Pipeline & Auto-Calibration:</div>
      <div class="console-logs">
        <div v-for="(log, idx) in logs" :key="idx" class="log-line" :class="log.type">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-msg">{{ log.text }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['data-updated'])

const isSyncing = ref(false)
const metrics = ref(null)
const logs = ref([
  { time: '09:00:00', text: '[INFO] Ground Truth Scraper active. RapidFuzz normalizer initialized.', type: 'info' },
  { time: '09:00:01', text: '[READY] Statistical validation engine ready for auto-calibration.', type: 'success' }
])

const addLog = (text, type = 'info') => {
  const time = new Date().toLocaleTimeString('en-US', { hour12: false })
  logs.value.push({ time, text, type })
}

const fetchMetrics = async () => {
  try {
    const res = await fetch('/api/calibration/metrics')
    if (res.ok) {
      metrics.value = await res.json()
    }
  } catch (err) {
    console.error('Error fetching metrics:', err)
  }
}

const runGroundTruthScraper = async () => {
  isSyncing.value = true
  addLog('[SCRAPER] Mengambil benchmark riil dari NotebookCheck & TechPowerUp...', 'info')
  addLog('[RAPIDFUZZ] Memetakan string varian hardware ke Canonical Database IDs...', 'info')

  try {
    const res = await fetch('/api/scraper/ground-truth/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    const data = await res.json()
    if (res.ok) {
      metrics.value = data.metrics
      addLog(`[SUCCESS] Berhasil memetakan ${data.seeded_count} data ground truth riil.`, 'success')
      addLog(`[CALIBRATION] Akurasi Model: ${data.metrics.accuracy_pct}% (MAPE: ${data.metrics.mape_pct}%, R²: ${data.metrics.r2_score})`, 'success')
      emit('data-updated')
    }
  } catch (err) {
    addLog(`[ERROR] Gagal sinkronisasi: ${err.message}`, 'error')
  } finally {
    isSyncing.value = false
  }
}

onMounted(() => {
  fetchMetrics()
})
</script>

<style scoped>
.scraper-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.scraper-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
}

.header-info {
  flex: 1;
  min-width: 280px;
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 4px;
}

.panel-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.5;
}

/* Calibration Stats Grid */
.calib-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.stat-card {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-lbl {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-dim);
  letter-spacing: 0.05em;
}

.stat-val {
  font-size: 1.8rem;
  font-weight: 800;
  font-family: var(--font-mono);
  margin: 4px 0 2px;
}

.stat-sub {
  font-size: 0.72rem;
  color: var(--text-dim);
}

.stat-green { color: #4ade80; }
.stat-blue { color: #60a5fa; }
.stat-purple { color: #c084fc; }
.stat-amber { color: #fbbf24; }

/* Ground Truth Table */
.gt-table-wrap {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
}

.gt-table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.gt-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
}

.gt-count {
  font-size: 0.78rem;
  color: var(--text-dim);
  font-weight: 600;
}

.table-responsive {
  max-height: 320px;
  overflow-y: auto;
}

.gt-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.gt-table th {
  text-align: left;
  padding: 8px 10px;
  font-size: 0.72rem;
  color: var(--text-dim);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  background: var(--bg-input);
  z-index: 10;
}

.gt-table td {
  padding: 8px 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.cell-bold {
  font-weight: 700;
  color: var(--text-main);
}

.hw-stack {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.hw-cpu {
  color: var(--text-muted);
  font-size: 0.75rem;
}

.hw-gpu {
  color: #60a5fa;
  font-weight: 600;
  font-size: 0.8rem;
}

.res-tag {
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.72rem;
  color: var(--text-muted);
}

.cell-num {
  font-family: var(--font-mono);
  font-weight: 600;
}

.cell-calc {
  color: #38bdf8;
}

.err-tag {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 700;
  font-family: var(--font-mono);
}

.err-good {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
}

.err-mid {
  background: rgba(217, 119, 6, 0.15);
  color: #fbbf24;
}

.err-warn {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.cell-source {
  color: var(--text-dim);
  font-size: 0.72rem;
}

/* Console Box */
.console-box {
  background: #020617;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.console-title {
  color: var(--text-dim);
  font-weight: 700;
  margin-bottom: 8px;
}

.console-logs {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 160px;
  overflow-y: auto;
}

.log-line {
  display: flex;
  gap: 8px;
}

.log-time {
  color: var(--text-dim);
}

.log-line.info .log-msg { color: #60a5fa; }
.log-line.success .log-msg { color: #4ade80; }
.log-line.error .log-msg { color: #f87171; }

.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
