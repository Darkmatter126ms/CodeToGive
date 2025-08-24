<script setup>
import { ref, computed } from 'vue'

/* -----------------------------------
   Mock campaigns (align with Edit form)
   ----------------------------------- */
const campaigns = ref([
  {
    id: 1,
    title: "Emergency School Meals",
    school: "Yan Oi Tong Pang Hung Cheung KG",
    region: "Kowloon",
    description: "Provide nutritious meals to children affected by recent floods.",
    image: "https://images.unsplash.com/photo-1498721406610-899c1d4eb77d?q=80&w=1600",
    startDate: "2025-01-15",
    endDate: "2025-03-15",
    goal: 25000,
    raised: 18500,
    supporters: 127,
    status: "Active"
  },
  {
    id: 2,
    title: "Digital Learning Kits",
    school: "Renaissance College",
    region: "New Territories East",
    description: "Tablets and educational apps for remote learning.",
    image: "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1600",
    startDate: "2024-12-01",
    endDate: "2025-04-30",
    goal: 60000,
    raised: 42300,
    supporters: 289,
    status: "Active"
  },
  {
    id: 3,
    title: "Safe Play Spaces",
    school: "Community Centre (Sham Shui Po)",
    region: "Kowloon",
    description: "Build safe playgrounds and recreation areas.",
    image: "https://images.unsplash.com/photo-1544717297-fa95b6ee9643?q=80&w=1600",
    startDate: "2025-02-01",
    endDate: "2025-06-01",
    goal: 35000,
    raised: 8200,
    supporters: 64,
    status: "Ongoing"
  },
  {
    id: 4,
    title: "Reading Corner Libraries",
    school: "South Island School",
    region: "Hong Kong Island",
    description: "Create cozy reading spaces with diverse books.",
    image: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=1600",
    startDate: "2025-01-10",
    endDate: "2025-05-10",
    goal: 40000,
    raised: 31500,
    supporters: 201,
    status: "Active"
  },
  {
    id: 5,
    title: "Mental Health Support",
    school: "District Outreach",
    region: "New Territories West",
    description: "Counsellor training and mental wellness programs.",
    image: "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?q=80&w=1600",
    startDate: "2025-01-20",
    endDate: "2025-07-20",
    goal: 50000,
    raised: 12800,
    supporters: 98,
    status: "Ongoing"
  },
  {
    id: 6,
    title: "Clean Water Initiative",
    school: "Cluster of Partner Schools",
    region: "New Territories East",
    description: "Install purification systems in school canteens.",
    image: "https://images.unsplash.com/photo-1541919329513-35f7af297129?q=80&w=1600",
    startDate: "2024-11-15",
    endDate: "2025-08-15",
    goal: 80000,
    raised: 67500,
    supporters: 445,
    status: "Active"
  }
])

/* -----------------------------------
   Filters & search
   ----------------------------------- */
const query = ref('')
const selectedRegion = ref('All')
const selectedStatus = ref('All')
const regions = ["All", "Hong Kong Island", "Kowloon", "New Territories East", "New Territories West"]
const statuses = ["All", "Active", "Ongoing", "Completed"]

const progressPct = (r, g) => Math.min(100, Math.round((r / g) * 100))
const formatAmt = (n) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n)
const formatDate = (d) =>
  new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()

  return campaigns.value.filter(c => {
    const matchesRegion = selectedRegion.value === 'All' || c.region === selectedRegion.value
    const matchesStatus = selectedStatus.value === 'All' || c.status === selectedStatus.value
    const matchesQuery = !q ||
      c.title.toLowerCase().includes(q) ||
      c.school.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q)
    return matchesRegion && matchesStatus && matchesQuery
  })
})
</script>

