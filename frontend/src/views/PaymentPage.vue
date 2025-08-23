<script setup>
import { ref, computed } from 'vue'

// Payment type selection
const paymentType = ref('one-time') // 'one-time' or 'subscription'

// One-time donation amounts
const selectedAmount = ref(50)
const predefinedAmounts = [25, 50, 100, 250]
const customAmount = ref('')
const useCustomAmount = ref(false)

// Subscription plans (matching backend plans)
const subscriptionPlans = ref([
  {
    id: 'supporter',
    name: 'Supporter',
    price: 60,
    currency: 'USD',
    interval: 'month',
    features: [
      'Monthly impact reports',
      'Basic badge collection',
      'Leaderboard access',
      'Tax-deductible receipts'
    ],
    color: 'blue'
  },
  {
    id: 'advocate', 
    name: 'Advocate',
    price: 120,
    currency: 'USD',
    interval: 'month',
    features: [
      'Weekly impact reports',
      'Advanced badge collection',
      'Leaderboard access',
      'Exclusive campaign access',
      'Priority support'
    ],
    color: 'purple',
    popular: true
  },
  {
    id: 'champion',
    name: 'Champion', 
    price: 500,
    currency: 'USD',
    interval: 'month',
    features: [
      'Real-time impact tracking',
      'Premium badge collection',
      'VIP leaderboard access',
      'Personal impact reports',
      'Direct contact with teams',
      'Monthly video calls'
    ],
    color: 'gold'
  }
])

const selectedPlan = ref('advocate')

// Donor information
const donorInfo = ref({
  name: '',
  email: '',
  phone: '',
  address: '',
  city: '',
  country: 'Singapore'
})

// Payment method
const paymentMethod = ref('card')
const cardInfo = ref({
  number: '',
  expiry: '',
  cvc: '',
  name: ''
})

// Form validation
const errors = ref({})

// Campaign selection (optional)
const selectedCampaign = ref(null)
const campaigns = ref([
  {
    id: 1,
    title: "Emergency School Meals",
    description: "Provide nutritious meals to children affected by recent floods",
    image: "https://images.unsplash.com/photo-1498721406610-899c1d4eb77d?q=80&w=400"
  },
  {
    id: 2,
    title: "Digital Learning Kits", 
    description: "Tablets and educational apps for children in remote areas",
    image: "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=400"
  },
  {
    id: 3,
    title: "Safe Play Spaces",
    description: "Building secure playgrounds in underserved neighborhoods", 
    image: "https://images.unsplash.com/photo-1544717297-fa95b6ee9643?q=80&w=400"
  }
])

// Computed values
const finalAmount = computed(() => {
  if (paymentType.value === 'subscription') {
    return subscriptionPlans.value.find(p => p.id === selectedPlan.value)?.price || 0
  }
  return useCustomAmount.value ? (parseInt(customAmount.value) || 0) : selectedAmount.value
})

const isFormValid = computed(() => {
  return donorInfo.value.name && 
         donorInfo.value.email && 
         finalAmount.value > 0 &&
         cardInfo.value.number.length >= 16 &&
         cardInfo.value.expiry &&
         cardInfo.value.cvc.length >= 3
})

// Functions
function selectAmount(amount) {
  selectedAmount.value = amount
  useCustomAmount.value = false
  customAmount.value = ''
}

function selectCustomAmount() {
  useCustomAmount.value = true
}

function selectPlan(planId) {
  selectedPlan.value = planId
}

function formatCardNumber(value) {
  return value.replace(/\s/g, '').replace(/(\d{4})/g, '$1 ').trim()
}

function formatExpiry(value) {
  return value.replace(/\D/g, '').replace(/(\d{2})(\d)/, '$1/$2')
}

function validateForm() {
  errors.value = {}
  
  if (!donorInfo.value.name) errors.value.name = 'Name is required'
  if (!donorInfo.value.email) errors.value.email = 'Email is required'
  if (!cardInfo.value.number || cardInfo.value.number.replace(/\s/g, '').length < 16) {
    errors.value.cardNumber = 'Valid card number is required'
  }
  if (!cardInfo.value.expiry) errors.value.expiry = 'Expiry date is required'
  if (!cardInfo.value.cvc || cardInfo.value.cvc.length < 3) {
    errors.value.cvc = 'Valid CVC is required'
  }
  
  return Object.keys(errors.value).length === 0
}

