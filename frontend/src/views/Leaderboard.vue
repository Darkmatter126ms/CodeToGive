<script setup>
import { ref, computed, onMounted } from 'vue'

// --- API bases (match your Flask ports) ---
const DONOR_API    = 'http://localhost:8081/donor'
const DONATION_API = 'http://localhost:8084/donation'
const CAMPAIGN_API = 'http://localhost:8080/campaign'

// --- State ---
const loading = ref(false)
const error   = ref(null)

const donors     = ref([])      // raw donors
const donations  = ref([])      // raw donations
const campaigns  = ref([])      // raw campaigns

// Filters (kept from your UI)
const timeWindow = ref('all')   // all | year | month | week
const regionFilter = ref('All Regions')
const schoolFilter = ref('All Schools')

// Region mapping (fallback inference from text)
const regionMapping = {
  'Wan Chai':'Hong Kong Island','Central':'Hong Kong Island','Admiralty':'Hong Kong Island','Sheung Wan':'Hong Kong Island','Causeway Bay':'Hong Kong Island','North Point':'Hong Kong Island','Quarry Bay':'Hong Kong Island','Tai Koo':'Hong Kong Island','Chai Wan':'Hong Kong Island','Stanley':'Hong Kong Island','Aberdeen':'Hong Kong Island','Repulse Bay':'Hong Kong Island',
  'Tsim Sha Tsui':'Kowloon','Mong Kok':'Kowloon','Yau Ma Tei':'Kowloon','Jordan':'Kowloon','Sham Shui Po':'Kowloon','Kowloon Tong':'Kowloon','Kwun Tong':'Kowloon','Diamond Hill':'Kowloon','Wong Tai Sin':'Kowloon','Kowloon City':'Kowloon','To Kwa Wan':'Kowloon','Hung Hom':'Kowloon','Lai Chi Kok':'Kowloon','Cheung Sha Wan':'Kowloon',
  'Sha Tin':'New Territories East','Tai Po':'New Territories East','Fanling':'New Territories East','Sheung Shui':'New Territories East','Ma On Shan':'New Territories East','Sai Kung':'New Territories East','Tseung Kwan O':'New Territories East',
  'Tsuen Wan':'New Territories West','Tuen Mun':'New Territories West','Yuen Long':'New Territories West','Tin Shui Wai':'New Territories West','Tung Chung':'New Territories West','Tai Wai':'New Territories West','Kwai Chung':'New Territories West','Tsing Yi':'New Territories West'
}
const regionOptions = ['All Regions','Hong Kong Island','Kowloon','New Territories East','New Territories West']

// --- Helpers ---
const fmtHKD = n => new Intl.NumberFormat('en-US', { style:'currency', currency:'HKD', maximumFractionDigits:0 }).format(Number(n||0))
const initialBadge = name => (name?.trim()?.charAt(0) || '•').toUpperCase()

function inferRegionFromText(text='') {
  const t = String(text).toLowerCase()
  for (const [district, region] of Object.entries(regionMapping)) {
    if (t.includes(district.toLowerCase())) return region
  }
  if (t.includes('kowloon')) return 'Kowloon'
  if (t.includes('tsuen wan') || t.includes('yuen long') || t.includes('tuen mun')) return 'New Territories West'
  if (t.includes('sha tin') || t.includes('tai po') || t.includes('sai kung')) return 'New Territories East'
  return 'Hong Kong Island'
}

function tierFor(amount) {
  const a = Number(amount||0)
  if (a >= 50000) return {label:'Platinum', cls:'badge-platinum'}
  if (a >= 10000) return {label:'Gold',     cls:'badge-gold'}
  if (a >=  5000) return {label:'Silver',   cls:'badge-silver'}
  if (a >=  1000) return {label:'Bronze',   cls:'badge-bronze'}
  return {label:'Supporter', cls:'badge-supporter'}
}

function inWindow(createdAt, win) {
  if (win === 'all') return true
  const ts = createdAt ?? null
  const d = ts ? new Date(ts) : null
  if (!d || isNaN(d)) return true // include if no timestamp
  const now = new Date()
  if (win === 'year')  return d >= new Date(now.getFullYear(),0,1)
  if (win === 'month') return d >= new Date(now.getFullYear(),now.getMonth(),1)
  if (win === 'week')  return d >= new Date(now.getFullYear(),now.getMonth(),now.getDate()-7)
  return true
}

