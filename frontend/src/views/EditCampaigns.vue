<script setup>
import { ref, computed } from 'vue'

// Stock photos pool for random campaign images
const stockPhotos = [
  "https://images.unsplash.com/photo-1497486751825-1233686d5d80?q=80&w=1600", // School building
  "https://images.unsplash.com/photo-1580582932707-520aed937b7b?q=80&w=1600", // Students studying
  "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1600", // Classroom tech
  "https://images.unsplash.com/photo-1544717297-fa95b6ee9643?q=80&w=1600", // School playground
  "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=1600", // School supplies
  "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?q=80&w=1600", // Students reading
  "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=1600", // School library
  "https://images.unsplash.com/photo-1588072432836-e10032774350?q=80&w=1600", // School cafeteria
]

// Mock campaign data with Hong Kong schools/locations
const campaigns = ref([
  {
    id: 1,
    name: "Emergency Relief Fund",
    description: "Supporting families affected by recent typhoon damage in Tin Shui Wai district.",
    schoolName: "Tin Shui Wai Primary School",
    image: stockPhotos[0],
    startDate: "2025-01-15",
    endDate: "2025-03-15",
    raised: 18500,
    goal: 25000,
    schoolLogo: "https://images.unsplash.com/photo-1562813733-b31f71025d54?q=80&w=400",
    badgeImage: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=400",
    urgency: "high",
    supporters: 127,
    status: "open",
    newsletterSent: false
  },
  {
    id: 2,
    name: "Digital Learning Initiative",
    description: "Providing tablets and internet access for remote learning in Sham Shui Po.",
    schoolName: "Sham Shui Po Community School",
    image: stockPhotos[2],
    startDate: "2024-12-01",
    endDate: "2025-04-30",
    raised: 42300,
    goal: 60000,
    schoolLogo: "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?q=80&w=400",
    badgeImage: "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?q=80&w=400",
    urgency: "medium",
    supporters: 289,
    status: "open",
    newsletterSent: false
  },
  {
    id: 3,
    name: "School Lunch Program",
    description: "Ensuring nutritious meals for underprivileged students in Kwun Tong area.",
    schoolName: "Kwun Tong Secondary School",
    image: stockPhotos[7],
    startDate: "2024-11-01",
    endDate: "2024-12-31",
    raised: 35000,
    goal: 35000,
    schoolLogo: "https://images.unsplash.com/photo-1559827260-dc66d52bef19?q=80&w=400",
    badgeImage: "https://images.unsplash.com/photo-1559827260-dc66d52bef19?q=80&w=400",
    urgency: "low",
    supporters: 164,
    status: "finished",
    newsletterSent: false
  },
  {
    id: 4,
    name: "After School Care",
    description: "Extended childcare support for working parents in Tuen Mun district.",
    schoolName: "Tuen Mun International School",
    image: stockPhotos[5],
    startDate: "2024-09-01",
    endDate: "2024-11-30",
    raised: 28000,
    goal: 30000,
    schoolLogo: "https://images.unsplash.com/photo-1562813733-b31f71025d54?q=80&w=400",
    badgeImage: "https://images.unsplash.com/photo-1562813733-b31f71025d54?q=80&w=400",
    urgency: "medium",
    supporters: 89,
    status: "closed",
    newsletterSent: true
  }
])

// Tab management
const activeTab = ref('open')
const tabs = [
  { id: 'open', label: 'Open Campaigns', count: computed(() => campaigns.value.filter(c => c.status === 'open').length) },
  { id: 'finished', label: 'Finished', count: computed(() => campaigns.value.filter(c => c.status === 'finished').length) },
  { id: 'closed', label: 'Closed', count: computed(() => campaigns.value.filter(c => c.status === 'closed').length) }
]

// Form state
const showCreateForm = ref(false)
const showBadgeGenerator = ref(false)
const editingCampaign = ref(null)
const formData = ref({
  name: '',
  description: '',
  endDate: '',
  goal: '',
  schoolLogo: null,
  schoolLogoPreview: ''
})

