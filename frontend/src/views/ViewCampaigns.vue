<script setup>
import { ref, computed } from 'vue'

// Mock campaign data - replace with real API call
const campaigns = ref([
  {
    id: 1,
    title: "Emergency School Meals",
    description: "Provide nutritious meals to children affected by recent floods in rural communities.",
    image: "https://images.unsplash.com/photo-1498721406610-899c1d4eb77d?q=80&w=1600",
    startDate: "2025-01-15",
    endDate: "2025-03-15",
    raised: 18500,
    goal: 25000,
    badgeImage: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=400",
    urgency: "high",
    supporters: 127
  },
  {
    id: 2,
    title: "Digital Learning Kits",
    description: "Tablets and educational apps for children in remote areas to continue learning.",
    image: "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1600",
    startDate: "2024-12-01",
    endDate: "2025-04-30",
    raised: 42300,
    goal: 60000,
    badgeImage: "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?q=80&w=400",
    urgency: "medium",
    supporters: 289
  },
  {
    id: 3,
    title: "Safe Play Spaces",
    description: "Building secure playgrounds and recreation areas in underserved neighborhoods.",
    image: "https://images.unsplash.com/photo-1544717297-fa95b6ee9643?q=80&w=1600",
    startDate: "2025-02-01",
    endDate: "2025-06-01",
    raised: 8200,
    goal: 35000,
    badgeImage: "https://images.unsplash.com/photo-1559827260-dc66d52bef19?q=80&w=400",
    urgency: "low",
    supporters: 64
  },
  {
    id: 4,
    title: "Reading Corner Libraries",
    description: "Creating cozy reading spaces with diverse books in local languages.",
    image: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=1600",
    startDate: "2025-01-10",
    endDate: "2025-05-10",
    raised: 31500,
    goal: 40000,
    badgeImage: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400",
    urgency: "medium",
    supporters: 201
  },
  {
    id: 5,
    title: "Mental Health Support",
    description: "Training counselors and providing mental wellness programs for children.",
    image: "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?q=80&w=1600",
    startDate: "2025-01-20",
    endDate: "2025-07-20",
    raised: 12800,
    goal: 50000,
    badgeImage: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?q=80&w=400",
    urgency: "high",
    supporters: 98
  },
  {
    id: 6,
    title: "Clean Water Initiative",
    description: "Installing water purification systems in schools across Southeast Asia.",
    image: "https://images.unsplash.com/photo-1541919329513-35f7af297129?q=80&w=1600",
    startDate: "2024-11-15",
    endDate: "2025-08-15",
    raised: 67500,
    goal: 80000,
    badgeImage: "https://images.unsplash.com/photo-1559827260-dc66d52bef19?q=80&w=400",
    urgency: "medium",
    supporters: 445
  }
])

const selectedFilter = ref('all')
const sortBy = ref('progress')

const filters = [
  { value: 'all', label: 'All Campaigns' },
  { value: 'high', label: 'Urgent' },
  { value: 'medium', label: 'Active' },
  { value: 'low', label: 'Ongoing' }
]

const sortOptions = [
  { value: 'progress', label: 'Most Progress' },
  { value: 'recent', label: 'Most Recent' },
  { value: 'ending', label: 'Ending Soon' },
  { value: 'supporters', label: 'Most Supporters' }
]

const filteredCampaigns = computed(() => {
  let filtered = campaigns.value
  
  if (selectedFilter.value !== 'all') {
    filtered = filtered.filter(c => c.urgency === selectedFilter.value)
  }
  
  // Sort campaigns
  filtered = [...filtered].sort((a, b) => {
    switch (sortBy.value) {
      case 'progress':
        return (b.raised / b.goal) - (a.raised / a.goal)
      case 'recent':
        return new Date(b.startDate) - new Date(a.startDate)
      case 'ending':
        return new Date(a.endDate) - new Date(b.endDate)
      case 'supporters':
        return b.supporters - a.supporters
      default:
        return 0
    }
  })
  
  return filtered
})

function getProgressPercentage(raised, goal) {
  return Math.min((raised / goal) * 100, 100)
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function formatAmount(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount)
}

function getDaysRemaining(endDate) {
  const end = new Date(endDate)
  const now = new Date()
  const diffTime = end - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays > 0 ? diffDays : 0
}

function getUrgencyColor(urgency) {
  switch (urgency) {
    case 'high': return 'urgent-high'
    case 'medium': return 'urgent-medium'
    case 'low': return 'urgent-low'
    default: return ''
  }
}

function getUrgencyLabel(urgency) {
  switch (urgency) {
    case 'high': return 'Urgent'
    case 'medium': return 'Active'
    case 'low': return 'Ongoing'
    default: return ''
  }
}

function donateToCampaign(campaignId) {
  // Replace with real donation flow
  window.location.href = `https://example.org/donate?campaign=${campaignId}`
}
</script>