// --- Fetchers ---
async function fetchAll() {
  loading.value = true
  error.value = null
  try {
    const [donorRes, donationRes, campaignRes] = await Promise.all([
      fetch(`${DONOR_API}/`),
      fetch(`${DONATION_API}/`),
      fetch(`${CAMPAIGN_API}/`)
    ])
    const donorsJson    = await donorRes.json().catch(()=>({status:'error'}))
    const donationsJson = await donationRes.json().catch(()=>({status:'error'}))
    const campaignsJson = await campaignRes.json().catch(()=>({status:'error'}))

    donors.value    = donorsJson?.status === 'success' ? (donorsJson.data || [])       : []
    donations.value = donationsJson?.status === 'success' ? (donationsJson.data || []) : []
    campaigns.value = campaignsJson?.status === 'success' ? (campaignsJson.data || []) : []

    // Hard fallback to keep UI pretty if backend empty
    if (!donors.value.length && !donations.value.length) {
      donors.value = mockDonors.map(d => ({ donor_id:d.id, name:d.name, email:d.email }))
      donations.value = mockDonations
      campaigns.value = mockCampaigns
    }
  } catch (e) {
    error.value = 'Failed to load leaderboard. Showing mock data.'
    donors.value    = mockDonors.map(d => ({ donor_id:d.id, name:d.name, email:d.email }))
    donations.value = mockDonations
    campaigns.value = mockCampaigns
  } finally {
    loading.value = false
  }
}

// --- Join & aggregate ---
const campaignById = computed(() => {
  const m = new Map()
  for (const c of campaigns.value) m.set(c.campaign_id, c)
  return m
})

const leaderboard = computed(() => {
  // Accept a variety of timestamp field names just in case
  const filteredDonations = donations.value.filter(d =>
    inWindow(d.created_at ?? d.createdAt ?? d.timestamp, timeWindow.value)
  )

  // Sum by donor
  const sums = new Map() // donor_id -> { total, count, campaignIds:Set, latestAt }
  for (const d of filteredDonations) {
    const id = d.donor_id
    if (!id) continue
    if (!sums.has(id)) sums.set(id, { total:0, count:0, campaignIds:new Set(), latestAt:null })
    const entry = sums.get(id)
    entry.total += Number(d.amount || 0)
    entry.count += 1
    if (d.campaign_id) entry.campaignIds.add(d.campaign_id)
    const ts = d.created_at ?? d.createdAt ?? d.timestamp
    if (ts) {
      const t = new Date(ts)
      entry.latestAt = entry.latestAt ? (t > entry.latestAt ? t : entry.latestAt) : t
    }
  }

  // Build rows
  const rows = []
  for (const [donor_id, agg] of sums.entries()) {
    const donor = donors.value.find(x => x.donor_id === donor_id) || {}
    const campaignNames = [...agg.campaignIds].map(id => campaignById.value.get(id)?.name).filter(Boolean)
    const reg = campaignNames.length ? inferRegionFromText(campaignNames[0]) : 'Hong Kong Island'
    const tier = tierFor(agg.total)

    rows.push({
      donor_id,
      donor_name: donor.name || 'Anonymous Donor',
      email: donor.email || '',
      total: agg.total,
      count: agg.count,
      campaigns: campaignNames,
      region: reg,
      badge: tier.label,
      badgeCls: tier.cls,
      latestAt: agg.latestAt
    })
  }

  // Optional region / school filters
  const regionSel = regionFilter.value
  const schoolSel = schoolFilter.value
  const filtered = rows.filter(r => {
    const okRegion = regionSel === 'All Regions' || r.region === regionSel
    const okSchool = schoolSel === 'All Schools' || r.campaigns.includes(schoolSel)
    return okRegion && okSchool
  })

  filtered.sort((a,b) => b.total - a.total)
  return filtered.map((r, i) => ({ rank: i+1, ...r }))
})