// Badge generation state
const badgeThemes = [
  { id: 'cute', label: 'Cute', colors: ['#FFB6C1', '#FF69B4', '#FFD700'] },
  { id: 'prestigious', label: 'Prestigious', colors: ['#000080', '#FFD700', '#FFFFFF'] },
  { id: 'pretty', label: 'Pretty', colors: ['#E6E6FA', '#DDA0DD', '#FF1493'] },
  { id: 'nature', label: 'Nature', colors: ['#228B22', '#32CD32', '#90EE90'] },
  { id: 'modern', label: 'Modern', colors: ['#2C3E50', '#3498DB', '#ECF0F1'] }
]
const selectedTheme = ref('cute')
const generatedBadge = ref(null)
const isGeneratingBadge = ref(false)

// Form validation
const isFormValid = computed(() => {
  return formData.value.name.trim() && 
         formData.value.description.trim() && 
         formData.value.endDate && 
         formData.value.goal > 0 &&
         formData.value.schoolLogo
})

// Filtered campaigns based on active tab
const filteredCampaigns = computed(() => {
  return campaigns.value.filter(campaign => {
    if (activeTab.value === 'open') {
      return campaign.status === 'open'
    } else if (activeTab.value === 'finished') {
      return campaign.status === 'finished'
    } else if (activeTab.value === 'closed') {
      return campaign.status === 'closed'
    }
    return false
  })
})

// Functions
function setActiveTab(tabId) {
  activeTab.value = tabId
}

function createNewCampaign() {
  showCreateForm.value = true
  editingCampaign.value = null
  resetForm()
}

function resetForm() {
  formData.value = {
    name: '',
    description: '',
    endDate: '',
    goal: '',
    schoolLogo: null,
    schoolLogoPreview: ''
  }
  generatedBadge.value = null
  selectedTheme.value = 'cute'
}

function cancelEdit() {
  showCreateForm.value = false
  showBadgeGenerator.value = false
  editingCampaign.value = null
  resetForm()
}

