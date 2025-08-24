<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// API Configuration
const API_BASE_URL = 'http://localhost:8080/campaign'

// Stock photos pool for campaign images (fallback for display)
const stockPhotos = [
  "https://media.istockphoto.com/id/497000834/photo/little-asian-boy.jpg?s=612x612&w=0&k=20&c=bMs3BE39UAVO-ocjTfvLKD8Aq2YEM6TB2cH3xPUS_JM=", // School building
  "https://media.istockphoto.com/id/1437682932/photo/a-close-up-of-a-young-boy-smiling-at-the-park.jpg?s=612x612&w=0&k=20&c=_qh6OfA_9i7Udj-2LcXlLtSuht8E9HYNdT7WEVdqHq8=", // Students studying
  "https://thumbs.dreamstime.com/b/cute-asian-kids-5233885.jpg", // Classroom tech
  "https://st2.depositphotos.com/1930953/7447/i/950/depositphotos_74478231-stock-photo-asian-children-playing-with-magnifier.jpg", // School playground
  "https://plus.unsplash.com/premium_photo-1682095589825-d43015141de6?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDMwfHx8ZW58MHx8fHx8", // School supplies
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVtBOBTckxEHHy7GzECapZp75njAzSUfUtBw&s", // Students reading
  "https://imageio.forbes.com/specials-images/imageserve/644955ee63363c62512a02d3/0x0.jpg?format=jpg&height=600&width=1200&fit=bounds", // School library
]

// Region mapping for Hong Kong districts
const regionMapping = {
  'Wan Chai': 'Hong Kong Island',
  'Central': 'Hong Kong Island',
  'Admiralty': 'Hong Kong Island',
  'Sheung Wan': 'Hong Kong Island',
  'Causeway Bay': 'Hong Kong Island',
  'North Point': 'Hong Kong Island',
  'Quarry Bay': 'Hong Kong Island',
  'Tai Koo': 'Hong Kong Island',
  'Chai Wan': 'Hong Kong Island',
  'Stanley': 'Hong Kong Island',
  'Aberdeen': 'Hong Kong Island',
  'Repulse Bay': 'Hong Kong Island',
  'Tsim Sha Tsui': 'Kowloon',
  'Mong Kok': 'Kowloon',
  'Yau Ma Tei': 'Kowloon',
  'Jordan': 'Kowloon',
  'Sham Shui Po': 'Kowloon',
  'Kowloon Tong': 'Kowloon',
  'Kwun Tong': 'Kowloon',
  'Diamond Hill': 'Kowloon',
  'Wong Tai Sin': 'Kowloon',
  'Kowloon City': 'Kowloon',
  'To Kwa Wan': 'Kowloon',
  'Hung Hom': 'Kowloon',
  'Lai Chi Kok': 'Kowloon',
  'Cheung Sha Wan': 'Kowloon',
  'Sha Tin': 'New Territories East',
  'Tai Po': 'New Territories East',
  'Fanling': 'New Territories East',
  'Sheung Shui': 'New Territories East',
  'Ma On Shan': 'New Territories East',
  'Sai Kung': 'New Territories East',
  'Tseung Kwan O': 'New Territories East',
  'Tsuen Wan': 'New Territories West',
  'Tuen Mun': 'New Territories West',
  'Yuen Long': 'New Territories West',
  'Tin Shui Wai': 'New Territories West',
  'Tung Chung': 'New Territories West',
  'Tai Wai': 'New Territories West',
  'Kwai Chung': 'New Territories West',
  'Tsing Yi': 'New Territories West'
}

// Reactive data
const campaigns = ref([])
const loading = ref(false)
const error = ref(null)

// Filters & search
const query = ref('')
const selectedRegion = ref('All')
const selectedStatus = ref('All')
const regions = ["All", "Hong Kong Island", "Kowloon", "New Territories East", "New Territories West"]
const statuses = ["All", "Active", "Completed", "Closed"]

// Helper functions
const progressPct = (r, g) => Math.min(100, Math.round((r / g) * 100))
const formatAmt = (n) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n)
const formatDate = (d) =>
  new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })

// Get region from school name or description
function extractRegion(schoolName, description) {
  const text = `${schoolName} ${description}`.toLowerCase()
  for (const [district, region] of Object.entries(regionMapping)) {
    if (text.includes(district.toLowerCase())) return region
  }
  if (text.includes('island') || text.includes('central') || text.includes('wan chai')) return 'Hong Kong Island'
  if (text.includes('kowloon') || text.includes('tsim sha tsui') || text.includes('mong kok')) return 'Kowloon'
  if (text.includes('sha tin') || text.includes('tai po') || text.includes('sai kung')) return 'New Territories East'
  if (text.includes('tuen mun') || text.includes('yuen long') || text.includes('tsuen wan')) return 'New Territories West'
  const randomRegions = ['Hong Kong Island', 'Kowloon', 'New Territories East', 'New Territories West']
  return randomRegions[Math.floor(Math.random() * randomRegions.length)]
}