// --- Header stats ---
const statTotalDonors  = computed(() => leaderboard.value.length)
const statTotalRaised  = computed(() => leaderboard.value.reduce((s,r)=>s+r.total,0))
const statActiveSchools= computed(() => new Set(leaderboard.value.flatMap(r=>r.campaigns)).size)
const statRegions      = computed(() => new Set(leaderboard.value.map(r=>r.region)).size)

// --- Mock data (only used if API fails/empty) ---
const mockCampaigns = [
  { campaign_id: 1, name:'Hong Kong International School Library Fund' },
  { campaign_id: 2, name:'Kowloon STEM Lab Upgrade' },
  { campaign_id: 3, name:'New Territories East Wellness Program' },
]
const mockDonors = [
  { id: 101, name:'Corporate Sponsor A', email:'corp-a@example.com' },
  { id: 102, name:'Foundation Partner',  email:'foundation@example.com' },
  { id: 103, name:'Anonymous Donor',     email:'' },
]
const mockDonations = [
  { donation_id:1, donor_id:101, campaign_id:1, amount:60000, created_at:'2024-01-05T10:00:00Z' },
  { donation_id:2, donor_id:102, campaign_id:2, amount:25000, created_at:'2024-02-09T10:00:00Z' },
  { donation_id:3, donor_id:103, campaign_id:3, amount:12000, created_at:'2024-02-15T11:12:00Z' },
]

// --- Lifecycle ---
onMounted(fetchAll)
</script>