function processPayment() {
  if (!validateForm()) return
  
  // Mock payment processing
  alert(`Payment processed! ${paymentType.value === 'subscription' ? 'Subscription' : 'Donation'} of $${finalAmount.value}`)
  
  // Reset form
  resetForm()
}

function resetForm() {
  donorInfo.value = {
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    country: 'Singapore'
  }
  cardInfo.value = {
    number: '',
    expiry: '',
    cvc: '',
    name: ''
  }
  selectedAmount.value = 50
  customAmount.value = ''
  useCustomAmount.value = false
  selectedCampaign.value = null
  errors.value = {}
}

function formatAmount(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount)
}

// Watch for card number formatting
function onCardNumberInput(event) {
  const formatted = formatCardNumber(event.target.value)
  if (formatted.length <= 19) { // 16 digits + 3 spaces
    cardInfo.value.number = formatted
  }
}

function onExpiryInput(event) {
  const formatted = formatExpiry(event.target.value)
  if (formatted.length <= 5) { // MM/YY
    cardInfo.value.expiry = formatted
  }
}

function onCvcInput(event) {
  const value = event.target.value.replace(/\D/g, '')
  if (value.length <= 4) {
    cardInfo.value.cvc = value
  }
}
</script>

<template>
  <!-- HERO SECTION -->
  <header class="hero-gradient hero-pattern">
    <div class="container py-20 md:py-28">
      <div class="max-w-4xl mx-auto text-center animate-slide-up">
        <span class="trust-badge mb-6 inline-block">🔒 Secure Payment Gateway</span>
        <h1 class="hero-title text-white text-shadow">
          Complete Your <span class="text-gradient">Donation</span>
        </h1>
        <p class="hero-lead mt-4 text-white opacity-95">
          Choose between a one-time donation or monthly subscription to create lasting impact. 
          Your contribution is secure and 100% goes toward helping children.
        </p>
        
        <div class="social-proof mt-8">
          🛡️ SSL Encrypted • 💳 Stripe Secured • 📧 Instant Receipt
        </div>
      </div>
    </div>
  </header>

  <div class="section-light">
    <div class="container py-16">
      <!-- PAYMENT TYPE SELECTION -->
      <section class="mb-12">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-center text-slate-900 mb-8">Choose Your Impact Style</h2>
          
          <div class="grid md:grid-cols-2 gap-6">
            <!-- One-time Donation -->
            <div 
              class="card p-8 cursor-pointer transition-all duration-300"
              :class="{ 'ring-4 ring-purple-300 bg-purple-50': paymentType === 'one-time' }"
              @click="paymentType = 'one-time'"
            >
              <div class="text-center">
                <div class="text-4xl mb-4">💝</div>
                <h3 class="text-xl font-weight-700 text-slate-900 mb-2">One-Time Donation</h3>
                <p class="text-slate-600 mb-4">Make an immediate impact with a single contribution</p>
                
                <div class="trust-badge" :class="paymentType === 'one-time' ? 'urgent-medium' : ''">
                  {{ paymentType === 'one-time' ? 'Selected' : 'Choose This' }}
                </div>
              </div>
            </div>

            <!-- Monthly Subscription -->
            <div 
              class="card p-8 cursor-pointer transition-all duration-300"
              :class="{ 'ring-4 ring-purple-300 bg-purple-50': paymentType === 'subscription' }"
              @click="paymentType = 'subscription'"
            >
              <div class="text-center">
                <div class="text-4xl mb-4">🌟</div>
                <h3 class="text-xl font-weight-700 text-slate-900 mb-2">Monthly Subscription</h3>
                <p class="text-slate-600 mb-4">Become a regular supporter with ongoing impact tracking</p>
                
                <div class="trust-badge" :class="paymentType === 'subscription' ? 'urgent-medium' : ''">
                  {{ paymentType === 'subscription' ? 'Selected' : 'Choose This' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="max-w-6xl mx-auto">
        <div class="grid lg:grid-cols-3 gap-8">
          <!-- MAIN PAYMENT FORM -->
          <div class="lg:col-span-2 space-y-8">
            
            <!-- AMOUNT/PLAN SELECTION -->
            <section class="card p-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">
                {{ paymentType === 'subscription' ? 'Choose Your Plan' : 'Select Amount' }}
              </h3>

              <!-- One-time amounts -->
              <div v-if="paymentType === 'one-time'" class="space-y-6">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <button
                    v-for="amount in predefinedAmounts"
                    :key="amount"
                    @click="selectAmount(amount)"
                    class="amount-btn"
                    :class="{ 'selected': selectedAmount === amount && !useCustomAmount }"
                  >
                    {{ formatAmount(amount) }}
                    <div class="progress-mini mt-2">
                      <div class="progress-fill-mini" :style="{ width: Math.min(amount/250, 1) * 100 + '%' }"></div>
                    </div>
                  </button>
                </div>

                <div class="flex items-center gap-4">
                  <input
                    v-model="customAmount"
                    @focus="selectCustomAmount"
                    type="number"
                    min="1"
                    placeholder="Custom amount"
                    class="form-input flex-1"
                  />
                  <span class="text-slate-600">USD</span>
                </div>

                <div class="impact-highlight">
                  <strong>{{ formatAmount(finalAmount) }}</strong> can provide 
                  <strong>{{ Math.round(finalAmount / 2.5) }} learning hours</strong> for children in need.
                </div>
              </div>

              <!-- Subscription plans -->
              <div v-if="paymentType === 'subscription'" class="space-y-6">
                <div class="grid md:grid-cols-3 gap-6">
                  <div
                    v-for="plan in subscriptionPlans"
                    :key="plan.id"
                    @click="selectPlan(plan.id)"
                    class="card p-6 cursor-pointer transition-all duration-300 relative"
                    :class="{ 
                      'ring-4 ring-purple-300 bg-purple-50': selectedPlan === plan.id,
                      'transform scale-105': plan.popular 
                    }"
                  >
                    <div v-if="plan.popular" class="trust-badge urgent-high absolute -top-3 left-1/2 transform -translate-x-1/2">
                      Most Popular
                    </div>
                    
                    <div class="text-center mb-4">
                      <h4 class="text-lg font-weight-700 text-slate-900">{{ plan.name }}</h4>
                      <div class="text-3xl font-weight-800 text-slate-900 mt-2">
                        {{ formatAmount(plan.price) }}
                        <span class="text-sm text-slate-600 font-weight-500">/month</span>
                      </div>
                    </div>

                    <ul class="space-y-2 text-sm">
                      <li v-for="feature in plan.features" :key="feature" class="flex items-start gap-2">
                        <span class="text-green-500 mt-1">✓</span>
                        <span class="text-slate-600">{{ feature }}</span>
                      </li>
                    </ul>

                    <div class="mt-6 text-center">
                      <div class="trust-badge" :class="selectedPlan === plan.id ? 'urgent-medium' : ''">
                        {{ selectedPlan === plan.id ? 'Selected' : 'Choose Plan' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- CAMPAIGN SELECTION (Optional) -->
            <section class="card p-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-4">
                Support a Specific Campaign (Optional)
              </h3>
              <p class="text-slate-600 mb-6">Choose a campaign to direct your donation, or leave unselected for general support.</p>
              
              <div class="grid md:grid-cols-3 gap-4">
                <div
                  v-for="campaign in campaigns"
                  :key="campaign.id"
                  @click="selectedCampaign = selectedCampaign === campaign.id ? null : campaign.id"
                  class="story-card cursor-pointer transition-all duration-300"
                  :class="{ 'ring-2 ring-purple-400': selectedCampaign === campaign.id }"
                >
                  <img :src="campaign.image" :alt="campaign.title" class="w-full h-32 object-cover" />
                  <div class="p-4">
                    <h4 class="font-weight-600 text-slate-900 text-sm mb-1">{{ campaign.title }}</h4>
                    <p class="text-xs text-slate-600">{{ campaign.description }}</p>
                  </div>
                </div>
              </div>
            </section>

            <!-- DONOR INFORMATION -->
            <section class="card p-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">Your Information</h3>
              
              <div class="grid md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-weight-600 text-slate-900 mb-2">Full Name *</label>
                  <input
                    v-model="donorInfo.name"
                    type="text"
                    class="form-input w-full"
                    :class="{ 'border-red-500': errors.name }"
                    placeholder="John Doe"
                  />
                  <p v-if="errors.name" class="text-red-500 text-sm mt-1">{{ errors.name }}</p>
                </div>

                <div>
                  <label class="block text-sm font-weight-600 text-slate-900 mb-2">Email Address *</label>
                  <input
                    v-model="donorInfo.email"
                    type="email"
                    class="form-input w-full"
                    :class="{ 'border-red-500': errors.email }"
                    placeholder="john@example.com"
                  />
                  <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
                </div>

                <div>
                  <label class="block text-sm font-weight-600 text-slate-900 mb-2">Phone Number</label>
                  <input
                    v-model="donorInfo.phone"
                    type="tel"
                    class="form-input w-full"
                    placeholder="+65 9123 4567"
                  />
                </div>

                <div>
                  <label class="block text-sm font-weight-600 text-slate-900 mb-2">Country</label>
                  <select v-model="donorInfo.country" class="form-input w-full">
                    <option value="Singapore">Singapore</option>
                    <option value="Malaysia">Malaysia</option>
                    <option value="Indonesia">Indonesia</option>
                    <option value="Thailand">Thailand</option>
                    <option value="Philippines">Philippines</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
            </section>

            <!-- PAYMENT METHOD -->
            <section class="card p-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">Payment Method</h3>
              
              <div class="space-y-6">
                <!-- Payment method selector -->
                <div class="grid grid-cols-3 gap-4">
                  <button 
                    @click="paymentMethod = 'card'"
                    class="amount-btn"
                    :class="{ 'selected': paymentMethod === 'card' }"
                  >
                    💳 Card
                  </button>
                  <button 
                    @click="paymentMethod = 'paypal'"
                    class="amount-btn opacity-50 cursor-not-allowed"
                    disabled
                  >
                    🅿️ PayPal
                  </button>
                  <button 
                    @click="paymentMethod = 'bank'"
                    class="amount-btn opacity-50 cursor-not-allowed"
                    disabled
                  >
                    🏦 Bank
                  </button>
                </div>

                <!-- Card form -->
                <div v-if="paymentMethod === 'card'" class="grid md:grid-cols-2 gap-6">
                  <div class="md:col-span-2">
                    <label class="block text-sm font-weight-600 text-slate-900 mb-2">Card Number *</label>
                    <input
                      :value="cardInfo.number"
                      @input="onCardNumberInput"
                      type="text"
                      class="form-input w-full"
                      :class="{ 'border-red-500': errors.cardNumber }"
                      placeholder="1234 5678 9012 3456"
                      maxlength="19"
                    />
                    <p v-if="errors.cardNumber" class="text-red-500 text-sm mt-1">{{ errors.cardNumber }}</p>
                  </div>

                  <div>
                    <label class="block text-sm font-weight-600 text-slate-900 mb-2">Expiry Date *</label>
                    <input
                      :value="cardInfo.expiry"
                      @input="onExpiryInput"
                      type="text"
                      class="form-input w-full"
                      :class="{ 'border-red-500': errors.expiry }"
                      placeholder="MM/YY"
                      maxlength="5"
                    />
                    <p v-if="errors.expiry" class="text-red-500 text-sm mt-1">{{ errors.expiry }}</p>
                  </div>

                  <div>
                    <label class="block text-sm font-weight-600 text-slate-900 mb-2">CVC *</label>
                    <input
                      :value="cardInfo.cvc"
                      @input="onCvcInput"
                      type="text"
                      class="form-input w-full"
                      :class="{ 'border-red-500': errors.cvc }"
                      placeholder="123"
                      maxlength="4"
                    />
                    <p v-if="errors.cvc" class="text-red-500 text-sm mt-1">{{ errors.cvc }}</p>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- PAYMENT SUMMARY SIDEBAR -->
          <div class="lg:col-span-1">
            <div class="card p-8 sticky top-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">Payment Summary</h3>
              
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-slate-600">Type:</span>
                  <span class="font-weight-600 text-slate-900">
                    {{ paymentType === 'subscription' ? 'Monthly Subscription' : 'One-time Donation' }}
                  </span>
                </div>

                <div v-if="paymentType === 'subscription'" class="flex justify-between items-center">
                  <span class="text-slate-600">Plan:</span>
                  <span class="font-weight-600 text-slate-900">
                    {{ subscriptionPlans.find(p => p.id === selectedPlan)?.name }}
                  </span>
                </div>

                <div v-if="selectedCampaign" class="flex justify-between items-center">
                  <span class="text-slate-600">Campaign:</span>
                  <span class="font-weight-600 text-slate-900 text-sm">
                    {{ campaigns.find(c => c.id === selectedCampaign)?.title }}
                  </span>
                </div>

                <hr class="border-slate-200">

                <div class="flex justify-between items-center">
                  <span class="text-lg font-weight-600 text-slate-900">Total:</span>
                  <span class="text-2xl font-weight-800 text-slate-900">
                    {{ formatAmount(finalAmount) }}
                    <span v-if="paymentType === 'subscription'" class="text-sm font-weight-500 text-slate-600">/month</span>
                  </span>
                </div>

                <div class="impact-highlight">
                  <div class="text-center">
                    <div class="font-weight-600 text-slate-900 mb-2">Your Impact</div>
                    <div class="text-sm text-slate-600">
                      {{ paymentType === 'subscription' ? 'Monthly' : 'One-time' }} support of 
                      <strong>{{ Math.round(finalAmount / 2.5) }} learning hours</strong>
                    </div>
                  </div>
                </div>

                <button
                  @click="processPayment"
                  class="btn-donate w-full"
                  :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }"
                  :disabled="!isFormValid"
                >
                  {{ paymentType === 'subscription' ? 'Start Subscription' : 'Complete Donation' }}
                </button>

                <div class="text-center">
                  <div class="trust-badge mb-3">🔒 Secure Payment</div>
                  <p class="text-xs text-slate-600 leading-relaxed">
                    Your payment is processed securely by Stripe. We never store your card details.
                    {{ paymentType === 'subscription' ? 'You can cancel your subscription anytime.' : '' }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TRUST SECTION -->
  <section class="section-white">
    <div class="container py-16">
      <div class="text-center">
        <h2 class="text-slate-900 mb-8">Why Your Payment is Safe</h2>
        
        <div class="grid md:grid-cols-4 gap-6">
          <div class="card p-6 text-center">
            <div class="text-3xl mb-4">🔒</div>
            <h3 class="font-weight-600 text-slate-900 mb-2">SSL Encrypted</h3>
            <p class="text-sm text-slate-600">Bank-level security for all transactions</p>
          </div>
          
          <div class="card p-6 text-center">
            <div class="text-3xl mb-4">💳</div>
            <h3 class="font-weight-600 text-slate-900 mb-2">Stripe Powered</h3>
            <p class="text-sm text-slate-600">Trusted by millions worldwide</p>
          </div>
          
          <div class="card p-6 text-center">
            <div class="text-3xl mb-4">📧</div>
            <h3 class="font-weight-600 text-slate-900 mb-2">Instant Receipt</h3>
            <p class="text-sm text-slate-600">Immediate confirmation and tax receipt</p>
          </div>
          
          <div class="card p-6 text-center">
            <div class="text-3xl mb-4">🛡️</div>
            <h3 class="font-weight-600 text-slate-900 mb-2">Privacy Protected</h3>
            <p class="text-sm text-slate-600">Your data is never shared or sold</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Form input styling to match design system */
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

.form-input.border-red-500 {
  border-color: #ef4444;
}

/* Enhanced card hover effects for payment selection */
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
}

/* Sticky sidebar */
.sticky {
  position: sticky;
}

/* Animation delays for staggered entrance */
.card {
  animation: slideInUp 0.6s ease-out;
}

.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }

/* Responsive adjustments */
@media (max-width: 768px) {
  .form-input {
    font-size: 0.9rem;
    padding: 0.625rem 0.875rem;
  }
  
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .lg\:col-span-2,
  .lg\:col-span-1 {
    grid-column: span 1;
  }
  
  .sticky {
    position: static;
  }
}

/* Payment method specific styling */
.amount-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.amount-btn:disabled:hover {
  transform: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* Enhanced ring styling for selections */
.ring-4 {
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.3);
}

.ring-2 {
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.5);
}
</style>
