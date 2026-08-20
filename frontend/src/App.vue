<template>
  <div class="app-layout">
    <!-- Header -->
    <header class="navbar">
      <div class="nav-container">
        <div class="brand" @click="currentTab = 'calculator'">
          <div class="brand-badge">FPS</div>
          <div>
            <div class="brand-title">FPSBench</div>
            <div class="brand-sub">Hardware & Game Performance Estimator</div>
          </div>
        </div>

        <nav class="nav-links">
          <button 
            class="nav-tab" 
            :class="{ active: currentTab === 'calculator' }"
            @click="currentTab = 'calculator'"
          >
            Kalkulator FPS
          </button>
          <button 
            class="nav-tab" 
            :class="{ active: currentTab === 'compare' }"
            @click="currentTab = 'compare'"
          >
            Bandingkan Hardware
          </button>
          <button 
            class="nav-tab" 
            :class="{ active: currentTab === 'catalog' }"
            @click="currentTab = 'catalog'"
          >
            Database Spek
          </button>
          <button 
            class="nav-tab" 
            :class="{ active: currentTab === 'scraper' }"
            @click="currentTab = 'scraper'"
          >
            Data Sync
          </button>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-container">
      <!-- Tab 1: Calculator -->
      <div v-show="currentTab === 'calculator'">
        <Calculator 
          :hardware-list="hardwareList" 
          :games="games"
          @calculate="handleCalculate"
        />

        <ResultCard 
          v-if="latestResult" 
          :result="latestResult" 
        />
      </div>

      <!-- Tab 2: Head to Head -->
      <div v-show="currentTab === 'compare'">
        <HeadToHead :hardware-list="hardwareList" />
      </div>

      <!-- Tab 3: Hardware Catalog -->
      <div v-show="currentTab === 'catalog'">
        <HardwareCatalog :hardware-list="hardwareList" />
      </div>

      <!-- Tab 4: ETL Scraper -->
      <div v-show="currentTab === 'scraper'">
        <ScraperPanel @data-updated="fetchInitialData" />
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-inner">
        <span>FPSBench • Alat estimasi performa game & cek bottleneck hardware laptop dan desktop.</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Calculator from './components/Calculator.vue'
import ResultCard from './components/ResultCard.vue'
import HeadToHead from './components/HeadToHead.vue'
import HardwareCatalog from './components/HardwareCatalog.vue'
import ScraperPanel from './components/ScraperPanel.vue'

const currentTab = ref('calculator')
const hardwareList = ref([])
const games = ref([])
const latestResult = ref(null)

const fetchInitialData = async () => {
  try {
    const [hwRes, gameRes] = await Promise.all([
      fetch('/api/hardware/search?limit=500'),
      fetch('/api/games')
    ])
    if (hwRes.ok && gameRes.ok) {
      hardwareList.value = await hwRes.json()
      games.value = await gameRes.json()
    }
  } catch (err) {
    console.error('Error fetching data from API:', err)
  }
}

const handleCalculate = async (payload) => {
  try {
    const res = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (res.ok) {
      latestResult.value = await res.json()
    }
  } catch (err) {
    console.error('Calculation error:', err)
  }
}

onMounted(() => {
  fetchInitialData()
})
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navbar */
.navbar {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  padding: 12px 0;
}

.nav-container {
  max-width: 1050px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.brand-badge {
  background: var(--primary);
  color: white;
  font-size: 0.8rem;
  font-weight: 800;
  padding: 6px 8px;
  border-radius: var(--radius-sm);
}

.brand-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}

.brand-sub {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.nav-links {
  display: flex;
  gap: 4px;
}

.nav-tab {
  background: transparent;
  border: none;
  color: var(--text-muted);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.nav-tab:hover {
  background: var(--bg-surface-elevated);
  color: var(--text-main);
}

.nav-tab.active {
  background: var(--bg-surface-elevated);
  color: #60a5fa;
  font-weight: 700;
}

/* Main Container */
.main-container {
  flex: 1;
  max-width: 1050px;
  width: 100%;
  margin: 24px auto;
  padding: 0 20px;
}

/* Footer */
.footer {
  border-top: 1px solid var(--border-color);
  background: #090d16;
  padding: 20px;
  margin-top: 40px;
}

.footer-inner {
  max-width: 1050px;
  margin: 0 auto;
  text-align: center;
  font-size: 0.8rem;
  color: var(--text-dim);
}
</style>
