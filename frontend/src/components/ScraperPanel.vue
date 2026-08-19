<template>
  <div class="panel scraper-panel">
    <div class="scraper-header">
      <div class="header-info">
        <h3 class="panel-title">Data Pipeline & Scraper Sync</h3>
        <p class="panel-desc">
          Sinkronisasi data spesifikasi benchmark hardware otomatis dan normalisasi form factor (Laptop vs Desktop TGP).
        </p>
      </div>
      <button 
        class="btn-primary" 
        :disabled="isSyncing" 
        @click="runSampleEtl"
      >
        {{ isSyncing ? 'Memproses Sync...' : 'Jalankan Sync Database' }}
      </button>
    </div>

    <!-- Pipeline Log Console -->
    <div class="console-box">
      <div class="console-title">Log Pipeline:</div>
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
import { ref } from 'vue'

const emit = defineEmits(['data-updated'])

const isSyncing = ref(false)
const logs = ref([
  { time: '09:00:00', text: '[INFO] Cron scheduler active. Automated scraping interval: Weekly.', type: 'info' },
  { time: '09:00:01', text: '[READY] Database schema synchronized with SQLAlchemy.', type: 'success' }
])

const addLog = (text, type = 'info') => {
  const time = new Date().toLocaleTimeString('en-US', { hour12: false })
  logs.value.push({ time, text, type })
}

const runSampleEtl = async () => {
  isSyncing.value = true
  addLog('[ETL] Mengambil raw feed data benchmark hardware...', 'info')

  const sampleRawData = [
    { name: "Core i9-14900KS", brand: "Intel", single_score: 2450, multi_score: 31000, base_clock_ghz: 3.2, boost_clock_ghz: 6.2, release_year: 2024 },
    { name: "GeForce RTX 4070 Ti Super Laptop 140W", brand: "NVIDIA", single_score: 16000, multi_score: 16000, tgp_watts: 140, vram_gb: 12, release_year: 2024 },
    { name: "Ryzen 9 8945HS Laptop", brand: "AMD", single_score: 2000, multi_score: 17500, tgp_watts: 45, release_year: 2024 }
  ]

  setTimeout(async () => {
    addLog(`[NORMALIZER] Menormalisasi form factor dan TGP...`, 'info')
    try {
      const res = await fetch('/api/pipeline/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sampleRawData)
      })
      const data = await res.json()
      addLog(`[UPSERT] Berhasil update ${data.upserted_count} data hardware ke database.`, 'success')
      emit('data-updated')
    } catch (err) {
      addLog(`[ERROR] Gagal sinkronisasi: ${err.message}`, 'error')
    } finally {
      isSyncing.value = false
    }
  }, 800)
}
</script>

<style scoped>
.scraper-panel {
  margin-top: 10px;
}

.scraper-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.panel-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
}

.panel-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.console-box {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 12px;
  font-family: var(--font-mono);
}

.console-title {
  font-size: 0.75rem;
  color: var(--text-dim);
  margin-bottom: 6px;
}

.console-logs {
  max-height: 120px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.log-line {
  font-size: 0.78rem;
  display: flex;
  gap: 8px;
}

.log-time {
  color: var(--text-dim);
}

.log-msg {
  color: var(--text-muted);
}

.success .log-msg {
  color: #4ade80;
}

.error .log-msg {
  color: #f87171;
}
</style>
