<script setup>
import { ref, computed, watch } from 'vue'

/* ----------------------------
   Filters / state
----------------------------- */
const selectedPeriod = ref('all')
const selectedRegion = ref('')
const selectedSchool = ref('')
const currentPage   = ref(1)
const itemsPerPage  = ref(25)

const timePeriods = [
  { label: 'All Time',  value: 'all'   },
  { label: 'This Year', value: 'year'  },
  { label: 'This Month',value: 'month' },
  { label: 'This Week', value: 'week'  },
]

// HK-flavoured regions
const regions = [
  'Hong Kong Island',
  'Kowloon',
  'New Territories East',
  'New Territories West'
]

// Mock Hong Kong schools (trim or extend freely)
const schools = [
  'University of Hong Kong',
  'Chinese University of Hong Kong',
  'Hong Kong University of Science and Technology',
  'City University of Hong Kong',
  'Hong Kong Polytechnic University',
  'Hong Kong Baptist University',
  'Lingnan University',
  'Education University of Hong Kong',
  'Hong Kong International School',
  'German Swiss International School',
  'French International School',
  'Canadian International School',
  'Australian International School',
  'Singapore International School',
  'La Salle College',
  'St. Paul\'s College',
  'Diocesan Boys\' School',
  'Diocesan Girls\' School',
  'St. Paul\'s Co-educational College',
  'Wah Yan College Hong Kong',
  'Maryknoll Convent School',
  'St. Stephen\'s Girls\' College',
  'Queen Elizabeth School',
  'King George V School',
  'South Island School',
  'Island School',
  'West Island School',
  'Renaissance College',
  'Discovery College'
]

