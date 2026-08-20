<template>
  <div class="panel">
    <!-- Header Section -->
    <div class="calc-top">
      <div>
        <h2 class="calc-title">Kalkulator Performa & Bottleneck</h2>
        <p class="calc-desc">Pilih spesifikasi laptop / PC dan game untuk melihat estimasi FPS serta analisis keseimbangan hardware secara real-time.</p>
      </div>

      <!-- Mode Selector -->
      <div class="tab-pill">
        <button 
          class="pill-btn" 
          :class="{ active: inputMode === 'manual' }"
          @click="inputMode = 'manual'"
        >
          Pilih Manual
        </button>
        <button 
          class="pill-btn" 
          :class="{ active: inputMode === 'raw_spec' }"
          @click="inputMode = 'raw_spec'"
        >
          Tempel Teks Spek Toko
        </button>
      </div>
    </div>

    <!-- Quick Laptop Presets Bar -->
    <div class="presets-bar">
      <span class="preset-title">⚡ Preset Laptop Populer:</span>
      <div class="preset-chips">
        <button 
          v-for="p in laptopPresets" 
          :key="p.name" 
          class="chip-btn"
          @click="applyPreset(p)"
        >
          {{ p.name }}
        </button>
      </div>
    </div>

    <!-- Mode 2: Quick Spec Text Parser -->
    <div v-if="inputMode === 'raw_spec'" class="spec-paste-area">
      <div class="paste-header">
        <label class="field-label">Tempel Teks Spesifikasi (dari Tokopedia / Shopee / Brosur):</label>
        <button class="link-btn" @click="loadSampleSpec">
          Isi Contoh Spek Laptop
        </button>
      </div>

      <textarea
        v-model="rawSpecText"
        class="input-textarea"
        rows="6"
        placeholder="Contoh:
Processor : Intel Core i5-13420H
Graphics : NVIDIA GeForce RTX 3050 6GB GDDR6
Memory : 16GB DDR4
Display : 15.6 inch FHD 144Hz"
      ></textarea>

      <div class="paste-action">
        <button 
          class="btn-primary" 
          :disabled="!rawSpecText.trim() || isParsing"
          @click="parseAndApplySpec"
        >
          {{ isParsing ? 'Mengekstrak...' : 'Terapkan Spesifikasi' }}
        </button>
      </div>

      <!-- Extracted result feedback -->
      <div v-if="parsedDetails" class="extracted-box">
        <div class="extracted-item">
          <span class="ex-lbl">CPU:</span>
          <span class="ex-val">{{ parsedDetails.matched_cpu ? `${parsedDetails.matched_cpu.brand} ${parsedDetails.matched_cpu.name}` : (parsedDetails.parsed.cpu_query || 'Tidak cocok') }}</span>
        </div>
        <div class="extracted-item">
          <span class="ex-lbl">GPU:</span>
          <span class="ex-val">{{ parsedDetails.matched_gpu ? `${parsedDetails.matched_gpu.brand} ${parsedDetails.matched_gpu.name}` : (parsedDetails.parsed.gpu_query || 'Tidak cocok') }}</span>
        </div>
        <div class="extracted-item">
          <span class="ex-lbl">RAM & Layar:</span>
          <span class="ex-val">{{ parsedDetails.parsed.ram_gb }} GB RAM • {{ parsedDetails.parsed.resolution }}</span>
        </div>
      </div>
    </div>

    <!-- Mode 1: Manual Controls Form -->
    <div class="form-grid">
      <!-- 1. CPU -->
      <div class="form-group">
        <label class="field-label">Prosesor (CPU)</label>
        <div class="autocomplete-box">
          <input
            type="text"
            v-model="cpuSearch"
            placeholder="Cari CPU (misal: i5-13420H, Ryzen 5...)"
            @focus="showCpuDropdown = true"
            class="input-control"
          />
          <div v-if="showCpuDropdown && filteredCpus.length" class="dropdown-list">
            <div
              v-for="cpu in filteredCpus"
              :key="cpu.id"
              class="dropdown-row"
              @click="selectCpu(cpu)"
            >
              <div class="row-left">
                <span class="row-name">{{ cpu.brand }} {{ cpu.name }}</span>
                <span class="row-sub">Single: {{ cpu.single_score }} | Multi: {{ cpu.multi_score }}</span>
              </div>
              <span class="badge" :class="cpu.form_factor === 'laptop' ? 'badge-laptop' : 'badge-desktop'">
                {{ cpu.form_factor }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. GPU -->
      <div class="form-group">
        <label class="field-label">Kartu Grafis (GPU)</label>
        <div class="autocomplete-box">
          <input
            type="text"
            v-model="gpuSearch"
            placeholder="Cari GPU (misal: RTX 3050, RTX 4060...)"
            @focus="showGpuDropdown = true"
            class="input-control"
          />
          <div v-if="showGpuDropdown && filteredGpus.length" class="dropdown-list">
            <div
              v-for="gpu in filteredGpus"
              :key="gpu.id"
              class="dropdown-row"
              @click="selectGpu(gpu)"
            >
              <div class="row-left">
                <span class="row-name">{{ gpu.brand }} {{ gpu.name }}</span>
                <span class="row-sub">Score: {{ gpu.multi_score }} {{ gpu.vram_gb ? '| ' + gpu.vram_gb + 'GB' : '' }}</span>
              </div>
              <span class="badge" :class="gpu.form_factor === 'laptop' ? 'badge-laptop' : 'badge-desktop'">
                {{ gpu.form_factor }} {{ gpu.tgp_watts ? gpu.tgp_watts + 'W' : '' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. RAM -->
      <div class="form-group">
        <label class="field-label">Kapasitas RAM</label>
        <div class="btn-group">
          <button 
            v-for="ram in [4, 8, 16, 32, 64]" 
            :key="ram"
            class="opt-btn"
            :class="{ active: selectedRam === ram }"
            @click="setRam(ram)"
          >
            {{ ram }} GB
          </button>
        </div>
      </div>
    </div>

    <!-- Interactive Game Selection Chips -->
    <div class="game-chips-wrap">
      <label class="field-label">Target Game (Klik untuk ganti)</label>
      <div class="game-chips">
        <button 
          v-for="g in games" 
          :key="g.id"
          class="game-chip-btn"
          :class="{ active: selectedGameId === g.id }"
          @click="selectGame(g.id)"
        >
          <span class="g-title">{{ g.title }}</span>
          <span class="g-genre">{{ g.genre }}</span>
        </button>
      </div>
    </div>

    <!-- Parameter Row: Resolution & Preset -->
    <div class="param-row">
      <div class="param-item">
        <label class="field-label">Resolusi Layar</label>
        <div class="btn-group">
          <button 
            v-for="res in ['1080p', '1440p', '4K']" 
            :key="res"
            class="opt-btn"
            :class="{ active: selectedResolution === res }"
            @click="setResolution(res)"
          >
            {{ res }}
          </button>
        </div>
      </div>

      <div class="param-item">
        <label class="field-label">Preset Grafis Game</label>
        <div class="btn-group">
          <button 
            v-for="p in ['Low', 'Medium', 'High', 'Ultra']" 
            :key="p"
            class="opt-btn"
            :class="{ active: selectedPreset === p }"
            @click="setPreset(p)"
          >
            {{ p }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  hardwareList: {
    type: Array,
    default: () => []
  },
  games: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['calculate'])

const inputMode = ref('manual')
const rawSpecText = ref('')
const isParsing = ref(false)
const parsedDetails = ref(null)

const cpuSearch = ref('')
const gpuSearch = ref('')
const showCpuDropdown = ref(false)
const showGpuDropdown = ref(false)

const selectedCpu = ref(null)
const selectedGpu = ref(null)
const selectedGameId = ref(1)
const selectedRam = ref(16)
const selectedResolution = ref('1080p')
const selectedPreset = ref('Ultra')
const isCalculating = ref(false)

// Popular laptop presets for instant testing
const laptopPresets = [
  { name: "Lenovo LOQ (i5-13420H + RTX 3050 6GB)", cpu: "13420H", gpu: "RTX 3050 6GB Laptop (95W)", ram: 16 },
  { name: "Acer Nitro V15 (i5-13420H + RTX 4050)", cpu: "13420H", gpu: "RTX 4050 Laptop (95W)", ram: 16 },
  { name: "ASUS TUF A15 (Ryzen 7 7735HS + RTX 4060)", cpu: "7735HS", gpu: "RTX 4060 Laptop (140W)", ram: 16 },
  { name: "ROG Strix G16 (i9-14900HX + RTX 4080)", cpu: "14900HX", gpu: "RTX 4080 Laptop (175W)", ram: 32 },
  { name: "PC Rakitan Hemat (Ryzen 5 5600 + RTX 4060)", cpu: "5600", gpu: "GeForce RTX 4060", ram: 16, desktop: true },
]

const applyPreset = (p) => {
  const cpu = props.hardwareList.find(i => i.category === 'cpu' && i.name.includes(p.cpu))
  const gpu = props.hardwareList.find(i => i.category === 'gpu' && i.name.includes(p.gpu))
  if (cpu) selectCpu(cpu)
  if (gpu) selectGpu(gpu)
  if (p.ram) selectedRam.value = p.ram
}

const sampleSpec = `Processor : 13th Generation Intel Core i5-13420H Processor (12M Cache, up to 4.60 GHz)
Graphics : NVIDIA GeForce RTX 3050 6GB GDDR6
Memory : 16GB DDR4
Storage : 512GB PCIe NVMe M.2 SSD
Display : 15.6 inch Full HD IPS (1920 x 1080), 144Hz refresh rate
Operating System : Windows 11 + Office Home Student 2021`

const loadSampleSpec = () => {
  rawSpecText.value = sampleSpec
}

const parseAndApplySpec = async () => {
  if (!rawSpecText.value.trim()) return
  isParsing.value = true
  try {
    const res = await fetch('/api/hardware/parse-raw-spec', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text: rawSpecText.value })
    })
    if (res.ok) {
      const data = await res.json()
      parsedDetails.value = data
      
      if (data.matched_cpu) selectCpu(data.matched_cpu)
      if (data.matched_gpu) selectGpu(data.matched_gpu)
      if (data.parsed.ram_gb) selectedRam.value = data.parsed.ram_gb
      if (data.parsed.resolution) selectedResolution.value = data.parsed.resolution
    }
  } catch (err) {
    console.error('Error parsing raw spec:', err)
  } finally {
    isParsing.value = false
  }
}