function handleSchoolLogoUpload(event) {
  const file = event.target.files[0]
  if (file) {
    formData.value.schoolLogo = file
    
    // Create preview URL
    const reader = new FileReader()
    reader.onload = (e) => {
      formData.value.schoolLogoPreview = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

function proceedToBadgeGeneration() {
  if (!isFormValid.value) return
  showCreateForm.value = false
  showBadgeGenerator.value = true
}

function selectTheme(themeId) {
  selectedTheme.value = themeId
  generatedBadge.value = null // Reset generated badge when theme changes
}

function generateBadge() {
  if (!formData.value.schoolLogoPreview) return
  
  isGeneratingBadge.value = true
  
  // Simulate badge generation with a delay
  setTimeout(() => {
    const theme = badgeThemes.find(t => t.id === selectedTheme.value)
    
    // Create a simple badge representation (in a real app, this would be more sophisticated)
    generatedBadge.value = {
      theme: selectedTheme.value,
      schoolLogo: formData.value.schoolLogoPreview,
      colors: theme.colors,
      timestamp: Date.now()
    }
    
    isGeneratingBadge.value = false
  }, 2000)
}

function saveBadgeAndCreateCampaign() {
  if (!generatedBadge.value) return
  
  const randomImage = stockPhotos[Math.floor(Math.random() * stockPhotos.length)]
  const currentDate = new Date().toISOString().split('T')[0]
  
  const newCampaign = {
    id: Date.now(),
    name: formData.value.name,
    description: formData.value.description,
    schoolName: `${formData.value.name} School`, // Could be extracted or separate field
    image: randomImage,
    startDate: currentDate,
    endDate: formData.value.endDate,
    goal: Number(formData.value.goal),
    raised: 0,
    supporters: 0,
    status: 'open',
    schoolLogo: formData.value.schoolLogoPreview,
    badgeImage: generatedBadge.value, // In real app, this would be saved image URL
    urgency: 'medium',
    newsletterSent: false
  }
  
  campaigns.value.push(newCampaign)
  cancelEdit()
}

function deleteCampaign(campaignId) {
  if (confirm('Are you sure you want to delete this campaign?')) {
    campaigns.value = campaigns.value.filter(c => c.id !== campaignId)
  }
}

function markAsFinished(campaign) {
  campaign.status = 'finished'
}

function sendNewsletter(campaign) {
  // Simulate sending newsletter
  setTimeout(() => {
    campaign.status = 'closed'
    campaign.newsletterSent = true
  }, 1000)
}

function formatAmount(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount)
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function getProgressPercentage(raised, goal) {
  return Math.min((raised / goal) * 100, 100)
}

function getStatusBadgeClass(status) {
  switch(status) {
    case 'open': return 'urgent-low'
    case 'finished': return 'urgent-medium'
    case 'closed': return 'urgent-high'
    default: return 'urgent-medium'
  }
}

function isDatePassed(dateString) {
  return new Date(dateString) < new Date()
}
</script>

<template>
  <!-- HEADER -->
  <header class="hero-gradient hero-pattern">
    <div class="container py-20 md:py-28">
      <div class="max-w-4xl mx-auto text-center animate-slide-up">
        <span class="trust-badge mb-6 inline-block">Campaign Management</span>
        <h1 class="hero-title text-white text-shadow">
          Manage Your <span class="text-gradient">Hong Kong Campaigns</span>
        </h1>
        <p class="hero-lead mt-4 text-white opacity-95">
          Create and manage campaigns for schools and communities across Hong Kong.
        </p>
        
        <div class="mt-8">
          <button 
            @click="createNewCampaign"
            class="btn-donate"
            :class="{ 'opacity-50': showCreateForm || showBadgeGenerator }"
            :disabled="showCreateForm || showBadgeGenerator"
          >
            + Create New Campaign
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- CREATE FORM -->
  <section v-if="showCreateForm" class="section-light">
    <div class="container py-16">
      <div class="max-w-3xl mx-auto">
        <div class="card p-8">
          <!-- Form Header -->
          <div class="mb-8 text-center">
            <h2 class="text-slate-900 mb-2">Create New Campaign</h2>
            <div class="trust-badge urgent-low">Step 1: Campaign Details</div>
          </div>

          <!-- Campaign Form -->
          <form @submit.prevent="proceedToBadgeGeneration" class="space-y-6">
            <!-- Campaign Name -->
            <div>
              <label class="form-label">Campaign Name *</label>
              <input
                v-model="formData.name"
                type="text"
                class="form-input w-full"
                placeholder="e.g., Emergency Relief Fund"
                required
              />
            </div>

            <!-- Description -->
            <div>
              <label class="form-label">Description *</label>
              <textarea
                v-model="formData.description"
                class="form-input w-full"
                rows="4"
                placeholder="Describe your campaign goals and the community it will help..."
                required
              ></textarea>
            </div>

            <!-- Goal Amount and End Date -->
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label class="form-label">Goal Amount (HKD) *</label>
                <input
                  v-model="formData.goal"
                  type="number"
                  min="1"
                  class="form-input w-full"
                  placeholder="25000"
                  required
                />
              </div>
              <div>
                <label class="form-label">End Date *</label>
                <input
                  v-model="formData.endDate"
                  type="date"
                  class="form-input w-full"
                  :min="new Date().toISOString().split('T')[0]"
                  required
                />
              </div>
            </div>

            <!-- School Logo Upload -->
            <div>
              <label class="form-label">School Logo *</label>
              <div class="file-upload-zone">
                <input
                  type="file"
                  accept="image/*"
                  @change="handleSchoolLogoUpload"
                  class="file-input"
                  id="schoolLogo"
                  required
                  style="position: absolute; opacity: 0; width: 0; height: 0;"
                />
                <label for="schoolLogo" class="file-upload-content">
                  <div v-if="!formData.schoolLogoPreview" class="upload-placeholder">
                    <svg class="file-upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                    </svg>
                    <p class="file-upload-text">Click to upload school logo</p>
                    <p class="file-upload-hint">PNG, JPG up to 5MB</p>
                  </div>
                  <div v-else class="logo-preview">
                    <img :src="formData.schoolLogoPreview" alt="School logo preview" style="width: 80px; height: 80px; object-fit: cover; border-radius: 12px; border: 3px solid #22c55e; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2); margin-bottom: 0.75rem;" />
                    <p class="logo-uploaded" style="color: #22c55e; font-weight: 600; font-size: 0.9rem;">Logo uploaded ✓</p>
                  </div>
                </label>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="flex gap-4 justify-center mt-8">
              <button
                type="submit"
                class="btn-donate"
                :class="{ 'opacity-50': !isFormValid }"
                :disabled="!isFormValid"
              >
                Next: Generate Badge
              </button>
              <button
                type="button"
                @click="cancelEdit"
                class="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>

  <!-- BADGE GENERATOR -->
  <section v-if="showBadgeGenerator" class="section-white">
    <div class="container py-16">
      <div class="max-w-4xl mx-auto">
        <div class="card p-8">
          <!-- Badge Generator Header -->
          <div class="mb-8 text-center">
            <h2 class="text-slate-900 mb-2">Generate Campaign Badge</h2>
            <div class="trust-badge urgent-medium">Step 2: Badge Generation</div>
          </div>

          <div class="grid md:grid-cols-2 gap-8">
            <!-- Badge Preview -->
            <div class="text-center">
              <h3 class="text-lg font-weight-700 text-slate-900 mb-4">Badge Preview</h3>
              <div class="badge-preview-container" style="background: linear-gradient(145deg, #f1f5f9, #f8fafc); border: 2px solid #e2e8f0; border-radius: 20px; padding: 2rem; min-height: 300px; display: flex; align-items: center; justify-content: center;">
                <div v-if="!generatedBadge && !isGeneratingBadge" class="badge-placeholder" style="text-align: center; color: #64748b;">
                  <svg style="width: 80px; height: 80px; margin: 0 auto 1rem; color: #cbd5e1;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
                  </svg>
                  <p>Select a theme and click generate</p>
                </div>
                
                <div v-else-if="isGeneratingBadge" class="badge-generating" style="text-align: center; color: #8b5cf6;">
                  <div class="spinner" style="width: 60px; height: 60px; margin: 0 auto 1rem; border: 4px solid #e2e8f0; border-top: 4px solid #8b5cf6; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                  <p>Generating your badge...</p>
                </div>

                <div v-else class="generated-badge" :style="{ background: `linear-gradient(135deg, ${generatedBadge.colors[0]}, ${generatedBadge.colors[1]})`, width: '200px', height: '200px', borderRadius: '20px', padding: '1.5rem', color: 'white', boxShadow: '0 12px 36px rgba(0, 0, 0, 0.15)', border: '3px solid rgba(255, 255, 255, 0.3)', position: 'relative', overflow: 'hidden' }">
                  <div class="badge-content" style="position: relative; z-index: 2; display: flex; flexDirection: 'column'; alignItems: 'center'; justifyContent: 'center'; height: '100%'; textAlign: 'center';">
                    <img :src="generatedBadge.schoolLogo" alt="School logo" style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%; border: 3px solid rgba(255, 255, 255, 0.8); margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);" />
                    <div class="badge-text">
                      <h4 style="font-size: 0.9rem; font-weight: 700; margin-bottom: 0.25rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);">{{ formData.name }}</h4>
                      <p style="font-size: 0.75rem; font-weight: 500; opacity: 0.9; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);">{{ selectedTheme }} Theme</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Theme Selection -->
            <div>
              <h3 class="text-lg font-weight-700 text-slate-900 mb-4">Select Theme</h3>
              <div class="grid grid-cols-2 gap-3">
                <button
                  v-for="theme in badgeThemes"
                  :key="theme.id"
                  @click="selectTheme(theme.id)"
                  type="button"
                  class="theme-option"
                  :class="{ 'selected': selectedTheme === theme.id }"
                  :style="{ background: `linear-gradient(135deg, ${theme.colors[0]}, ${theme.colors[1]})` }"
                >
                  <span class="theme-label">{{ theme.label }}</span>
                </button>
              </div>

              <div class="mt-6 space-y-4">
                <button
                  @click="generateBadge"
                  type="button"
                  class="btn-donate w-full"
                  :disabled="!formData.schoolLogoPreview || isGeneratingBadge"
                  :class="{ 'opacity-50': !formData.schoolLogoPreview || isGeneratingBadge }"
                >
                  {{ isGeneratingBadge ? 'Generating...' : 'Generate Badge' }}
                </button>

                <button
                  v-if="generatedBadge"
                  @click="saveBadgeAndCreateCampaign"
                  type="button"
                  class="action-btn secondary w-full"
                >
                  Save Badge & Create Campaign
                </button>

                <button
                  @click="cancelEdit"
                  type="button"
                  class="action-btn danger w-full"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- TABS NAVIGATION -->
  <section v-if="!showCreateForm && !showBadgeGenerator" class="section-light">
    <div class="container py-8">
      <div class="tab-navigation">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="setActiveTab(tab.id)"
          class="tab-item"
          :class="{ 'active': activeTab === tab.id }"
        >
          {{ tab.label }}
          <span class="tab-badge">{{ tab.count.value }}</span>
        </button>
      </div>
    </div>
  </section>

  <!-- CAMPAIGNS LIST -->
  <section v-if="!showCreateForm && !showBadgeGenerator" class="section-white">
    <div class="container py-20">
      <div class="text-center mb-12">
        <h2 class="text-slate-900 mb-2">{{ tabs.find(t => t.id === activeTab)?.label }}</h2>
        <p class="text-slate-600 mb-4">Manage campaigns for Hong Kong schools and communities</p>
      </div>

      <div class="campaigns-grid-enhanced">
        <article
          v-for="campaign in filteredCampaigns"
          :key="campaign.id"
          class="story-card campaign-card animate-slide-up"
        >
          <!-- Campaign Image -->
          <div class="campaign-image-wrapper">
            <img
              :src="campaign.image"
              :alt="campaign.name"
              class="w-full h-44 object-cover"
            />
            <div class="campaign-badges">
              <span class="trust-badge" :class="getStatusBadgeClass(campaign.status)">
                {{ campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1) }}
              </span>
              <div class="school-logo-badge">
                <img :src="campaign.schoolLogo" alt="School logo" class="badge-preview-image" />
              </div>
            </div>
          </div>

          <!-- Campaign Content -->
          <div class="p-6">
            <div class="mb-4">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-1">{{ campaign.name }}</h3>
              <p class="text-sm text-slate-500 mb-2">{{ campaign.schoolName }}</p>
              <p class="text-slate-600">{{ campaign.description }}</p>
            </div>

            <!-- Campaign Stats -->
            <div class="card p-4 mb-4">
              <div class="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div class="text-lg font-weight-700 text-slate-900">{{ formatAmount(campaign.raised) }}</div>
                  <div class="text-sm text-slate-600">Raised</div>
                </div>
                <div>
                  <div class="text-lg font-weight-700 text-slate-900">{{ formatAmount(campaign.goal) }}</div>
                  <div class="text-sm text-slate-600">Goal</div>
                </div>
              </div>
              
              <div class="progress-bar-large mt-3 mb-2">
                <div 
                  class="progress-fill-large"
                  :style="{ width: getProgressPercentage(campaign.raised, campaign.goal) + '%' }"
                ></div>
              </div>
              
              <div class="text-center text-sm text-slate-600">
                {{ campaign.supporters }} supporters • {{ Math.round(getProgressPercentage(campaign.raised, campaign.goal)) }}% funded
              </div>
            </div>

            <!-- Campaign Dates -->
            <div class="impact-highlight mb-4">
              <div class="flex justify-between text-sm">
                <span><strong>Started:</strong> {{ formatDate(campaign.startDate) }}</span>
                <span><strong>Ends:</strong> {{ formatDate(campaign.endDate) }}</span>
              </div>
            </div>

            <!-- Action Buttons based on status -->
            <div class="campaign-actions">
              <div v-if="campaign.status === 'open'" class="grid grid-cols-2 gap-3">
                <button 
                  @click="markAsFinished(campaign)"
                  class="campaign-action-btn secondary"
                  v-if="isDatePassed(campaign.endDate)"
                >
                  Mark Finished
                </button>
                <button 
                  @click="deleteCampaign(campaign.id)"
                  class="campaign-action-btn danger"
                >
                  Delete
                </button>
              </div>

              <div v-else-if="campaign.status === 'finished'" class="grid grid-cols-2 gap-3">
                <button 
                  @click="sendNewsletter(campaign)"
                  class="campaign-action-btn primary"
                >
                  Send Newsletter
                </button>
                <button 
                  @click="deleteCampaign(campaign.id)"
                  class="campaign-action-btn danger"
                >
                  Delete
                </button>
              </div>

              <div v-else-if="campaign.status === 'closed'" class="text-center">
                <div class="trust-badge urgent-low mb-3">Newsletter Sent ✓</div>
                <button 
                  @click="deleteCampaign(campaign.id)"
                  class="campaign-action-btn danger"
                >
                  Delete Campaign
                </button>
              </div>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-if="filteredCampaigns.length === 0" class="text-center py-16">
        <div class="trust-badge urgent-medium mb-4 inline-block">No {{ activeTab }} Campaigns</div>
        <h3 class="text-xl font-weight-700 text-slate-900 mb-2">
          {{ activeTab === 'open' ? 'Start Your First Campaign' : `No ${activeTab} campaigns yet` }}
        </h3>
        <p class="text-slate-600 mb-6">
          {{ activeTab === 'open' ? 'Create your first campaign to begin raising funds for Hong Kong schools.' : `Check back later for ${activeTab} campaigns.` }}
        </p>
        <button v-if="activeTab === 'open'" @click="createNewCampaign" class="btn-donate">
          Create Your First Campaign
        </button>
      </div>
    </div>
  </section>

  <!-- STATISTICS SUMMARY -->
  <section v-if="!showCreateForm && !showBadgeGenerator" class="section-gradient">
    <div class="container py-16">
      <div class="text-center">
        <h2 class="text-slate-900">Hong Kong Campaign Statistics</h2>
        <p class="mt-2 text-slate-600">Impact across all school communities</p>
        
        <div class="grid md:grid-cols-4 gap-6 mt-10">
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.length }}</div>
            <p>Total Campaigns</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.filter(c => c.status === 'open').length }}</div>
            <p>Active Campaigns</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ formatAmount(campaigns.reduce((sum, c) => sum + c.raised, 0)).replace('$', 'HK$') }}</div>
            <p>Total Raised</p>
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
}

