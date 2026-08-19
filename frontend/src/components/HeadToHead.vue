<template>
  <div class="head-to-head-container">
    <div class="section-title-bar">
      <div>
        <h2 class="title-text">Komparasi Spesifikasi Hardware</h2>
        <p class="subtitle-text">Bandingkan spesifikasi dan skor sintetis 2 hingga 4 komponen berdampingan.</p>
      </div>
      <div class="type-toggle">
        <button 
          class="btn-toggle" 
          :class="{ active: compareCategory === 'gpu' }"
          @click="setCategory('gpu')"
        >
          Kartu Grafis (GPU)
        </button>
        <button 
          class="btn-toggle" 
          :class="{ active: compareCategory === 'cpu' }"
          @click="setCategory('cpu')"
        >
          Prosesor (CPU)
        </button>
      </div>
    </div>

    <!-- Search & Select Component Row -->
    <div class="panel selector-box">
      <div class="search-wrap">
        <input 
          type="text" 
          v-model="searchQuery" 
          :placeholder="`Cari dan tambahkan ${compareCategory.toUpperCase()} untuk dibandingkan...`" 
          class="search-input"
          @focus="isDropdownOpen = true"
        />
        <div v-if="isDropdownOpen && filteredCandidates.length" class="dropdown-list">
          <div 
            v-for="item in filteredCandidates" 
            :key="item.id" 
            class="dropdown-item"
            @click="addItem(item)"
          >
            <div class="item-main">
              <span class="item-name">{{ item.brand }} {{ item.name }}</span>
              <span class="badge" :class="item.form_factor === 'laptop' ? 'badge-laptop' : 'badge-desktop'">
                {{ item.form_factor }} {{ item.tgp_watts ? item.tgp_watts + 'W' : '' }}
              </span>
            </div>
            <span class="item-score">Skor: {{ item.multi_score.toLocaleString() }}</span>
          </div>
        </div>
      </div>
      <span class="limit-info">{{ selectedItems.length }}/4 Terpilih</span>
    </div>

    <!-- Comparison Table Matrix -->
    <div v-if="selectedItems.length > 0" class="panel table-wrapper">
      <table class="compare-table">
        <thead>
          <tr>
            <th class="metric-col">Spesifikasi & Metrik</th>
            <th v-for="item in selectedItems" :key="item.id" class="item-col">
              <div class="item-th-header">
                <button class="remove-btn" @click="removeItem(item.id)">✕</button>
                <div class="badge" :class="item.form_factor === 'laptop' ? 'badge-laptop' : 'badge-desktop'">
                  {{ item.form_factor }}
                </div>
                <div class="item-th-name">{{ item.brand }} {{ item.name }}</div>
                <div v-if="item.tgp_watts" class="tgp-sub">TGP: {{ item.tgp_watts }}W</div>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="metric-label">Form Factor</td>
            <td v-for="item in selectedItems" :key="item.id" class="val-cell">
              {{ item.form_factor.toUpperCase() }}
            </td>
          </tr>
          <tr>
            <td class="metric-label">
              {{ compareCategory === 'cpu' ? 'Single-Core Benchmark' : 'Compute Score' }}
            </td>
            <td v-for="item in selectedItems" :key="item.id" class="val-cell">
              <div class="bar-num-group">
                <span class="metric-number">{{ item.single_score.toLocaleString() }}</span>
                <div class="score-bar-bg">
                  <div 
                    class="score-bar-fill" 
                    :style="{ width: `${(item.single_score / maxSingleScore) * 100}%` }"
                  ></div>
                </div>
              </div>
            </td>
          </tr>
          <tr>
            <td class="metric-label">
              {{ compareCategory === 'cpu' ? 'Multi-Core Score' : '3D Graphic Score' }}
            </td>
            <td v-for="item in selectedItems" :key="item.id" class="val-cell">
              <div class="bar-num-group">
                <span class="metric-number highlight-blue">{{ item.multi_score.toLocaleString() }}</span>
                <div class="score-bar-bg">
                  <div 
                    class="score-bar-fill fill-blue" 
                    :style="{ width: `${(item.multi_score / maxMultiScore) * 100}%` }"
                  ></div>
                </div>
              </div>
            </td>
          </tr>
          <tr>
            <td class="metric-label">Base / Boost Clock</td>
            <td v-for="item in selectedItems" :key="item.id" class="val-cell">
              {{ item.base_clock_ghz || '-' }} GHz / {{ item.boost_clock_ghz || '-' }} GHz
            </td>
          </tr>
          <tr v-if="compareCategory === 'gpu'">
            <td class="metric-label">Kapasitas VRAM</td>
            <td v-for="item in selectedItems" :key="item.id" class="val-cell">
              {{ item.vram_gb ? item.vram_gb + ' GB GDDR' : '-' }}
            </td>
          </tr>
          <tr>
            <td class="metric-label">Tahun Rilis</td>
            <td v-for="item in selectedItems" :key="item.id" class="val-cell">
              {{ item.release_year }}
            </td>
          </tr>
          <tr>
            <td class="metric-label">Performa Relatif</td>
            <td v-for="item in selectedItems" :key="item.id" class="val-cell">
              <span class="perf-delta" :class="{ 'perf-lead': item.multi_score === maxMultiScore }">
                {{ Math.round((item.multi_score / maxMultiScore) * 100) }}% Relatif
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="empty-state panel">
      <p>Pilih minimal 2 komponen hardware pada kolom pencarian di atas untuk mulai membandingkan.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  hardwareList: {
    type: Array,
    default: () => []
  }
})