/* ----------------------------
   Mock donors
   periods: tags array so Month/Year filters work
----------------------------- */
const allDonors = ref([
  { id: 39, name: 'Corporate Sponsor A', school: 'Corporate', region: 'Hong Kong Island', amount: 100000, donationCount: 2, periods: ['all','year','month'] },
  { id: 40, name: 'Foundation Partner',  school: 'Foundation', region: 'New Territories East', amount: 75000, donationCount: 3, periods: ['all','year'] },
  { id: 38, name: 'Anonymous Donor',     school: 'Individual Donor', region: 'Hong Kong Island', amount: 50000, donationCount: 1, periods: ['all','year','month','week'] },
  { id: 1,  name: 'Sarah Chen',           school: 'University of Hong Kong', region: 'Hong Kong Island', amount: 25000, donationCount: 15, periods: ['all','year','month'] },
  { id: 2,  name: 'Michael Wong',         school: 'Hong Kong International School', region: 'Hong Kong Island', amount: 18500, donationCount: 8, periods: ['all','year'] },
  { id: 3,  name: 'Emily Lau',            school: 'Chinese University of Hong Kong', region: 'New Territories East', amount: 15750, donationCount: 12, periods: ['all','year','month'] },
  { id: 4,  name: 'David Kim',            school: 'Hong Kong University of Science and Technology', region: 'New Territories East', amount: 14200, donationCount: 6, periods: ['all'] },
  { id: 5,  name: 'Jennifer Li',          school: 'City University of Hong Kong', region: 'Kowloon', amount: 12800, donationCount: 10, periods: ['all','year','month','week'] },
  { id: 6,  name: 'Alex Turner',          school: 'Hong Kong International School', region: 'Hong Kong Island', amount: 11900, donationCount: 7, periods: ['all','year'] },
  { id: 7,  name: 'Grace Ng',             school: 'Hong Kong Polytechnic University', region: 'Kowloon', amount: 10500, donationCount: 9, periods: ['all','month'] },
  { id: 8,  name: 'Robert Zhang',         school: 'Hong Kong Baptist University', region: 'Kowloon', amount: 9800, donationCount: 5, periods: ['all'] },
  { id: 9,  name: 'Michelle Tam',         school: 'Lingnan University', region: 'New Territories West', amount: 9200, donationCount: 8, periods: ['all','year'] },
  { id: 10, name: 'Kevin Choi',           school: 'Education University of Hong Kong', region: 'New Territories East', amount: 8750, donationCount: 6, periods: ['all','year','month'] },
  { id: 11, name: 'Lisa Park',            school: 'German Swiss International School', region: 'Hong Kong Island', amount: 8500, donationCount: 11, periods: ['all','month'] },
  { id: 12, name: 'James Wu',             school: 'French International School', region: 'Hong Kong Island', amount: 8200, donationCount: 4, periods: ['all'] },
  { id: 13, name: 'Amanda Ho',            school: 'Canadian International School', region: 'Hong Kong Island', amount: 7900, donationCount: 7, periods: ['all','year'] },
  { id: 14, name: 'Tony Lam',             school: 'Australian International School', region: 'Kowloon', amount: 7600, donationCount: 5, periods: ['all'] },
  { id: 15, name: 'Helen Yu',             school: 'Singapore International School', region: 'Hong Kong Island', amount: 7300, donationCount: 9, periods: ['all','week'] },
  { id: 16, name: 'Peter Fong',           school: 'La Salle College', region: 'Kowloon', amount: 7000, donationCount: 6, periods: ['all'] },
  { id: 17, name: 'Stephanie Chu',        school: 'St. Paul\'s College', region: 'Hong Kong Island', amount: 6800, donationCount: 8, periods: ['all','month'] },
  { id: 18, name: 'Andrew Ma',            school: 'Diocesan Boys\' School', region: 'Kowloon', amount: 6500, donationCount: 4, periods: ['all'] },
  { id: 19, name: 'Rachel Leung',         school: 'Diocesan Girls\' School', region: 'Kowloon', amount: 6200, donationCount: 7, periods: ['all'] },
  { id: 20, name: 'William Tsang',        school: 'St. Paul\'s Co-educational College', region: 'Hong Kong Island', amount: 5900, donationCount: 5, periods: ['all','year'] },
  { id: 21, name: 'Crystal Wang',         school: 'Wah Yan College Hong Kong', region: 'Hong Kong Island', amount: 5600, donationCount: 6, periods: ['all'] },
  { id: 22, name: 'Daniel Yip',           school: 'Maryknoll Convent School', region: 'Kowloon', amount: 5300, donationCount: 8, periods: ['all','week'] },
  { id: 23, name: 'Vivian Chan',          school: 'St. Stephen\'s Girls\' College', region: 'Hong Kong Island', amount: 5000, donationCount: 3, periods: ['all'] },
  { id: 24, name: 'Eric Siu',             school: 'Queen Elizabeth School', region: 'Hong Kong Island', amount: 4800, donationCount: 7, periods: ['all'] },
  { id: 25, name: 'Nancy Liu',            school: 'King George V School', region: 'Kowloon', amount: 4500, donationCount: 5, periods: ['all'] },
  { id: 26, name: 'Steven Mok',           school: 'South Island School', region: 'Hong Kong Island', amount: 4200, donationCount: 4, periods: ['all'] },
  { id: 27, name: 'Tina Kwok',            school: 'Island School', region: 'Hong Kong Island', amount: 3900, donationCount: 6, periods: ['all','month'] },
  { id: 28, name: 'Gary Cheng',           school: 'West Island School', region: 'Hong Kong Island', amount: 3600, donationCount: 3, periods: ['all'] },
  { id: 29, name: 'Chloe Hui',            school: 'Renaissance College', region: 'New Territories East', amount: 3300, donationCount: 5, periods: ['all','year'] },
  { id: 30, name: 'Marcus Luk',           school: 'Discovery College', region: 'New Territories East', amount: 3000, donationCount: 4, periods: ['all'] },
  { id: 31, name: 'Iris Yeung',           school: 'University of Hong Kong', region: 'Hong Kong Island', amount: 2800, donationCount: 7, periods: ['all'] },
  { id: 32, name: 'Henry Tse',            school: 'Chinese University of Hong Kong', region: 'New Territories East', amount: 2500, donationCount: 3, periods: ['all'] },
  { id: 33, name: 'Joanne Kwan',          school: 'Hong Kong University of Science and Technology', region: 'New Territories East', amount: 2200, donationCount: 6, periods: ['all','week'] },
  { id: 34, name: 'Vincent So',           school: 'City University of Hong Kong', region: 'Kowloon', amount: 1900, donationCount: 2, periods: ['all'] },
  { id: 35, name: 'Mandy Ip',             school: 'Hong Kong Polytechnic University', region: 'Kowloon', amount: 1600, donationCount: 5, periods: ['all'] },
  { id: 36, name: 'Keith Poon',           school: 'Hong Kong Baptist University', region: 'Kowloon', amount: 1300, donationCount: 4, periods: ['all'] },
  { id: 37, name: 'Fiona Ng',             school: 'Lingnan University', region: 'New Territories West', amount: 1000, donationCount: 2, periods: ['all'] },
])

/* ----------------------------
   Stats (overall)
----------------------------- */
const totalDonors  = computed(() => allDonors.value.length)
const totalRaised  = computed(() => allDonors.value.reduce((s,d)=>s+d.amount,0))
const activeSchools = computed(() => new Set(allDonors.value.map(d=>d.school)).size)
const regionsActive = computed(() => new Set(allDonors.value.map(d=>d.region)).size)