// Map backend status to frontend status
function mapStatus(backendStatus) {
  switch(backendStatus?.toLowerCase()) {
    case 'open': return 'Active'
    case 'finished': return 'Completed'
    case 'closed': return 'Closed'
    default: return 'Active'
  }
}

// Check if campaign is currently active (within date range and open status)
function isActiveCampaign(campaign) {
  const now = new Date()
  const endDate = new Date(campaign.end_date)
  return campaign.status === 'open' && endDate > now
}

// API Functions
async function fetchCampaigns() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`${API_BASE_URL}/`)
    const result = await response.json()
    if (result.status === 'success') {
      campaigns.value = result.data
        .filter(campaign => isActiveCampaign(campaign))
        .map((campaign) => {
          const schoolName = extractSchoolName(campaign.name)
          const region = extractRegion(schoolName, campaign.description)
          console.log(campaign)
          return {
            id: campaign.campaign_id,
            title: campaign.name,
            school: schoolName,
            region,
            description: campaign.description,
            // RANDOM mock photo:
            image: stockPhotos[Math.floor(Math.random() * stockPhotos.length)],
            startDate: campaign.created_at ? campaign.created_at.split('T')[0] : new Date().toISOString().split('T')[0],
            endDate: campaign.end_date,
            goal: campaign.goal_amount || 0,
            raised: campaign.current_amount || 0,
            supporters: Math.floor(Math.random() * 300) + 50,
            status: mapStatus(campaign.status)
          }
        })
    } else {
      error.value = result.message || 'Failed to fetch campaigns'
      campaigns.value = []
    }
  } catch (err) {
    error.value = 'Network error: Unable to fetch campaigns. Please try again later.'
    console.error('Error fetching campaigns:', err)
    campaigns.value = []
  } finally {
    loading.value = false
  }
}

// Extract school name from campaign name (keep your heuristic)
function extractSchoolName(campaignName) {
  const schoolKeywords = ['school', 'college', 'academy', 'institute', 'kindergarten', 'kg', 'primary', 'secondary']
  const name = campaignName.toLowerCase()
  if (schoolKeywords.some(keyword => name.includes(keyword))) {
    return campaignName + ' School'
  }
  const schoolPrefixes = [
    'Hong Kong International', 'Island Christian', 'Kowloon Junior', 'New Territories',
    'Discovery Bay', 'Canadian International', 'German Swiss International', 'French International',
    'Australian International', 'Diocesan Boys\'', 'Diocesan Girls\'', 'La Salle', 'St. Paul\'s',
    'Wah Yan', 'Maryknoll', 'Po Leung Kuk'
  ]
  const schoolSuffixes = [
    'Primary School', 'Secondary School', 'International School', 'College', 'Academy', 'Kindergarten'
  ]
  const prefix = schoolPrefixes[Math.floor(Math.random() * schoolPrefixes.length)]
  const suffix = schoolSuffixes[Math.floor(Math.random() * schoolSuffixes.length)]
  return `${prefix} ${suffix}`
}

// Computed filtered campaigns
const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return campaigns.value.filter(c => {
    const matchesRegion = selectedRegion.value === 'All' || c.region === selectedRegion.value
    const matchesStatus = selectedStatus.value === 'All' || c.status === selectedStatus.value
    const matchesQuery =
      !q ||
      c.title.toLowerCase().includes(q) ||
      c.school.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q)
    return matchesRegion && matchesStatus && matchesQuery
  })
})

// Clear all filters
function clearFilters() {
  query.value = ''
  selectedRegion.value = 'All'
  selectedStatus.value = 'All'
}

// 👉 Go to payment page with the campaign id in the query string
function goToDonate(c) {
  router.push({ path: '/payment', query: { campaignid: c.id } })
}

onMounted(() => {
  fetchCampaigns()
})
</script>

