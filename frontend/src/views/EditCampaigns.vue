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
    supporters: 127,
    status: "active"
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
    supporters: 289,
    status: "active"
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
    supporters: 64,
    status: "draft"
  }
])

// Form state
const showCreateForm = ref(false)
const editingCampaign = ref(null)
const formData = ref({
  title: '',
  description: '',
  startDate: '',
  endDate: '',
  goal: '',
  urgency: 'medium',
  image: '',
  badgeImage: ''
})

// Form validation
const isFormValid = computed(() => {
  return formData.value.title.trim() && 
         formData.value.description.trim() && 
         formData.value.startDate && 
         formData.value.endDate && 
         formData.value.goal > 0
})

// Functions
function createNewCampaign() {
  showCreateForm.value = true
  editingCampaign.value = null
  resetForm()
}

function editCampaign(campaign) {
  showCreateForm.value = false
  editingCampaign.value = campaign
  formData.value = {
    title: campaign.title,
    description: campaign.description,
    startDate: campaign.startDate,
    endDate: campaign.endDate,
    goal: campaign.goal,
    urgency: campaign.urgency,
    image: campaign.image,
    badgeImage: campaign.badgeImage
  }
}

function resetForm() {
  formData.value = {
    title: '',
    description: '',
    startDate: '',
    endDate: '',
    goal: '',
    urgency: 'medium',
    image: '',
    badgeImage: ''
  }
}

function cancelEdit() {
  showCreateForm.value = false
  editingCampaign.value = null
  resetForm()
}

function saveCampaign() {
  if (!isFormValid.value) return
  
  if (showCreateForm.value) {
    // Create new campaign
    const newCampaign = {
      id: Date.now(),
      ...formData.value,
      goal: Number(formData.value.goal),
      raised: 0,
      supporters: 0,
      status: 'draft'
    }
    campaigns.value.push(newCampaign)
  } else if (editingCampaign.value) {
    // Update existing campaign
    const index = campaigns.value.findIndex(c => c.id === editingCampaign.value.id)
    if (index !== -1) {
      campaigns.value[index] = {
        ...campaigns.value[index],
        ...formData.value,
        goal: Number(formData.value.goal)
      }
    }
  }
  
  cancelEdit()
}

function deleteCampaign(campaignId) {
  if (confirm('Are you sure you want to delete this campaign?')) {
    campaigns.value = campaigns.value.filter(c => c.id !== campaignId)
  }
}

function toggleCampaignStatus(campaign) {
  campaign.status = campaign.status === 'active' ? 'draft' : 'active'
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
  return status === 'active' ? 'urgent-low' : 'urgent-medium'
}
</script>