/* ----------------------------
   Filtering / sorting / paging
----------------------------- */
const filteredDonors = computed(() => {
  let list = [...allDonors.value]

  if (selectedPeriod.value !== 'all') {
    list = list.filter(d => d.periods?.includes(selectedPeriod.value))
  }
  if (selectedRegion.value) {
    list = list.filter(d => d.region === selectedRegion.value)
  }
  if (selectedSchool.value) {
    list = list.filter(d => d.school === selectedSchool.value)
  }

  // sort by total amount, desc
  list.sort((a,b)=> b.amount - a.amount)
  return list
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredDonors.value.length / itemsPerPage.value))
)

const paginatedDonors = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredDonors.value.slice(start, start + itemsPerPage.value)
})

// simple numeric page window
const visiblePages = computed(() => {
  const total = totalPages.value
  const cur   = currentPage.value
  const start = Math.max(1, cur - 2)
  const end   = Math.min(total, cur + 2)
  const out = []
  for (let p = start; p <= end; p++) out.push(p)
  if (!out.includes(1)) out.unshift(1)
  if (!out.includes(total)) out.push(total)
  return [...new Set(out)].sort((a,b)=>a-b)
})

// reset page when any filter changes
watch([selectedPeriod, selectedRegion, selectedSchool], () => {
  currentPage.value = 1
})

/* ----------------------------
   Small helpers for chips/badges
----------------------------- */
function regionChipStyle(region){
  switch(region){
    case 'Hong Kong Island':   return { background:'#dbeafe', color:'#1e40af' } // blue
    case 'Kowloon':            return { background:'#f3e8ff', color:'#6b21a8' } // purple
    case 'New Territories East': return { background:'#dcfce7', color:'#065f46' } // green
    case 'New Territories West': return { background:'#ffedd5', color:'#9a3412' } // orange
    default: return { background:'#e2e8f0', color:'#334155' }
  }
}

function tierStyle(amount){
  if (amount >= 50000) return { background: 'linear-gradient(90deg,#f59e0b,#d97706)', color: '#fff' } // Platinum-ish
  if (amount >= 25000) return { background: 'linear-gradient(90deg,#8b5cf6,#7c3aed)', color: '#fff' } // Diamond-ish
  if (amount >= 10000) return { background: 'linear-gradient(90deg,#3b82f6,#1d4ed8)', color: '#fff' } // Gold-ish
  if (amount >=  5000) return { background: 'linear-gradient(90deg,#10b981,#059669)', color: '#fff' } // Silver-ish
  if (amount >=  1000) return { background: 'linear-gradient(90deg,#6366f1,#4338ca)', color: '#fff' } // Bronze-ish
  return { background:'#e2e8f0', color:'#334155' }
}
function tierText(amount){
  if (amount >= 50000) return 'Platinum'
  if (amount >= 25000) return 'Diamond'
  if (amount >= 10000) return 'Gold'
  if (amount >=  5000) return 'Silver'
  if (amount >=  1000) return 'Bronze'
  return 'Supporter'
}
</script>

