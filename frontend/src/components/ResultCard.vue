<template>
  <div v-if="result" class="panel result-panel">
    <!-- Header -->
    <div class="result-top">
      <div>
        <span class="game-name">{{ result.game_title }}</span>
        <span class="preset-meta">{{ result.resolution }} • Preset {{ result.preset }}</span>
      </div>
      <div class="badge" :class="statusBadgeClass">
        {{ result.bottleneck_status }}
      </div>
    </div>

    <!-- Main FPS Numbers with Smooth Animated Counting -->
    <div class="metrics-grid">
      <div class="metric-card">
        <span class="metric-lbl">ESTIMASI AVERAGE FPS</span>
        <div class="metric-num-wrap">
          <span class="metric-num">{{ displayAvgFps }}</span>
          <span class="metric-unit">FPS</span>
        </div>
        <span class="tier-label" :style="{ color: getFpsColor(displayAvgFps) }">
          {{ getFpsStatus(displayAvgFps) }}
        </span>
      </div>

      <div class="metric-card">
        <span class="metric-lbl">1% LOW (KELANCARAN)</span>
        <div class="metric-num-wrap">
          <span class="metric-num num-secondary">{{ displayLowFps }}</span>
          <span class="metric-unit">FPS</span>
        </div>
        <span class="tier-sub">
          Penurunan frame: {{ displayAvgFps > 0 ? Math.round((1 - (displayLowFps / displayAvgFps)) * 100) : 0 }}%
        </span>
      </div>
    </div>

    <!-- Target Refresh Rate Compatibility Checklist with pop animation -->
    <div class="hz-checklist">
      <span class="hz-title">Kesesuaian Monitor Gaming:</span>
      <div class="hz-items">
        <div class="hz-badge" :class="{ pass: displayAvgFps >= 60 }">
          <span class="hz-icon">{{ displayAvgFps >= 60 ? '✓' : '✗' }}</span>
          <span>60 Hz (Standard)</span>
        </div>
        <div class="hz-badge" :class="{ pass: displayAvgFps >= 120 }">
          <span class="hz-icon">{{ displayAvgFps >= 120 ? '✓' : '✗' }}</span>
          <span>120 Hz (Gaming)</span>
        </div>
        <div class="hz-badge" :class="{ pass: displayAvgFps >= 144 }">
          <span class="hz-icon">{{ displayAvgFps >= 144 ? '✓' : '✗' }}</span>
          <span>144 Hz (Kompetitif)</span>
        </div>
        <div class="hz-badge" :class="{ pass: displayAvgFps >= 240 }">
          <span class="hz-icon">{{ displayAvgFps >= 240 ? '✓' : '✗' }}</span>
          <span>240 Hz (eSports)</span>
        </div>
      </div>
    </div>

    <!-- Bottleneck Balance Bar with Smooth Width Transition -->
    <div class="bottleneck-section">
      <div class="bar-top">
        <span class="bar-title">Beban Hardware (Bottleneck: {{ result.bottleneck_pct }}%)</span>
        <div class="util-split">
          <span class="cpu-txt">CPU: {{ result.cpu_utilization_est }}%</span>
          <span class="gpu-txt">GPU: {{ result.gpu_utilization_est }}%</span>
        </div>
      </div>
      <div class="bar-track">
        <div 
          class="bar-seg cpu-bar" 
          :style="{ width: `${cpuPercent}%` }"
        >
          CPU
        </div>
        <div 
          class="bar-seg gpu-bar" 
          :style="{ width: `${gpuPercent}%` }"
        >
          GPU
        </div>
      </div>
    </div>

    <!-- Estimated Scaling Across Resolutions Matrix -->
    <div class="res-scaling-box">
      <span class="res-matrix-title">📊 Perkiraan di Resolusi Lain (Preset {{ result.preset }}):</span>
      <div class="res-matrix-grid">
        <div class="res-card" :class="{ 'current-res': result.resolution === '1080p' }">
          <span class="rc-label">1080p FHD</span>
          <span class="rc-fps">{{ getScaledFps('1080p') }} FPS</span>
          <span class="rc-sub">{{ result.resolution === '1080p' ? 'Aktif' : 'Perkiraan' }}</span>
        </div>
        <div class="res-card" :class="{ 'current-res': result.resolution === '1440p' }">
          <span class="rc-label">1440p QHD</span>
          <span class="rc-fps">{{ getScaledFps('1440p') }} FPS</span>
          <span class="rc-sub">{{ result.resolution === '1440p' ? 'Aktif' : 'Perkiraan' }}</span>
        </div>
        <div class="res-card" :class="{ 'current-res': result.resolution === '4K' }">
          <span class="rc-label">4K UHD</span>
          <span class="rc-fps">{{ getScaledFps('4K') }} FPS</span>
          <span class="rc-sub">{{ result.resolution === '4K' ? 'Aktif' : 'Perkiraan' }}</span>
        </div>
      </div>
    </div>

    <!-- Component Info -->
    <div class="specs-summary">
      <div class="summary-item">
        <span class="s-lbl">CPU Terpilih</span>
        <span class="s-val">{{ result.cpu_name }}</span>
      </div>
      <div class="summary-item">
        <span class="s-lbl">GPU Terpilih</span>
        <span class="s-val">{{ result.gpu_name }}</span>
      </div>
      <div class="summary-item">
        <span class="s-lbl">RAM</span>
        <span class="s-val">{{ result.ram_gb }} GB</span>
      </div>
    </div>

    <!-- Verdict -->
    <div class="verdict-box" :class="{ 'verdict-warn': result.bottleneck_status !== 'Balanced / Optimal' }">
      <div class="verdict-text">{{ result.verdict }}</div>
      <div class="verdict-rec"><strong>Saran:</strong> {{ result.recommendation }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  result: {
    type: Object,
    default: null
  }
})

