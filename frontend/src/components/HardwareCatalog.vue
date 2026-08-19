<template>
  <div class="catalog-section">
    <div class="section-title-bar">
      <div>
        <h2 class="title-text">Database Hardware Benchmark</h2>
        <p class="subtitle-text">Daftar spesifikasi lengkap CPU & GPU laptop/desktop beserta skor benchmark sintetis.</p>
      </div>
      <div class="filters-wrap">
        <select v-model="filterCategory" class="filter-select">
          <option value="all">Semua Kategori</option>
          <option value="cpu">Hanya CPU</option>
          <option value="gpu">Hanya GPU</option>
        </select>
        <select v-model="filterFormFactor" class="filter-select">
          <option value="all">Semua Form Factor</option>
          <option value="desktop">Desktop</option>
          <option value="laptop">Laptop (TGP)</option>
        </select>
      </div>
    </div>

    <div class="panel catalog-card">
      <div class="search-bar">
        <input 
          type="text" 
          v-model="catalogSearch" 
          placeholder="Cari berdasarkan nama model atau brand..." 
          class="catalog-search-input"
        />
        <span class="count-badge">{{ filteredList.length }} Komponen</span>
      </div>

      <div class="catalog-grid">
        <div 
          v-for="item in filteredList" 
          :key="item.id" 
          class="hw-card"
        >
          <div class="hw-top">
            <span class="brand-tag">{{ item.brand }}</span>
            <span class="badge" :class="item.form_factor === 'laptop' ? 'badge-laptop' : 'badge-desktop'">
              {{ item.form_factor }}
            </span>
          </div>

          <h3 class="hw-name">{{ item.name }}</h3>

          <div class="hw-specs">
            <div class="spec-row">
              <span class="lbl">{{ item.category === 'cpu' ? 'Single Core' : 'Compute Score' }}</span>
              <span class="val">{{ item.single_score.toLocaleString() }}</span>
            </div>
            <div class="spec-row">
              <span class="lbl">{{ item.category === 'cpu' ? 'Multi Core' : '3D Score' }}</span>
              <span class="val highlight-val">{{ item.multi_score.toLocaleString() }}</span>
            </div>
            <div v-if="item.tgp_watts" class="spec-row">
              <span class="lbl">TGP Power</span>
              <span class="val tgp-val">{{ item.tgp_watts }} W</span>
            </div>
            <div v-if="item.vram_gb" class="spec-row">
              <span class="lbl">VRAM</span>
              <span class="val">{{ item.vram_gb }} GB</span>
            </div>
            <div class="spec-row">
              <span class="lbl">Rilis</span>
              <span class="val">{{ item.release_year }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  hardwareList: {
    type: Array,
    default: () => []
  }
})

const filterCategory = ref('all')
const filterFormFactor = ref('all')
const catalogSearch = ref('')

const filteredList = computed(() => {
  return props.hardwareList.filter(item => {
    if (filterCategory.value !== 'all' && item.category !== filterCategory.value) return false
    if (filterFormFactor.value !== 'all' && item.form_factor !== filterFormFactor.value) return false
    if (catalogSearch.value.trim()) {
      const q = catalogSearch.value.toLowerCase()
      if (!item.name.toLowerCase().includes(q) && !item.brand.toLowerCase().includes(q)) return false
    }
    return true
  })
})
</script>

<style scoped>
.catalog-section {
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

.filters-wrap {
  display: flex;
  gap: 8px;
}

.filter-select {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: white;
  padding: 6px 10px;
  font-size: 0.82rem;
  cursor: pointer;
}

.catalog-card {
  padding: 16px;
}

.search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.catalog-search-input {
  flex: 1;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  color: white;
  font-size: 0.85rem;
}

.catalog-search-input:focus {
  outline: none;
  border-color: var(--border-focus);
}

.count-badge {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 600;
}

.catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 12px;
}

.hw-card {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 12px;
}

.hw-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.brand-tag {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-dim);
}

.hw-name {
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 8px;
}

.hw-specs {
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 8px;
}

.spec-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
}

.lbl {
  color: var(--text-dim);
}

.val {
  color: var(--text-main);
  font-family: var(--font-mono);
  font-weight: 600;
}

.highlight-val {
  color: #38bdf8;
  font-weight: 700;
}

.tgp-val {
  color: #c084fc;
  font-weight: 700;
}
</style>