<template>
  <!-- ERROR ALERT -->
  <div v-if="error" class="error-alert" style="background: linear-gradient(145deg, #fef2f2, #fff); border: 2px solid #dc2626; color: #dc2626; padding: 1rem 2rem; border-radius: 16px; margin: 1rem auto; max-width: 1200px; text-align: center; font-weight: 600; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);">
    ⚠️ {{ error }}
    <button @click="error = null; fetchCampaigns()" style="margin-left: 1rem; background: none; border: none; color: #dc2626; font-weight: 700; cursor: pointer;">↻ Retry</button>
  </div>

  <!-- LOADING OVERLAY -->
  <div v-if="loading" class="loading-overlay" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 9999;">
    <div class="loading-content" style="background: white; padding: 2rem; border-radius: 20px; text-align: center; box-shadow: 0 12px 36px rgba(0, 0, 0, 0.15);">
      <div class="spinner" style="width: 60px; height: 60px; margin: 0 auto 1rem; border: 4px solid #e2e8f0; border-top: 4px solid #8b5cf6; border-radius: 50%; animation: spin 1s linear infinite;"></div>
      <p style="font-weight: 600; color: #1e293b;">Loading campaigns...</p>
    </div>
  </div>

  <!-- HERO -->
  <header
    class="hero-photo tint-dark text-white"
    style="--hero-bg:url('https://reach.org.hk/_assets/media/bccd049f097f1b6c3fa333cefd16ff30.jpg')"
>
    <div class="container py-20 md:py-28 text-center">
      <span class="trust-badge mb-6 inline-block">Live Campaigns</span>
      <h1 class="hero-title text-white animate-slide-up">
        Browse <span class="text-gradient">Active Campaigns</span>
      </h1>
      <p class="hero-lead text-white opacity-90 max-w-3xl mx-auto animate-fade-in">
        Discover and support ongoing campaigns across Hong Kong schools and communities. Make a difference today.
      </p>
      
      <div class="mt-8">
        <div class="social-proof">
          <span v-if="!loading">{{ campaigns.length }} active campaigns • {{ campaigns.reduce((sum, c) => sum + c.supporters, 0) }} supporters</span>
          <span v-else>Loading campaign data...</span>
        </div>
      </div>
    </div>
  </header>

  <!-- CONTENT WITH STICKY FILTERS -->
  <section class="section-white">
    <div class="container py-14">
      <div class="grid md:grid-cols-[320px,1fr] gap-8">
        <!-- Filters sidebar -->
        <aside class="card p-6 filters-sticky animate-slide-left">
          <h3 class="text-xl font-weight-700 text-slate-900 mb-4">Filter campaigns</h3>

          <div class="mb-4">
            <label class="form-label">Search</label>
            <div class="flex gap-2">
              <input 
                v-model="query" 
                class="form-input" 
                type="search" 
                placeholder="Campaign name or school..."
                :disabled="loading"
              />
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label">Region</label>
            <select v-model="selectedRegion" class="campaign-sort w-full" :disabled="loading">
              <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>

          <!-- Status filter kept for future use
          <div class="mb-6">
            <label class="form-label">Status</label>
            <select v-model="selectedStatus" class="campaign-sort w-full" :disabled="loading">
              <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
            </select>
          </div> -->

          <div class="flex gap-3">
            <button 
              class="btn-secondary flex-1" 
              @click="clearFilters"
              :disabled="loading"
            >
              Clear Filters
            </button>
            <button 
              class="action-btn secondary flex-1" 
              @click="fetchCampaigns"
              :disabled="loading"
            >
              {{ loading ? 'Loading...' : 'Apply Filters' }}
            </button>
          </div>
        </aside>

        <!-- Results -->
        <div id="results">
          <div class="social-proof mb-6">
            <span v-if="!loading">
              Showing <strong>{{ filtered.length }}</strong> of <strong>{{ campaigns.length }}</strong> active campaigns
              <span v-if="selectedRegion !== 'All'"> • Region: <strong>{{ selectedRegion }}</strong></span>
              <span v-if="selectedStatus !== 'All'"> • Status: <strong>{{ selectedStatus }}</strong></span>
              <span v-if="query"> • Search: <strong>"{{ query }}"</strong></span>
            </span>
            <span v-else>Loading campaigns...</span>
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
                  <span class="trust-badge urgent-low">{{ c.status }}</span>
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
                      <div class="text-sm text-slate-600">Started</div>
                      <div class="font-weight-600 text-slate-900 mt-1">{{ formatDate(c.startDate) }}</div>
                    </div>
                    <div>
                      <div class="text-sm text-slate-600">Ends</div>
                      <div class="font-weight-600 text-slate-900 mt-1">{{ formatDate(c.endDate) }}</div>
                    </div>
                  </div>
                </div>

                <!-- Progress -->
                <div class="mt-4">
                  <div class="flex justify-between items-center mb-2">
                    <div>
                      <div class="font-weight-700 text-slate-900">{{ formatAmt(c.raised).replace('$', 'HK$') }}</div>
                      <div class="text-sm text-slate-600">of {{ formatAmt(c.goal).replace('$', 'HK$') }}</div>
                    </div>
                    <span class="trust-badge urgent-medium">
                      {{ progressPct(c.raised, c.goal) }}% funded
                    </span>
                  </div>
                  <div class="progress-bar-large">
                    <div 
                      class="progress-fill-large" 
                      :style="{ width: progressPct(c.raised, c.goal) + '%' }"
                    ></div>
                  </div>
                  <div class="text-sm text-slate-600 mt-2 text-center">{{ c.supporters }} supporters</div>
                </div>

                <!-- Actions -->
                <div class="mt-6 flex gap-3">
                  <button class="btn-donate flex-1" @click="goToDonate(c)">
                    Donate Now
                  </button>
                  <button class="btn-secondary flex-1" @click="alert(`Learn more about: ${c.title}`)">
                    Learn More
                  </button>
                </div>
              </div>
            </article>
          </div>

          <!-- Empty state -->
          <div v-if="filtered.length === 0 && !loading" class="card p-8 mt-8 text-center">
            <div class="trust-badge urgent-medium mb-4 inline-block">No campaigns found</div>
            <h3 class="text-xl font-weight-700 text-slate-900 mb-2">No active campaigns match your filters</h3>
            <p class="text-slate-600 mb-6">Try clearing filters or changing your search criteria.</p>
            <button @click="clearFilters" class="btn-donate">Clear All Filters</button>
          </div>

          <!-- No campaigns at all -->
          <div v-if="campaigns.length === 0 && !loading && !error" class="card p-8 mt-8 text-center">
            <div class="trust-badge urgent-high mb-4 inline-block">No Active Campaigns</div>
            <h3 class="text-xl font-weight-700 text-slate-900 mb-2">No campaigns are currently running</h3>
            <p class="text-slate-600 mb-6">Check back later for new campaigns or contact us to start one.</p>
            <button @click="fetchCampaigns" class="btn-donate">Refresh</button>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- STATISTICS SECTION -->
  <section v-if="campaigns.length > 0" class="section-gradient">
    <div class="container py-16">
      <div class="text-center">
        <h2 class="text-slate-900">Campaign Impact</h2>
        <p class="mt-2 text-slate-600">Current active campaigns across Hong Kong</p>
        
        <div class="grid md:grid-cols-4 gap-6 mt-10">
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.length }}</div>
            <p>Active Campaigns</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ formatAmt(campaigns.reduce((sum, c) => sum + c.raised, 0)).replace('$', 'HK$') }}</div>
            <p>Total Raised</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ formatAmt(campaigns.reduce((sum, c) => sum + c.goal, 0)).replace('$', 'HK$') }}</div>
            <p>Total Goal</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.reduce((sum, c) => sum + c.supporters, 0) }}</div>
            <p>Total Supporters</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

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
  flex-wrap: wrap;
  gap: 0.5rem;
}