const displayAvgFps = ref(0)
const displayLowFps = ref(0)
let animationFrameId = null

// Smooth Counter Animation
const animateNumbers = (targetAvg, targetLow) => {
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  
  const startAvg = displayAvgFps.value || 0
  const startLow = displayLowFps.value || 0
  const duration = 400 // ms
  const startTime = performance.now()

  const step = (now) => {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)
    
    // Ease out cubic
    const ease = 1 - Math.pow(1 - progress, 3)

    displayAvgFps.value = Math.round(startAvg + (targetAvg - startAvg) * ease)
    displayLowFps.value = Math.round(startLow + (targetLow - startLow) * ease)

    if (progress < 1) {
      animationFrameId = requestAnimationFrame(step)
    } else {
      displayAvgFps.value = targetAvg
      displayLowFps.value = targetLow
    }
  }

  animationFrameId = requestAnimationFrame(step)
}

watch(() => props.result, (newRes) => {
  if (newRes) {
    animateNumbers(newRes.avg_fps, newRes.one_percent_low_fps)
  }
}, { immediate: true })

const cpuPercent = computed(() => {
  if (!props.result) return 50
  const total = props.result.cpu_utilization_est + props.result.gpu_utilization_est
  return total > 0 ? (props.result.cpu_utilization_est / total) * 100 : 50
})

const gpuPercent = computed(() => {
  return 100 - cpuPercent.value
})

const statusBadgeClass = computed(() => {
  if (!props.result) return ''
  if (props.result.bottleneck_status === 'Balanced / Optimal') return 'badge-optimal'
  if (props.result.bottleneck_pct > 25) return 'badge-danger'
  return 'badge-warning'
})

const getFpsColor = (fps) => {
  if (fps >= 60) return '#4ade80'
  if (fps >= 40) return '#fbbf24'
  return '#f87171'
}

const getFpsStatus = (fps) => {
  if (fps >= 144) return 'Sangat Lancar (144Hz+)'
  if (fps >= 60) return 'Lancar Stabil (60 FPS)'
  if (fps >= 30) return 'Cukup (30-60 FPS)'
  return 'Patah-patah (<30 FPS)'
}