<template>
  <div class="section-light">
    <!-- Hero -->
    <header class="hero-gradient hero-pattern">
      <div class="container py-16 text-center">
        <h1 class="hero-title text-white mb-4 animate-slide-up">
          <span class="text-gradient">Donor</span> Leaderboard
        </h1>
        <p class="hero-lead text-white opacity-90 max-w-3xl mx-auto animate-fade-in">
          Celebrating the community that powers our work for children in Hong Kong.
        </p>
      </div>
    </header>

    <!-- Stats -->
    <section class="section-light">
      <div class="container py-16">
        <div class="grid md:grid-cols-4 gap-6">
          <div class="stat-card animate-slide-up">
            <div class="stat-number">{{ totalDonors.toLocaleString() }}</div>
            <p>Total Donors</p>
          </div>
          <div class="stat-card stat-money animate-slide-up" style="animation-delay:.05s">
            <div class="stat-number">${{ totalRaised.toLocaleString() }}</div>
            <p>Total Raised</p>
          </div>
          <div class="stat-card animate-slide-up" style="animation-delay:.1s">
            <div class="stat-number">{{ activeSchools }}</div>
            <p>Active Schools</p>
          </div>
          <div class="stat-card animate-slide-up" style="animation-delay:.15s">
            <div class="stat-number">{{ regionsActive }}</div>
            <p>Regions</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Filters -->
    <section class="section-white">
      <div class="container py-8">
        <div class="card p-6 max-w-4xl mx-auto">
          <h3 class="text-xl font-weight-700 text-slate-900 mb-6 text-center">Filter Rankings</h3>

          <!-- time tabs (uses amount-btn + selected state from main.css) -->
          <div class="flex flex-wrap gap-3 justify-center mb-6">
            <button
              v-for="p in timePeriods" :key="p.value"
              class="amount-btn campaign-filter"
              :class="{ selected: selectedPeriod === p.value }"
              @click="selectedPeriod = p.value"
              style="padding:.75rem 1.25rem"
            >
              {{ p.label }}
            </button>
          </div>

          <div class="grid md:grid-cols-2 gap-4">
            <div>
              <label class="form-label">Filter by Region</label>
              <select v-model="selectedRegion" class="form-input">
                <option value="">All Regions</option>
                <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>
            <div>
              <label class="form-label">Filter by School</label>
              <select v-model="selectedSchool" class="form-input">
                <option value="">All Schools</option>
                <option v-for="s in schools" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
          </div>

          <!-- active chips -->
          <div v-if="selectedRegion || selectedSchool" class="mt-4 flex flex-wrap gap-2">
            <span v-if="selectedRegion" class="trust-badge">
              Region: {{ selectedRegion }}
              <button @click="selectedRegion=''" style="margin-left:.5rem">×</button>
            </span>
            <span v-if="selectedSchool" class="trust-badge">
              School: {{ selectedSchool }}
              <button @click="selectedSchool=''" style="margin-left:.5rem">×</button>
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Top 3 -->
    <section class="section-light">
      <div class="container py-16">
        <h2 class="text-center text-2xl md:text-3xl font-weight-700 text-slate-900 mb-10 py-8">Top Contributors</h2>

        <div class="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <!-- 2nd -->
          <article class="story-card campaign-card animate-slide-left order-2 md:order-1" style="animation-delay:.15s">
            <div class="campaign-badges">
              <span class="trust-badge urgent-medium">#2</span>
            </div>
            <div class="campaign-image-wrapper h-44">
              <img class="w-full h-full object-cover"
                   src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80"
                   alt="Second place donor">
            </div>
            <div class="p-6">
              <h3 class="text-lg font-weight-700 text-slate-900 mb-1">
                {{ filteredDonors[1]?.name || '—' }}
              </h3>
              <p class="text-slate-600 mb-1">{{ filteredDonors[1]?.school || '—' }}</p>
              <p class="text-slate-600 mb-4">{{ filteredDonors[1]?.region || '—' }}</p>
              <div class="impact-highlight" v-if="filteredDonors[1]">
                <strong>${{ filteredDonors[1].amount.toLocaleString() }}</strong> donated
              </div>
            </div>
          </article>

          <!-- 1st -->
          <article class="story-card campaign-card animate-slide-up order-1 md:order-2" style="transform:scale(1.04)">
            <div class="campaign-badges">
              <span class="trust-badge" style="background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#fff;border-color:#f59e0b">
                👑 #1
              </span>
            </div>
            <div class="campaign-image-wrapper h-44">
              <img class="w-full h-full object-cover"
                   src="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=600&q=80"
                   alt="First place donor">
            </div>
            <div class="p-6">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-1">
                {{ filteredDonors[0]?.name || '—' }}
              </h3>
              <p class="text-slate-600 mb-1">{{ filteredDonors[0]?.school || '—' }}</p>
              <p class="text-slate-600 mb-4">{{ filteredDonors[0]?.region || '—' }}</p>
              <div class="impact-highlight" v-if="filteredDonors[0]">
                <strong class="text-lg">${{ filteredDonors[0].amount.toLocaleString() }}</strong> donated
              </div>
            </div>
          </article>

          <!-- 3rd -->
          <article class="story-card campaign-card animate-slide-right order-3" style="animation-delay:.25s">
            <div class="campaign-badges">
              <span class="trust-badge urgent-low">#3</span>
            </div>
            <div class="campaign-image-wrapper h-44">
              <img class="w-full h-full object-cover"
                   src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&q=80"
                   alt="Third place donor">
            </div>
            <div class="p-6">
              <h3 class="text-lg font-weight-700 text-slate-900 mb-1">
                {{ filteredDonors[2]?.name || '—' }}
              </h3>
              <p class="text-slate-600 mb-1">{{ filteredDonors[2]?.school || '—' }}</p>
              <p class="text-slate-600 mb-4">{{ filteredDonors[2]?.region || '—' }}</p>
              <div class="impact-highlight" v-if="filteredDonors[2]">
                <strong>${{ filteredDonors[2].amount.toLocaleString() }}</strong> donated
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Full rankings -->
    <section class="section-white">
      <div class="container py-20">
        <div class="card p-8">
          <h3 class="text-2xl font-weight-700 text-slate-900 mb-6 text-center">Complete Rankings</h3>

          <div class="social-proof mb-6">
            Showing {{ filteredDonors.length }} donors
            <span v-if="selectedPeriod !== 'all'"> for {{ timePeriods.find(p=>p.value===selectedPeriod)?.label.toLowerCase() }}</span>
            <span v-if="selectedRegion"> in {{ selectedRegion }}</span>
            <span v-if="selectedSchool"> from {{ selectedSchool }}</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b-2 border-slate-200">
                  <th class="text-left py-3 px-2 font-weight-700 text-slate-900">Rank</th>
                  <th class="text-left py-3 px-2 font-weight-700 text-slate-900">Donor</th>
                  <th class="text-left py-3 px-2 font-weight-700 text-slate-900">School/Org</th>
                  <th class="text-left py-3 px-2 font-weight-700 text-slate-900">Region</th>
                  <th class="text-right py-3 px-2 font-weight-700 text-slate-900">Amount</th>
                  <th class="text-center py-3 px-2 font-weight-700 text-slate-900">Badge</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(donor, idx) in paginatedDonors" :key="donor.id"
                    class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                  <td class="py-3 px-2">
                    <div class="flex items-center">
                      <span class="font-weight-700 text-lg text-slate-700">
                        {{ (currentPage - 1) * itemsPerPage + idx + 1 }}
                      </span>
                      <span v-if="(currentPage - 1) * itemsPerPage + idx < 3" class="ml-2">
                        {{
                          (currentPage - 1) * itemsPerPage + idx === 0 ? '🥇'
                          : (currentPage - 1) * itemsPerPage + idx === 1 ? '🥈'
                          : '🥉'
                        }}
                      </span>
                    </div>
                  </td>

                  <td class="py-3 px-2">
                    <div class="flex items-center gap-3">
                      <div class="badge-preview-image bg-white flex items-center justify-center text-slate-700 font-weight-700 text-sm">
                        {{ donor.name.charAt(0) }}
                      </div>
                      <div>
                        <div class="font-weight-600 text-slate-900">{{ donor.name }}</div>
                        <div class="text-sm text-slate-500">{{ donor.donationCount }} donations</div>
                      </div>
                    </div>
                  </td>

                  <td class="py-3 px-2">
                    <div class="font-weight-500 text-slate-700">{{ donor.school }}</div>
                  </td>

                  <td class="py-3 px-2">
                    <span class="trust-badge" :style="regionChipStyle(donor.region)">{{ donor.region }}</span>
                  </td>

                  <td class="py-3 px-2 text-right">
                    <span class="font-weight-700 text-lg text-green-700">
                      ${{ donor.amount.toLocaleString() }}
                    </span>
                  </td>

                  <td class="py-3 px-2 text-center">
                    <span class="trust-badge" :style="tierStyle(donor.amount)">{{ tierText(donor.amount) }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="flex justify-between items-center mt-8" v-if="totalPages > 1">
            <div class="text-slate-600">
              Showing {{ (currentPage - 1) * itemsPerPage + 1 }}
              to {{ Math.min(currentPage * itemsPerPage, filteredDonors.length) }}
              of {{ filteredDonors.length }} results
            </div>

            <div class="flex items-center gap-6">
              <div class="flex gap-2">
                <button
                  class="btn-secondary"
                  style="padding:.5rem 1rem;border-radius:12px"
                  :disabled="currentPage===1"
                  @click="currentPage = Math.max(1, currentPage - 1)"
                >
                  Previous
                </button>

                <button
                  v-for="p in visiblePages" :key="p"
                  class="trust-badge"
                  :style="p===currentPage ? {background:'linear-gradient(90deg,#8b5cf6,#7c3aed)', color:'#fff', borderColor:'#7c3aed'} : {}"
                  @click="currentPage = p"
                >
                  {{ p }}
                </button>

                <button
                  class="btn-secondary"
                  style="padding:.5rem 1rem;border-radius:12px"
                  :disabled="currentPage===totalPages"
                  @click="currentPage = Math.min(totalPages, currentPage + 1)"
                >
                  Next
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="container py-16 text-center text-white">
        <h2 class="text-shadow">Join our community of changemakers</h2>
        <p class="mt-3 opacity-90">Every gift matters. See your name climb the board as your impact grows.</p>
        <div class="mt-6">
          <a href="/donate?[]" class="btn-donate">Make a Donation</a> <!--add code here!-->
        </div>
      </div>
    </section>
  </div>
</template>