const compareCategory = ref('gpu')
const searchQuery = ref('')
const isDropdownOpen = ref(false)
const selectedIds = ref([])

const setCategory = (cat) => {
  compareCategory.value = cat
  selectedIds.value = []
  searchQuery.value = ''
}

const currentCategoryPool = computed(() => {
  return props.hardwareList.filter(item => item.category === compareCategory.value)
})

const filteredCandidates = computed(() => {
  const pool = currentCategoryPool.value.filter(item => !selectedIds.value.includes(item.id))
  if (!searchQuery.value.trim()) return pool.slice(0, 8)
  const q = searchQuery.value.toLowerCase()
  return pool.filter(item => item.name.toLowerCase().includes(q) || item.brand.toLowerCase().includes(q)).slice(0, 10)
})

const selectedItems = computed(() => {
  return selectedIds.value.map(id => props.hardwareList.find(item => item.id === id)).filter(Boolean)
})

const maxSingleScore = computed(() => {
  if (!selectedItems.value.length) return 1
  return Math.max(...selectedItems.value.map(i => i.single_score)) || 1
})

const maxMultiScore = computed(() => {
  if (!selectedItems.value.length) return 1
  return Math.max(...selectedItems.value.map(i => i.multi_score)) || 1
})

const addItem = (item) => {
  if (selectedIds.value.length >= 4) return
  selectedIds.value.push(item.id)
  searchQuery.value = ''
  isDropdownOpen.value = false
}

const removeItem = (id) => {
  selectedIds.value = selectedIds.value.filter(i => i !== id)
}

onMounted(() => {
  const initialPool = props.hardwareList.filter(i => i.category === 'gpu')
  const defaultSeeds = initialPool.filter(i => 
    i.name.includes('RTX 4060 Laptop (140W)') || 
    i.name.includes('RTX 4060 Laptop (45W)') || 
    (i.name === 'GeForce RTX 4060' && i.form_factor === 'desktop')
  )
  if (defaultSeeds.length > 0) {
    selectedIds.value = defaultSeeds.map(s => s.id)
  }
})
</script>

<style scoped>
.head-to-head-container {
  margin-top: 10px;
}

.section-title-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.title-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
}

.subtitle-text {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.type-toggle {
  display: flex;
  background: var(--bg-input);
  border-radius: var(--radius-sm);
  padding: 3px;
  border: 1px solid var(--border-color);
}

.btn-toggle {
  background: transparent;
  border: none;
  color: var(--text-muted);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-toggle.active {
  background: var(--primary);
  color: white;
}

.selector-box {
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  margin-bottom: 20px;
}

.search-wrap {
  flex: 1;
  position: relative;
}

.search-input {
  width: 100%;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  color: white;
  font-size: 0.88rem;
}

.search-input:focus {
  outline: none;
  border-color: var(--border-focus);
}

.dropdown-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  z-index: 50;
  max-height: 240px;
  overflow-y: auto;
  box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}

.dropdown-item {
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.dropdown-item:hover {
  background: var(--bg-surface-elevated);
}

.item-main {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-name {
  font-size: 0.88rem;
  font-weight: 600;
}

.item-score {
  font-size: 0.8rem;
  color: #38bdf8;
  font-family: var(--font-mono);
}

.limit-info {
  font-size: 0.8rem;
  color: var(--text-dim);
  font-weight: 600;
}

/* Table */
.table-wrapper {
  overflow-x: auto;
  padding: 0;
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.compare-table th,
.compare-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
}

.metric-col {
  width: 220px;
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
  background: var(--bg-input);
}

.item-th-header {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.remove-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(248, 113, 113, 0.15);
  color: #f87171;
  border: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.7rem;
}

.item-th-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
}

.tgp-sub {
  font-size: 0.75rem;
  color: #c084fc;
}

.metric-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--bg-input);
}

.val-cell {
  font-size: 0.85rem;
  color: var(--text-main);
}

.highlight-blue {
  color: #38bdf8;
  font-weight: 700;
}

.score-bar-bg {
  height: 5px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  margin-top: 4px;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  background: #2563eb;
  border-radius: 3px;
}

.fill-blue {
  background: #0284c7;
}

.metric-number {
  font-family: var(--font-mono);
  font-weight: 700;
}

.perf-delta {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-muted);
}

.perf-lead {
  color: #4ade80;
}

.empty-state {
  padding: 30px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>