const getScaledFps = (targetRes) => {
  if (!props.result) return 0
  if (targetRes === props.result.resolution) {
    return props.result.avg_fps
  }
  let factor = 1.0
  if (props.result.resolution === '1080p') {
    if (targetRes === '1440p') factor = 0.72
    if (targetRes === '4K') factor = 0.48
  } else if (props.result.resolution === '1440p') {
    if (targetRes === '1080p') factor = 1.35
    if (targetRes === '4K') factor = 0.65
  } else if (props.result.resolution === '4K') {
    if (targetRes === '1080p') factor = 2.05
    if (targetRes === '1440p') factor = 1.50
  }
  return Math.round(props.result.avg_fps * factor)
}
</script>

<style scoped>
.result-panel {
  margin-top: 24px;
  animation: fadeIn 0.3s ease-out;
}

.result-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.game-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
  margin-right: 10px;
}

.preset-meta {
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* Metrics */
.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

@media (max-width: 550px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
}

.metric-card {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
  text-align: center;
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  border-color: rgba(96, 165, 250, 0.4);
}

.metric-lbl {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-dim);
  letter-spacing: 0.05em;
}

.metric-num-wrap {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 6px;
  margin: 4px 0;
}

.metric-num {
  font-size: 2.8rem;
  font-weight: 800;
  font-family: var(--font-mono);
  color: #f8fafc;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.num-secondary {
  color: #38bdf8;
}

.metric-unit {
  font-size: 0.95rem;
  color: var(--text-dim);
  font-weight: 700;
}

.tier-label {
  font-size: 0.8rem;
  font-weight: 600;
  transition: color 0.3s ease;
}

.tier-sub {
  font-size: 0.75rem;
  color: var(--text-dim);
}

/* Hz Checklist */
.hz-checklist {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.hz-title {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
}

.hz-items {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.hz-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-dim);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.hz-badge.pass {
  background: rgba(34, 197, 94, 0.12);
  color: #4ade80;
  border-color: rgba(34, 197, 94, 0.3);
  animation: popIn 0.3s ease-out;
}

.hz-icon {
  font-weight: 800;
}

/* Bottleneck Bar */
.bottleneck-section {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  margin-bottom: 16px;
}

.bar-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 0.8rem;
}

.bar-title {
  font-weight: 600;
  color: var(--text-muted);
}

.util-split {
  font-family: var(--font-mono);
  font-weight: 600;
  display: flex;
  gap: 12px;
}

.cpu-txt { color: #60a5fa; }
.gpu-txt { color: #38bdf8; }

.bar-track {
  height: 22px;
  display: flex;
  border-radius: 4px;
  overflow: hidden;
  background: #020617;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.bar-seg {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.cpu-bar { background: #2563eb; }
.gpu-bar { background: #0284c7; }

/* Res Scaling Box */
.res-scaling-box {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  margin-bottom: 16px;
}

.res-matrix-title {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
  display: block;
  margin-bottom: 8px;
}

.res-matrix-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.res-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}

.res-card:hover {
  transform: translateY(-1px);
}

.res-card.current-res {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
}

.rc-label {
  font-size: 0.72rem;
  color: var(--text-dim);
  font-weight: 700;
}

.rc-fps {
  font-size: 1.1rem;
  font-weight: 800;
  font-family: var(--font-mono);
  color: var(--text-main);
}

.rc-sub {
  font-size: 0.68rem;
  color: var(--text-muted);
}

/* Component Summary */
.specs-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}

.summary-item {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
}

.s-lbl {
  font-size: 0.7rem;
  color: var(--text-dim);
  font-weight: 600;
}

.s-val {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}

/* Verdict */
.verdict-box {
  background: var(--bg-input);
  border-left: 3px solid var(--success);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 12px 16px;
  font-size: 0.85rem;
  transition: all 0.25s ease;
}

.verdict-warn {
  border-left-color: var(--warning);
}

.verdict-text {
  color: var(--text-main);
  margin-bottom: 4px;
}

.verdict-rec {
  color: var(--text-muted);
}
</style>