<template>
  <!-- HERO -->
  <header class="hero-gradient hero-pattern">
    <div class="container py-16 md:py-20 text-center">
      <span class="trust-badge mb-4 inline-block">Donor Leaderboard</span>
      <h1 class="hero-title text-white text-shadow">Top <span class="text-gradient">Contributors</span></h1>
      <p class="hero-lead text-white opacity-90 max-w-3xl mx-auto">
        Ranked by total donated amount across all campaigns.
      </p>
    </div>
  </header>

  <!-- ERROR -->
  <div v-if="error" class="error-alert" style="margin-top:1rem;">
    ⚠️ {{ error }}
  </div>

  <!-- STATS -->
  <section class="section-white">
    <div class="container py-10">
      <div class="grid md:grid-cols-4 gap-6 stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ statTotalDonors }}</div>
          <p>Total Donors</p>
        </div>
        <div class="stat-card">
          <!-- smaller money typography -->
          <div class="stat-number hk-amount">{{ fmtHKD(statTotalRaised) }}</div>
          <p>Total Raised</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ statActiveSchools }}</div>
          <p>Active Campaigns</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ statRegions }}</div>
          <p>Regions</p>
        </div>
      </div>
    </div>
  </section>

  <!-- FILTER CARD -->
  <section class="section-white pt-0">
    <div class="container">
      <div class="card p-6 filter-card max-w-3xl mx-auto">
        <h3 class="text-center text-slate-900 font-weight-700 mb-4">Filter Rankings</h3>

        <div class="filter-pills">
          <button class="filter-pill" :class="{active: timeWindow==='all'}"   @click="timeWindow='all'">All Time</button>
          <button class="filter-pill" :class="{active: timeWindow==='year'}"  @click="timeWindow='year'">This Year</button>
          <button class="filter-pill" :class="{active: timeWindow==='month'}" @click="timeWindow='month'">This Month</button>
          <button class="filter-pill" :class="{active: timeWindow==='week'}"  @click="timeWindow='week'">This Week</button>
        </div>

        <div class="grid md:grid-cols-2 gap-3 mt-4">
          <select v-model="regionFilter" class="campaign-sort w-full">
            <option v-for="r in regionOptions" :key="r" :value="r">{{ r }}</option>
          </select>
          <select v-model="schoolFilter" class="campaign-sort w-full">
            <option>All Schools</option>
            <option v-for="n in [...new Set(leaderboard.flatMap(r=>r.campaigns))]" :key="n">{{ n }}</option>
          </select>
        </div>
      </div>
    </div>
  </section>

  <!-- TOP CONTRIBUTORS (restored) -->
  <section v-if="leaderboard.length > 0" class="section-light top3">
    <div class="container py-12">
      <h2 class="text-center text-2xl md:text-3xl font-weight-700 text-slate-900 mb-8 py-20">Top Contributors</h2>

      <div class="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <!-- #2 -->
        <article v-if="leaderboard[1]" class="story-card campaign-card animate-slide-left order-2 md:order-1" style="animation-delay:.15s">
          <div class="p-8 text-center">
            <div class="flex items-center justify-center w-20 h-20 mx-auto mb-4 rounded-full"
                 style="background: linear-gradient(135deg, #64748b, #475569); color: #fff;">
              <span class="text-2xl">🥈</span>
            </div>
            <span class="trust-badge urgent-medium mb-4 inline-block">#2</span>
            <h3 class="text-lg font-weight-700 text-slate-900 mb-1">{{ leaderboard[1].donor_name }}</h3>
            <p class="text-slate-600 mb-1">{{ leaderboard[1].campaigns[0] || '—' }}</p>
            <p class="text-slate-600 mb-4">{{ leaderboard[1].region }}</p>
            <div class="impact-highlight">
              <strong>{{ fmtHKD(leaderboard[1].total) }}</strong> donated
            </div>
          </div>
        </article>

        <!-- #1 -->
        <article v-if="leaderboard[0]" class="story-card campaign-card animate-slide-up order-1 md:order-2" style="transform:scale(1.04)">
          <div class="p-8 text-center">
            <div class="flex items-center justify-center w-24 h-24 mx-auto mb-4 rounded-full"
                 style="background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #fff;">
              <span class="text-3xl">🥇</span>
            </div>
            <span class="trust-badge mb-4 inline-block" style="background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#fff;border-color:#f59e0b">
              🏆 #1
            </span>
            <h3 class="text-xl font-weight-700 text-slate-900 mb-1">{{ leaderboard[0].donor_name }}</h3>
            <p class="text-slate-600 mb-1">{{ leaderboard[0].campaigns[0] || '—' }}</p>
            <p class="text-slate-600 mb-4">{{ leaderboard[0].region }}</p>
            <div class="impact-highlight">
              <strong class="text-lg">{{ fmtHKD(leaderboard[0].total) }}</strong> donated
            </div>
          </div>
        </article>

        <!-- #3 -->
        <article v-if="leaderboard[2]" class="story-card campaign-card animate-slide-right order-3" style="animation-delay:.25s">
          <div class="p-8 text-center">
            <div class="flex items-center justify-center w-20 h-20 mx-auto mb-4 rounded-full"
                 style="background: linear-gradient(135deg, #d97706, #b45309); color: #fff;">
              <span class="text-2xl">🥉</span>
            </div>
            <span class="trust-badge urgent-low mb-4 inline-block">#3</span>
            <h3 class="text-lg font-weight-700 text-slate-900 mb-1">{{ leaderboard[2].donor_name }}</h3>
            <p class="text-slate-600 mb-1">{{ leaderboard[2].campaigns[0] || '—' }}</p>
            <p class="text-slate-600 mb-4">{{ leaderboard[2].region }}</p>
            <div class="impact-highlight">
              <strong>{{ fmtHKD(leaderboard[2].total) }}</strong> donated
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- TABLE -->
  <section class="section-white pt-0">
    <div class="container pb-16 py-16">
      <div class="card p-0 overflow-auto">
        <div class="table-header text-center py-8 text-slate-600">
          Showing {{ leaderboard.length }} donors
        </div>

        <table class="leaderboard-table">
          <thead>
            <tr>
              <th style="min-width:80px">Rank</th>
              <th>Donor</th>
              <th>Campaigns</th>
              <th>Region</th>
              <th>Amount</th>
            </tr>
          </thead>

        <tbody>
          <tr v-for="row in leaderboard" :key="row.donor_id">
            <td class="rank-cell">
              <span class="rank-number">{{ row.rank }}</span>
            </td>

            <td class="donor-cell">
              <div class="avatar">{{ initialBadge(row.donor_name) }}</div>
              <div class="donor-meta">
                <div class="donor-name">{{ row.donor_name }}</div>
                <div class="donor-sub" v-if="row.count">{{ row.count }} donations</div>
              </div>
            </td>

            <td class="school-cell">
              <div class="campaign-list">
                <span v-if="!row.campaigns.length" class="muted">—</span>
                <template v-else>
                  <span class="pill pill-light" v-for="(cname, i) in row.campaigns.slice(0,2)" :key="cname+i">{{ cname }}</span>
                  <span v-if="row.campaigns.length > 2" class="pill pill-more">+{{ row.campaigns.length - 2 }} more</span>
                </template>
              </div>
            </td>

            <td class="region-cell">
              <span class="pill">{{ row.region }}</span>
            </td>

            <td class="amount-cell">
              <span class="amount-compact">{{ fmtHKD(row.total) }}</span>
            </td>

          </tr>

          <tr v-if="!loading && leaderboard.length===0">
            <td colspan="6" class="text-center py-8 text-slate-600">No donors in this range.</td>
          </tr>
        </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- LOADING OVERLAY -->
  <div v-if="loading" class="loading-overlay">
    <div class="loading-content">
      <div class="spinner" style="width:56px;height:56px;border:4px solid #e2e8f0;border-top:4px solid #8b5cf6;border-radius:50%;animation:spin 1s linear infinite;"></div>
      <p class="mt-2">Loading leaderboard…</p>
    </div>
  </div>