const filteredCpus = computed(() => {
  const cpus = props.hardwareList.filter(item => item.category === 'cpu')
  if (!cpuSearch.value.trim()) return cpus.slice(0, 8)
  const q = cpuSearch.value.toLowerCase()
  return cpus.filter(c => c.name.toLowerCase().includes(q) || c.brand.toLowerCase().includes(q)).slice(0, 10)
})

const filteredGpus = computed(() => {
  const gpus = props.hardwareList.filter(item => item.category === 'gpu')
  if (!gpuSearch.value.trim()) return gpus.slice(0, 8)
  const q = gpuSearch.value.toLowerCase()
  return gpus.filter(g => g.name.toLowerCase().includes(q) || g.brand.toLowerCase().includes(q)).slice(0, 10)
})

const selectCpu = (cpu) => {
  selectedCpu.value = cpu
  cpuSearch.value = `${cpu.brand} ${cpu.name}`
  showCpuDropdown.value = false
}

const selectGpu = (gpu) => {
  selectedGpu.value = gpu
  gpuSearch.value = `${gpu.brand} ${gpu.name}`
  showGpuDropdown.value = false
}

const selectGame = (id) => {
  selectedGameId.value = id
}

const setRam = (ram) => {
  selectedRam.value = ram
}

const setResolution = (res) => {
  selectedResolution.value = res
}

const setPreset = (p) => {
  selectedPreset.value = p
}

const triggerCalculate = () => {
  if (!selectedCpu.value || !selectedGpu.value || !selectedGameId.value) return
  emit('calculate', {
    cpu_id: selectedCpu.value.id,
    gpu_id: selectedGpu.value.id,
    game_id: selectedGameId.value,
    ram_gb: selectedRam.value,
    resolution: selectedResolution.value,
    preset: selectedPreset.value
  })
}

// Single authoritative watcher on all state parameters
watch(
  [selectedCpu, selectedGpu, selectedGameId, selectedRam, selectedResolution, selectedPreset],
  () => {
    triggerCalculate()
  }
)