.form-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.form-input::placeholder {
  color: #94a3b8;
}

/* School logo upload styling */
.file-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

/* Badge generator styling */
.badge-preview-container {
  background: linear-gradient(145deg, #f1f5f9, #f8fafc);
  border: 2px solid #e2e8f0;
  border-radius: 20px;
  padding: 2rem;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-placeholder {
  text-align: center;
  color: #64748b;
}

.badge-generating {
  text-align: center;
  color: #8b5cf6;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.generated-badge {
  width: 200px;
  height: 200px;
  border-radius: 20px;
  padding: 1.5rem;
  color: white;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.15);
  border: 3px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.generated-badge::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(180deg); }
}

.badge-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

/* Theme selection */
.theme-option {
  position: relative;
  padding: 1rem;
  border: 3px solid transparent;
  border-radius: 16px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.theme-option:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.theme-option.selected {
  border-color: white;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2), 0 0 0 3px rgba(139, 92, 246, 0.3);
}

.theme-label {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  font-size: 0.9rem;
}

/* Campaign tabs */
.tab-navigation {
  display: flex;
  justify-content: center;
  gap: 0;
  background: white;
  border-radius: 16px;
  padding: 0.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #e2e8f0;
}

.tab-item {
  flex: 1;
  background: transparent;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.tab-item:hover {
  background: linear-gradient(145deg, #f8fafc, #f1f5f9);
  color: #475569;
  transform: translateY(-1px);
}

.tab-item.active {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
  transform: translateY(-2px);
}

.tab-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
}

.tab-item.active .tab-badge {
  background: rgba(255, 255, 255, 0.25);
}

/* Enhanced campaign actions */
.campaign-actions {
  margin-top: auto;
}

/* School logo badge in campaign cards */
.school-logo-badge {
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-preview-image {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  object-fit: cover;
  border: 2px solid #22c55e;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
  transition: transform 0.3s ease;
}

.badge-preview-image:hover {
  transform: scale(1.05);
}

/* Campaign action buttons - enhanced from main.css */
.campaign-action-btn {
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
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
}

.campaign-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.campaign-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Primary button (main action) */
.campaign-action-btn.primary {
  background: linear-gradient(135deg, #ec4899, #be185d);
  border-color: #ec4899;
  color: white;
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
}

.campaign-action-btn.primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #f97316, #ea580c);
  box-shadow: 0 6px 16px rgba(236, 72, 153, 0.4);
}

/* Secondary button */
.campaign-action-btn.secondary {
  border-color: #8b5cf6;
  color: #8b5cf6;
  background: linear-gradient(145deg, #faf5ff, #fff);
}

.campaign-action-btn.secondary:hover {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

/* Danger button */
.campaign-action-btn.danger {
  border-color: #dc2626;
  color: #dc2626;
  background: linear-gradient(145deg, #fef2f2, #fff);
}

.campaign-action-btn.danger:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  color: white;
  box-shadow: 0 4px 16px rgba(220, 38, 38, 0.3);
}

/* Spacing utilities */
.space-y-4 > * + * {
  margin-top: 1rem;
}

.space-y-6 > * + * {
  margin-top: 1.5rem;
}

/* Enhanced button variants */
.btn-secondary {
  border-color: #e2e8f0 !important;
  color: #64748b !important;
  background: white !important;
}

.btn-secondary:hover {
  border-color: #cbd5e1 !important;
  color: #475569 !important;
  background: #f8fafc !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .form-input {
    font-size: 0.9rem;
    padding: 0.75rem 0.875rem;
  }
  
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .flex {
    flex-direction: column;
  }
  
  .flex-1 {
    flex: none;
  }
  
  .tab-navigation {
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem;
  }
  
  .tab-item {
    padding: 0.875rem 1rem;
  }
  
  .theme-option {
    min-height: 50px;
    font-size: 0.85rem;
  }
  
  .generated-badge {
    width: 160px;
    height: 160px;
    padding: 1rem;
  }
  
  .campaign-action-btn {
    font-size: 0.85rem;
    padding: 0.625rem 0.875rem;
  }
}

/* Enhanced accessibility */
.campaign-action-btn:focus,
.tab-item:focus,
.theme-option:focus,
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

/* Enhanced loading states */
@media (prefers-reduced-motion: reduce) {
  .generated-badge::before {
    animation: none;
  }
  
  .story-card.campaign-card {
    animation: none;
  }
}
</style>