<template>
  <!-- HEADER -->
  <header class="hero-gradient hero-pattern">
    <div class="container py-20 md:py-28 flex justify-center">
      <div class="max-w-3xl mx-auto text-center animate-slide-up">
        <span class="trust-badge mb-6 inline-block">Current Impact Campaigns</span>
        <h1 class="hero-title text-white text-shadow">
          Choose Your <span class="text-gradient">Impact</span>
        </h1>
        <p class="hero-lead mt-4 text-white opacity-90">
          Every campaign represents real children who need your support. Browse our active initiatives 
          and see exactly how your donation creates lasting change.
        </p>
        
        <div class="social-proof mt-8">
          {{ campaigns.reduce((sum, c) => sum + c.supporters, 0) }}+ supporters across all campaigns
        </div>
      </div>
    </div>
  </header>

  <!-- FILTERS & SORTING -->
  <section class="section-light">
    <div class="container py-10">
      <div class="flex flex-wrap gap-4 items-center justify-between">
        <div class="flex flex-wrap gap-3">
          <button
            v-for="filter in filters"
            :key="filter.value"
            @click="selectedFilter = filter.value"
            class="amount-btn campaign-filter"
            :class="{ 'selected': selectedFilter === filter.value }"
          >
            {{ filter.label }}
          </button>
        </div>
        
        <div class="flex items-center gap-3">
          <label class="text-sm font-weight-600 text-slate-600">Sort by:</label>
          <select v-model="sortBy" class="campaign-sort">
            <option v-for="option in sortOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>
    </div>
  </section>

  <!-- CAMPAIGNS GRID -->
  <section class="section-white">
    <div class="container py-16">
      <div class="grid md:grid-cols-2 gap-8">
        <article
          v-for="campaign in filteredCampaigns"
          :key="campaign.id"
          class="story-card campaign-card animate-slide-up"
        >
          <!-- Campaign Image -->
          <div class="campaign-image-wrapper">
            <img
              :src="campaign.image"
              :alt="campaign.title"
              class="w-full h-44 object-cover"
            />
            <div class="campaign-badges">
              <span class="trust-badge" :class="getUrgencyColor(campaign.urgency)">
                {{ getUrgencyLabel(campaign.urgency) }}
              </span>
              <div class="days-remaining-badge">
                {{ getDaysRemaining(campaign.endDate) }} days left
              </div>
            </div>
          </div>

          <!-- Campaign Content -->
          <div class="p-6">
            <div class="mb-4">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-2">{{ campaign.title }}</h3>
              <p class="text-slate-600">{{ campaign.description }}</p>
            </div>

            <!-- Date Range using existing card styling -->
            <div class="card p-4 mb-4">
              <div class="flex justify-between text-center">
                <div>
                  <span class="text-sm text-slate-600 font-weight-500">Started</span>
                  <div class="text-slate-900 font-weight-600 mt-1">{{ formatDate(campaign.startDate) }}</div>
                </div>
                <div>
                  <span class="text-sm text-slate-600 font-weight-500">Ends</span>
                  <div class="text-slate-900 font-weight-600 mt-1">{{ formatDate(campaign.endDate) }}</div>
                </div>
              </div>
            </div>

            <!-- Progress Section -->
            <div class="mb-4">
              <div class="flex justify-between items-center mb-2">
                <div>
                  <div class="text-lg font-weight-700 text-slate-900">{{ formatAmount(campaign.raised) }}</div>
                  <div class="text-sm text-slate-600">of {{ formatAmount(campaign.goal) }}</div>
                </div>
                <div class="trust-badge">
                  {{ Math.round(getProgressPercentage(campaign.raised, campaign.goal)) }}%
                </div>
              </div>
              
              <div class="progress-bar-large mb-2">
                <div 
                  class="progress-fill-large"
                  :style="{ width: getProgressPercentage(campaign.raised, campaign.goal) + '%' }"
                ></div>
              </div>
              
              <div class="text-center text-sm text-slate-600">
                {{ campaign.supporters }} supporters
              </div>
            </div>

            <!-- Badge Preview using impact-highlight styling -->
            <div class="impact-highlight mb-4">
              <div class="flex items-center gap-3">
                <img :src="campaign.badgeImage" alt="Supporter badge" class="badge-preview-image" />
                <div>
                  <div class="font-weight-600 text-slate-900">Earn Your Badge</div>
                  <div class="text-sm text-slate-600">Share your impact on social media</div>
                </div>
              </div>
            </div>

            <!-- Action Button -->
            <button 
              @click="donateToCampaign(campaign.id)"
              class="btn-donate w-full"
            >
              Support This Campaign
            </button>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- IMPACT SUMMARY -->
  <section class="section-gradient">
    <div class="container py-16">
      <div class="text-center">
        <h2 class="text-slate-900">Combined Impact</h2>
        <p class="mt-2 text-slate-600">See the collective power of all our current campaigns</p>
        
        <div class="grid md:grid-cols-4 gap-6 mt-10">
          <div class="stat-card">
            <div class="stat-number">{{ formatAmount(campaigns.reduce((sum, c) => sum + c.raised, 0)).replace(", '") }}</div>
            <p>Total Raised</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.reduce((sum, c) => sum + c.supporters, 0) }}</div>
            <p>Total Supporters</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.length }}</div>
            <p>Active Campaigns</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ Math.round((campaigns.reduce((sum, c) => sum + (c.raised/c.goal), 0) / campaigns.length) * 100) }}%</div>
            <p>Average Progress</p>
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