.days-remaining-badge {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
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

.campaign-sort:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Enhanced form styling */
.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.form-input {
  background: white;
  border: 2px solid #e2e8f0;
  color: #1e293b;
  font-weight: 500;
  padding: 0.875rem 1rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-size: 1rem;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-input::placeholder {
  color: #94a3b8;
}

/* Action buttons */
.action-btn {
  background: white;
  border: 2px solid #e2e8f0;
  color: #64748b;
  font-weight: 600;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  text-align: center;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.action-btn.secondary {
  border-color: #8b5cf6;
  color: #8b5cf6;
  background: linear-gradient(145deg, #faf5ff, #fff);
}

.action-btn.secondary:hover:not(:disabled) {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

/* Loading overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.15);
}

/* Error alert */
.error-alert {
  background: linear-gradient(145deg, #fef2f2, #fff);
  border: 2px solid #dc2626;
  color: #dc2626;
  padding: 1rem 2rem;
  border-radius: 16px;
  margin: 1rem auto;
  max-width: 1200px;
  text-align: center;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .campaign-badges {
    flex-direction: column;
    align-items: flex-start;
  }
  .days-remaining-badge {
    align-self: flex-end;
  }
  .form-input {
    font-size: 0.9rem;
    padding: 0.75rem 0.875rem;
  }
  .campaign-sort {
    font-size: 0.85rem;
    padding: 0.625rem 0.875rem;
  }
  .action-btn {
    font-size: 0.85rem;
    padding: 0.625rem 0.875rem;
  }
}

/* Enhanced accessibility */
.action-btn:focus,
.campaign-sort:focus,
.form-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3);
}

/* Animation delays for staggered entrance */
.story-card.campaign-card:nth-child(1) { animation-delay: 0.1s; }
.story-card.campaign-card:nth-child(2) { animation-delay: 0.2s; }
.story-card.campaign-card:nth-child(3) { animation-delay: 0.3s; }
.story-card.campaign-card:nth-child(4) { animation-delay: 0.4s; }
.story-card.campaign-card:nth-child(5) { animation-delay: 0.5s; }
.story-card.campaign-card:nth-child(6) { animation-delay: 0.6s; }

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .story-card.campaign-card { animation: none; }
}
</style>