</template>

<style scoped>
/* Minimal additions only; most styling comes from main.css */

/* smaller amount in the stat card */
.hk-amount {
  font-size: clamp(1.25rem, 2.6vw, 2.25rem);
  line-height: 1.1;
}

/* add space below the filter so it’s not glued to the table */
.filter-card { margin-bottom: 1.5rem; }

/* slight separation above Top Contributors block */
.top3 { margin-top: .25rem; }

/* leaderboard table tweaks */
.leaderboard-table { width:100%; border-collapse:separate; border-spacing:0; }
.leaderboard-table thead th {
  text-align:left; font-weight:700; color:#475569; padding:12px 16px; border-bottom:1px solid #e2e8f0; background:#fafafa;
}
.leaderboard-table tbody td { padding:14px 16px; border-bottom:1px solid #eef2f7; vertical-align:middle; }
.rank-cell .rank-number { font-weight:700; color:#0f172a; }

.avatar {
  width:32px;height:32px;border-radius:10px;border:2px solid #e2e8f0;display:flex;align-items:center;justify-content:center;
  font-weight:700;color:#334155;background:#f8fafc;margin-right:10px;
}
.donor-cell { display:flex; align-items:center; }
.donor-meta .donor-name { font-weight:700; color:#0f172a; }
.donor-meta .donor-sub { font-size:.8rem; color:#64748b; }

.pill { display:inline-block; padding:.35rem .6rem; border-radius:999px; background:#eef2ff; color:#1e40af; font-weight:600; font-size:.8rem; }
.pill-light { background:#f1f5f9; color:#475569; }
.pill-more { background:#ede9fe; color:#6d28d9; }

.amount-compact { font-weight:800; font-size:.95rem; color:#0f172a; }

.badge { padding:.35rem .7rem; border-radius:999px; font-weight:800; font-size:.8rem; color:#fff; }
.badge-platinum { background:linear-gradient(135deg,#94a3b8,#e2e8f0); color:#0f172a; }
.badge-gold     { background:linear-gradient(135deg,#f59e0b,#facc15); }
.badge-silver   { background:linear-gradient(135deg,#9ca3af,#e5e7eb); color:#0f172a; }
.badge-bronze   { background:linear-gradient(135deg,#b45309,#f59e0b); }
.badge-supporter{ background:linear-gradient(135deg,#64748b,#94a3b8); }

/* filter pills look/feel to match your theme */
.filter-pills { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
.filter-pill { border:none; border-radius:999px; padding:.9rem 1rem; font-weight:800; background:linear-gradient(180deg,#f4f4f5,#fff); box-shadow:inset 0 0 0 2px #eee; color:#0f172a; cursor:pointer; }
.filter-pill.active { background:linear-gradient(135deg,#ec4899,#7c3aed); color:#fff; box-shadow:0 8px 24px rgba(124,58,237,.25); }

/* simple loading overlay */
.loading-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.45);
  display:flex; align-items:center; justify-content:center; z-index: 9999;
}
.loading-content {
  background:#fff; padding:1.25rem 1.5rem; border-radius:16px; text-align:center; box-shadow:0 12px 36px rgba(0,0,0,.15);
}
</style>