<template>
  <!-- HEADER -->
  <header class="hero-gradient hero-pattern">
    <div class="container py-20 md:py-28">
      <div class="max-w-4xl mx-auto text-center animate-slide-up">
        <span class="trust-badge mb-6 inline-block">Campaign Management</span>
        <h1 class="hero-title text-white text-shadow">
          Manage Your <span class="text-gradient">Campaigns</span>
        </h1>
        <p class="hero-lead mt-4 text-white opacity-95">
          Create new campaigns and edit existing ones to maximize your impact and reach more supporters.
        </p>
        
        <div class="mt-8">
          <button 
            @click="createNewCampaign"
            class="btn-donate"
            :class="{ 'opacity-50': showCreateForm }"
            :disabled="showCreateForm"
          >
            + Create New Campaign
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- CREATE/EDIT FORM -->
  <section v-if="showCreateForm" class="section-light">
    <div class="container py-16">
      <div class="max-w-4xl mx-auto">
        <div class="card p-8">
          <!-- Form Header -->
          <div class="mb-8 text-center">
            <h2 class="text-slate-900 mb-2">Create New Campaign</h2>
            <div class="trust-badge urgent-low">New Campaign</div>
          </div>

          <!-- Campaign Form -->
          <form @submit.prevent="saveCampaign" class="grid md:grid-cols-2 gap-6">
            <!-- Left Column -->
            <div class="space-y-6">
              <!-- Title -->
              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Campaign Title *</label>
                <input
                  v-model="formData.title"
                  type="text"
                  class="form-input w-full"
                  placeholder="Enter campaign title..."
                  required
                />
              </div>

              <!-- Description -->
              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Description *</label>
                <textarea
                  v-model="formData.description"
                  class="form-input w-full"
                  rows="4"
                  placeholder="Describe your campaign goals and impact..."
                  required
                ></textarea>
              </div>

              <!-- Dates -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Start Date *</label>
                  <input
                    v-model="formData.startDate"
                    type="date"
                    class="form-input w-full"
                    required
                  />
                </div>
                <div>
                  <label class="text-sm font-weight-600 text-slate-900 mb-2 block">End Date *</label>
                  <input
                    v-model="formData.endDate"
                    type="date"
                    class="form-input w-full"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Goal Amount -->
              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Goal Amount ($) *</label>
                <input
                  v-model="formData.goal"
                  type="number"
                  min="1"
                  class="form-input w-full"
                  placeholder="25000"
                  required
                />
              </div>

              <!-- Urgency -->
              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Priority Level</label>
                <select v-model="formData.urgency" class="form-input w-full">
                  <option value="low">Ongoing</option>
                  <option value="medium">Active</option>
                  <option value="high">Urgent</option>
                </select>
              </div>

              <!-- Images -->
              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Campaign Image URL</label>
                <input
                  v-model="formData.image"
                  type="url"
                  class="form-input w-full"
                  placeholder="https://example.com/image.jpg"
                />
              </div>

              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Badge Image URL</label>
                <input
                  v-model="formData.badgeImage"
                  type="url"
                  class="form-input w-full"
                  placeholder="https://example.com/badge.jpg"
                />
              </div>
            </div>

            <!-- Form Actions -->
            <div class="md:col-span-2 flex gap-4 justify-center mt-8">
              <button
                type="submit"
                class="btn-donate"
                :class="{ 'opacity-50': !isFormValid }"
                :disabled="!isFormValid"
              >
                Create Campaign
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

  <!-- EDIT MODAL -->
  <div v-if="editingCampaign" class="modal-overlay" @click="cancelEdit">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="text-xl font-weight-700 text-slate-900">Edit Campaign</h2>
        <div class="trust-badge urgent-medium">Editing Mode</div>
        <button @click="cancelEdit" class="modal-close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <form @submit.prevent="saveCampaign" class="modal-body">
        <div class="grid md:grid-cols-2 gap-6">
          <!-- Left Column -->
          <div class="space-y-4">
            <div>
              <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Campaign Title *</label>
              <input
                v-model="formData.title"
                type="text"
                class="form-input w-full"
                required
              />
            </div>

            <div>
              <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Description *</label>
              <textarea
                v-model="formData.description"
                class="form-input w-full"
                rows="3"
                required
              ></textarea>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Start Date *</label>
                <input
                  v-model="formData.startDate"
                  type="date"
                  class="form-input w-full"
                  required
                />
              </div>
              <div>
                <label class="text-sm font-weight-600 text-slate-900 mb-2 block">End Date *</label>
                <input
                  v-model="formData.endDate"
                  type="date"
                  class="form-input w-full"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="space-y-4">
            <div>
              <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Goal Amount ($) *</label>
              <input
                v-model="formData.goal"
                type="number"
                min="1"
                class="form-input w-full"
                required
              />
            </div>

            <div>
              <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Priority Level</label>
              <select v-model="formData.urgency" class="form-input w-full">
                <option value="low">Ongoing</option>
                <option value="medium">Active</option>
                <option value="high">Urgent</option>
              </select>
            </div>

            <div>
              <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Campaign Image URL</label>
              <input
                v-model="formData.image"
                type="url"
                class="form-input w-full"
              />
            </div>

            <div>
              <label class="text-sm font-weight-600 text-slate-900 mb-2 block">Badge Image URL</label>
              <input
                v-model="formData.badgeImage"
                type="url"
                class="form-input w-full"
              />
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button
            type="submit"
            class="btn-donate"
            :class="{ 'opacity-50': !isFormValid }"
            :disabled="!isFormValid"
          >
            Save Changes
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

  <!-- CAMPAIGNS LIST -->
  <section class="section-white">
    <div class="container py-16">
      <div class="text-center mb-10">
        <h2 class="text-slate-900 mb-2">Your Campaigns</h2>
        <p class="text-slate-600">Manage and monitor your existing campaigns</p>
      </div>

      <div class="grid md:grid-cols-2 gap-8">
        <article
          v-for="campaign in campaigns"
          :key="campaign.id"
          class="story-card campaign-card animate-slide-up"
          :class="{ 'editing-highlight': editingCampaign?.id === campaign.id }"
        >
          <!-- Campaign Image -->
          <div class="campaign-image-wrapper">
            <img
              :src="campaign.image"
              :alt="campaign.title"
              class="w-full h-44 object-cover"
            />
            <div class="campaign-badges">
              <span class="trust-badge" :class="getStatusBadgeClass(campaign.status)">
                {{ campaign.status === 'active' ? 'Live' : 'Draft' }}
              </span>
              <div class="days-remaining-badge">
                ID: {{ campaign.id }}
              </div>
            </div>
          </div>

          <!-- Campaign Content -->
          <div class="p-6">
            <div class="mb-4">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-2">{{ campaign.title }}</h3>
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
                <span><strong>Start:</strong> {{ formatDate(campaign.startDate) }}</span>
                <span><strong>End:</strong> {{ formatDate(campaign.endDate) }}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="grid grid-cols-3 gap-3">
              <button 
                @click="editCampaign(campaign)"
                class="campaign-action-btn primary"
                :class="{ 'opacity-50': editingCampaign?.id === campaign.id }"
                :disabled="editingCampaign?.id === campaign.id"
              >
                {{ editingCampaign?.id === campaign.id ? 'Editing...' : 'Edit' }}
              </button>
              <button 
                @click="toggleCampaignStatus(campaign)"
                class="campaign-action-btn secondary"
                :class="campaign.status === 'active' ? 'active' : ''"
              >
                {{ campaign.status === 'active' ? 'Pause' : 'Activate' }}
              </button>
              <button 
                @click="deleteCampaign(campaign.id)"
                class="campaign-action-btn danger"
              >
                Delete
              </button>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-if="campaigns.length === 0" class="text-center py-16">
        <div class="trust-badge urgent-medium mb-4 inline-block">No Campaigns Yet</div>
        <h3 class="text-xl font-weight-700 text-slate-900 mb-2">Start Your First Campaign</h3>
        <p class="text-slate-600 mb-6">Create your first campaign to begin raising funds for your cause.</p>
        <button @click="createNewCampaign" class="btn-donate">
          Create Your First Campaign
        </button>
      </div>
    </div>
  </section>

  <!-- STATISTICS SUMMARY -->
  <section class="section-gradient">
    <div class="container py-16">
      <div class="text-center">
        <h2 class="text-slate-900">Campaign Statistics</h2>
        <p class="mt-2 text-slate-600">Overview of all your campaigns</p>
        
        <div class="grid md:grid-cols-4 gap-6 mt-10">
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.length }}</div>
            <p>Total Campaigns</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ campaigns.filter(c => c.status === 'active').length }}</div>
            <p>Active Campaigns</p>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ formatAmount(campaigns.reduce((sum, c) => sum + c.raised, 0)).replace('$', '') }}</div>
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
/* Modal styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background: white;
  border-radius: 24px;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.25), 0 10px 40px rgba(0, 0, 0, 0.15);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.modal-header {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.modal-close {
  background: rgba(100, 116, 139, 0.1);
  border: none;
  border-radius: 12px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.modal-close:hover {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
  transform: scale(1.05);
}

.modal-body {
  padding: 2rem;
  max-height: calc(90vh - 200px);
  overflow-y: auto;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(30px) scale(0.95); 
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1); 
  }
}

/* Campaign action buttons - uniform styling */
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

/* Primary button (Edit) */
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

/* Secondary button (Activate/Pause) */
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

.campaign-action-btn.secondary.active {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

/* Danger button (Delete) */
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

/* Form styling using main.css patterns */
.form-input {
  background: white;
  border: 2px solid #e2e8f0;
  color: #1e293b;
  font-weight: 500;
  padding: 0.75rem 1rem;
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

/* Editing highlight for active card */
.editing-highlight {
  border: 3px solid #8b5cf6 !important;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1) !important;
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

/* Spacing utilities */
.space-y-6 > * + * {
  margin-top: 1.5rem;
}

/* Status-specific styling */
.status-active {
  background: linear-gradient(145deg, #f0fdf4, #fff);
  border-left: 4px solid #22c55e;
}

.status-draft {
  background: linear-gradient(145deg, #fff7ed, #fff);
  border-left: 4px solid #ea580c;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .form-input {
    font-size: 0.9rem;
    padding: 0.625rem 0.875rem;
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
  
  .modal-content {
    margin: 0.5rem;
    max-height: 95vh;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }
  
  .modal-body {
    max-height: calc(95vh - 160px);
  }
}
</style>