<template>
  <!-- HERO -->
  <header class="hero-gradient hero-pattern">
    <div class="container py-20 md:py-28 text-center">
      <h1 class="hero-title text-white animate-slide-up">
        Browse <span class="text-gradient">Campaigns</span>
      </h1>
      <p class="hero-lead text-white opacity-90 max-w-3xl mx-auto animate-fade-in">
        Search and filter live campaigns. These match the fields you edit (title, region, dates, goal, status).
      </p>
    </div>
  </header>

  <!-- CONTENT WITH STICKY FILTERS -->
  <section class="section-white">
    <div class="container py-14">
      <div class="grid md:grid-cols-[320px,1fr] gap-8">
        <!-- Filters sidebar -->
        <aside class="card p-6 filters-sticky animate-slide-left">
          <h3 class="text-xl font-weight-700 text-slate-900 mb-4">Filter campaigns</h3>

          <label class="form-label">Search</label>
          <div class="flex gap-2">
            <input v-model="query" class="form-input" type="search" placeholder="Title, school or description…" />
            <button class="btn-donate" @click="/* v-model already filters; button just keeps UX */ null">Search</button>
          </div>

          <div class="mt-5">
            <label class="form-label">Region</label>
            <select v-model="selectedRegion" class="campaign-sort w-full">
              <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>

          <div class="mt-4">
            <label class="form-label">Status</label>
            <select v-model="selectedStatus" class="campaign-sort w-full">
              <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>

          <div class="mt-6 flex gap-3">
            <button class="btn-secondary flex-1" @click="query='';selectedRegion='All';selectedStatus='All'">
              Clear
            </button>
            <a href="#results" class="btn-donate flex-1">Jump to results</a>
          </div>
        </aside>

        <!-- Results -->
        <div id="results">
          <div class="social-proof mb-6">
            Showing <strong>{{ filtered.length }}</strong> campaign(s)
            <span v-if="selectedRegion !== 'All'"> • Region: <strong>{{ selectedRegion }}</strong></span>
            <span v-if="selectedStatus !== 'All'"> • Status: <strong>{{ selectedStatus }}</strong></span>
            <span v-if="query"> • Search: <strong>“{{ query }}”</strong></span>
          </div>

          <div class="grid md:grid-cols-2 gap-8">
            <article
              v-for="c in filtered"
              :key="c.id"
              class="story-card campaign-card animate-slide-up"
            >
              <!-- Image + badges -->
              <div class="campaign-image-wrapper">
                <img :src="c.image" :alt="c.title" class="w-full h-44 object-cover" />
                <div class="campaign-badges">
                  <span class="trust-badge">{{ c.status }}</span>
                  <span class="trust-badge">{{ c.region }}</span>
                </div>
              </div>

              <!-- Content -->
              <div class="p-6">
                <div class="mb-3">
                  <h3 class="text-xl font-weight-700 text-slate-900">{{ c.title }}</h3>
                  <p class="text-slate-600 mt-1">{{ c.school }}</p>
                </div>

                <p class="text-slate-600">{{ c.description }}</p>

                <!-- Dates -->
                <div class="card p-4 mt-4">
                  <div class="flex justify-between text-center">
                    <div>
                      <div class="text-sm text-slate-600">Start</div>
                      <div class="font-weight-600 text-slate-900 mt-1">{{ formatDate(c.startDate) }}</div>
                    </div>
                    <div>
                      <div class="text-sm text-slate-600">End</div>
                      <div class="font-weight-600 text-slate-900 mt-1">{{ formatDate(c.endDate) }}</div>
                    </div>
                  </div>
                </div>

                <!-- Progress -->
                <div class="mt-4">
                  <div class="flex justify-between items-center mb-2">
                    <div>
                      <div class="font-weight-700 text-slate-900">{{ formatAmt(c.raised) }}</div>
                      <div class="text-sm text-slate-600">of {{ formatAmt(c.goal) }}</div>
                    </div>
                    <span class="trust-badge">
                      {{ progressPct(c.raised, c.goal) }}%
                    </span>
                  </div>
                  <div class="progress-bar-large">
                    <div class="progress-fill-large" :style="{ width: progressPct(c.raised, c.goal) + '%' }"></div>
                  </div>
                  <div class="text-sm text-slate-600 mt-2 text-center">{{ c.supporters }} supporters</div>
                </div>

                <!-- Actions -->
                <div class="mt-6 flex gap-3">
                  <a :href="`/donate?campaign=${c.id}`" class="btn-donate flex-1 text-center">Donate</a>
                  <a :href="`/campaign/${c.id}`" class="btn-secondary flex-1 text-center">Learn more</a>
                </div>
              </div>
            </article>
          </div>

          <!-- Empty state -->
          <div v-if="filtered.length === 0" class="card p-8 mt-8 text-center">
            <h3 class="text-xl font-weight-700 text-slate-900">No campaigns found</h3>
            <p class="mt-2 text-slate-600">Try clearing filters or changing your search.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Minimal custom styles - using main.css components wherever possible */

/* Campaign image wrapper with overlay */
.campaign-image-wrapper {
  position: relative;
  overflow: hidden;
}

.campaign-badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.days-remaining-badge {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
}

/* Urgency color variants for trust-badge */
.urgent-high {
  border-color: #dc2626 !important;
  color: #dc2626 !important;
  background: linear-gradient(145deg, #fef2f2, #fff) !important;
}

.urgent-medium {
  border-color: #ea580c !important;
  color: #ea580c !important;
  background: linear-gradient(145deg, #fff7ed, #fff) !important;
}

.urgent-low {
  border-color: #16a34a !important;
  color: #16a34a !important;
  background: linear-gradient(145deg, #f0fdf4, #fff) !important;
}

/* Badge preview image */
.badge-preview-image {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  object-fit: cover;
  border: 2px solid #22c55e;
}

/* Custom sort select to match design system */
.campaign-sort {
  background: white;
  border: 2px solid #e2e8f0;
  color: #64748b;
  font-weight: 600;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  min-width: 150px;
}

.campaign-sort:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

/* Filter button customizations using existing amount-btn */
.campaign-filter {
  font-size: 0.9rem;
  padding: 0.75rem 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .campaign-badges {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .days-remaining-badge {
    align-self: flex-end;
  }
}

</style>