// Initialize default hardware & game when props arrive
watch([() => props.hardwareList, () => props.games], ([list, gList]) => {
  if (gList && gList.length > 0 && !selectedGameId.value) {
    selectedGameId.value = gList[0].id
  } else if (gList && gList.length > 0 && selectedGameId.value === 1 && gList[0].id !== 1) {
    selectedGameId.value = gList[0].id
  }

  if (list && list.length > 0 && !selectedCpu.value) {
    const defaultCpu = list.find(i => i.name.includes('13420H') || i.name.includes('13400F')) || list[0]
    const defaultGpu = list.find(i => i.name.includes('3050 6GB') || i.name.includes('3050')) || list[1]
    if (defaultCpu) {
      selectedCpu.value = defaultCpu
      cpuSearch.value = `${defaultCpu.brand} ${defaultCpu.name}`
    }
    if (defaultGpu) {
      selectedGpu.value = defaultGpu
      gpuSearch.value = `${defaultGpu.brand} ${defaultGpu.name}`
    }
  }
}, { immediate: true })
</script>

<style scoped>
.calc-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.calc-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-main);
}

.calc-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 2px;
}

/* Presets Bar */
.presets-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding: 8px 12px;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  overflow-x: auto;
}

.preset-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-dim);
  white-space: nowrap;
}

.preset-chips {
  display: flex;
  gap: 6px;
}

.chip-btn {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.chip-btn:hover {
  background: var(--bg-surface-elevated);
  border-color: #60a5fa;
  color: #60a5fa;
}

/* Tabs */
.tab-pill {
  display: flex;
  background: var(--bg-input);
  padding: 3px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

.pill-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.pill-btn.active {
  background: var(--bg-surface-elevated);
  color: var(--text-main);
}

/* Raw spec paste box */
.spec-paste-area {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 20px;
}

.paste-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.link-btn {
  background: transparent;
  border: none;
  color: #60a5fa;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

.input-textarea {
  width: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  color: var(--text-main);
  font-family: var(--font-mono);
  font-size: 0.82rem;
  line-height: 1.5;
  resize: vertical;
}

.input-textarea:focus {
  outline: none;
  border-color: var(--border-focus);
}

.paste-action {
  text-align: right;
  margin-top: 10px;
}

.extracted-box {
  display: flex;
  gap: 16px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
  flex-wrap: wrap;
}

.extracted-item {
  display: flex;
  gap: 6px;
  font-size: 0.8rem;
}

.ex-lbl {
  color: var(--text-dim);
  font-weight: 600;
}

.ex-val {
  color: #4ade80;
  font-weight: 600;
}

/* Form Controls */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
}

.autocomplete-box {
  position: relative;
}

.input-control, .select-control {
  width: 100%;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  color: var(--text-main);
  font-size: 0.88rem;
}

.input-control:focus, .select-control:focus {
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
  max-height: 220px;
  overflow-y: auto;
  z-index: 50;
  box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}

.dropdown-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 0.85rem;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}

.dropdown-row:hover {
  background: var(--bg-surface-elevated);
}

.row-left {
  display: flex;
  flex-direction: column;
}

.row-name {
  font-weight: 600;
  color: var(--text-main);
}

.row-sub {
  font-size: 0.72rem;
  color: var(--text-dim);
  font-family: var(--font-mono);
}

.btn-group {
  display: flex;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 2px;
  gap: 2px;
}

.opt-btn {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-muted);
  padding: 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.opt-btn.active {
  background: var(--primary);
  color: white;
}

/* Game Chips */
.game-chips-wrap {
  margin-bottom: 16px;
}

.game-chips-lbl {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-dim);
  display: block;
  margin-bottom: 6px;
}

.game-chips {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.game-chip-btn {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.game-chip-btn:hover {
  background: var(--bg-surface-elevated);
}

.game-chip-btn.active {
  border-color: var(--primary);
  background: rgba(37, 99, 235, 0.15);
}

.g-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-main);
}

.g-genre {
  font-size: 0.68rem;
  color: var(--text-muted);
}

.param-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 12px;
}

@media (max-width: 600px) {
  .param-row {
    grid-template-columns: 1fr;
  }
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
