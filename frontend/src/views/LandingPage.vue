<template>
  <div class="min-h-screen">
    <!-- Hero Section with Enhanced Urgency -->
    <section class="hero-gradient hero-pattern min-h-screen flex items-center relative overflow-hidden">
      <div class="container mx-auto px-4 text-center text-white relative z-10">
        <!-- Urgency Banner -->
        <div class="urgency-banner mb-8 animate-slide-up">
          ⚡ URGENT: Only {{ daysLeft }} days left to reach our emergency goal!
        </div>
        
        <div class="floating">
          <h1 class="text-5xl md:text-7xl font-bold mb-6 animate-slide-up text-shadow">
            <span class="block mb-2">One Click Away From</span>
            <span class="text-gradient bg-clip-text text-transparent bg-gradient-to-r from-yellow-300 to-pink-300">
              Changing Everything
            </span>
          </h1>
        </div>
        
        <p class="text-xl md:text-2xl mb-8 animate-slide-up text-shadow max-w-3xl mx-auto">
          Right now, <strong class="text-yellow-300 pulse-text">{{ waitingChildren }} children</strong> are waiting for someone like YOU to believe in their dreams. 
          <span class="block mt-2 text-lg opacity-90">Your $50 could be the moment their entire life changes forever.</span>
        </p>
        
        <!-- Real-time impact ticker -->
        <div class="impact-ticker mb-8 animate-slide-up">
          🎉 <strong>Sarah just got art supplies</strong> thanks to someone like you! 
          <span class="text-yellow-300">{{ Math.floor(Math.random() * 30) + 5 }} minutes ago</span>
        </div>
        
        <div class="flex flex-col md:flex-row gap-4 justify-center items-center animate-slide-up">
          <button class="btn-donate text-lg pulsing-button" @click="scrollToSection('donate')">
            💝 YES! Transform a Life - ${{ selectedAmount }}
          </button>
          <button class="btn-ghost" @click="scrollToSection('stories')">
            💕 See the Magic First
          </button>
        </div>
        
        <!-- Live stats counter -->
        <div class="live-stats mt-12 animate-slide-up">
          <div class="stats-container">
            <div class="stat-item">
              <div class="stat-value">{{ liveStats.helped }}</div>
              <div class="stat-label">Helped This Month</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">${{ liveStats.raised.toLocaleString() }}</div>
              <div class="stat-label">Raised This Week</div>
            </div>
          </div>
        </div>
        
        <!-- Enhanced floating hearts -->
        <div class="absolute top-20 left-10 text-pink-300 text-4xl floating heart-beat">💖</div>
        <div class="absolute top-40 right-20 text-yellow-300 text-3xl floating-delayed">⭐</div>
        <div class="absolute bottom-32 left-20 text-blue-300 text-3xl floating">🌟</div>
        <div class="absolute bottom-20 right-10 text-purple-300 text-4xl floating-delayed heart-beat">💜</div>
        <div class="absolute top-1/2 left-1/4 text-green-300 text-2xl floating">🎨</div>
        <div class="absolute top-1/3 right-1/4 text-orange-300 text-2xl floating-delayed">📚</div>
      </div>
      
      <!-- Background decorative elements -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full opacity-20 floating"></div>
        <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full opacity-20 floating-delayed"></div>
      </div>
    </section>

    <!-- Enhanced Impact Stats Section -->
    <section class="py-16 px-4 bg-white/50 backdrop-blur-sm">
      <div class="container mx-auto">
        <h2 class="text-4xl font-bold text-center mb-6 text-gradient">The Incredible Impact We're Making Together</h2>
        <p class="text-center text-lg text-gray-600 mb-12 max-w-2xl mx-auto">
          Every single donation creates ripples of hope. <strong>You're about to become part of something extraordinary.</strong>
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div class="stat-card animate-slide-up hover-lift">
            <div class="stat-number">{{ animatedStats.children }}</div>
            <p class="text-purple-600 font-semibold">Lives Transformed</p>
            <div class="progress-mini">
              <div class="progress-fill-mini" :style="`width: ${(animatedStats.children / 1500) * 100}%`"></div>
            </div>
            <p class="text-xs text-gray-500 mt-2">+{{ Math.floor(Math.random() * 5) + 1 }} today! 🎉</p>
          </div>
          
          <div class="stat-card animate-slide-up hover-lift" style="animation-delay: 0.2s;">
            <div class="stat-number">${{ (animatedStats.funds / 1000).toFixed(1) }}M</div>
            <p class="text-blue-600 font-semibold">Dreams Funded</p>
            <div class="progress-mini">
              <div class="progress-fill-mini" :style="`width: ${(animatedStats.funds / 3000000) * 100}%`"></div>
            </div>
            <p class="text-xs text-gray-500 mt-2">Goal: $3M 💪</p>
          </div>
          
          <div class="stat-card animate-slide-up hover-lift" style="animation-delay: 0.4s;">
            <div class="stat-number">{{ animatedStats.successRate }}%</div>
            <p class="text-green-600 font-semibold">Success Rate</p>
            <div class="progress-mini">
              <div class="progress-fill-mini" :style="`width: ${animatedStats.successRate}%`"></div>
            </div>
            <p class="text-xs text-gray-500 mt-2">Above average! ⭐</p>
          </div>
          
          <div class="stat-card animate-slide-up hover-lift" style="animation-delay: 0.6s;">
            <div class="stat-number">{{ animatedStats.programs }}+</div>
            <p class="text-orange-600 font-semibold">Life-Changing Programs</p>
            <div class="progress-mini">
              <div class="progress-fill-mini" :style="`width: ${(animatedStats.programs / 100) * 100}%`"></div>
            </div>
            <p class="text-xs text-gray-500 mt-2">New art program! 🎨</p>
          </div>
        </div>

        <!-- Monthly Goal Progress -->
        <div class="goal-progress mt-16 animate-slide-up">
          <div class="card p-8">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-2xl font-bold text-gray-800">December Emergency Goal</h3>
              <span class="text-xl font-bold text-green-600">${{ goalProgress.current.toLocaleString() }} / ${{ goalProgress.target.toLocaleString() }}</span>
            </div>
            <div class="progress-bar-large">
              <div class="progress-fill-large" :style="`width: ${(goalProgress.current / goalProgress.target) * 100}%`"></div>
            </div>
            <div class="flex justify-between text-sm text-gray-600 mt-2">
              <span>{{ Math.round((goalProgress.current / goalProgress.target) * 100) }}% Complete</span>
              <span>${{ (goalProgress.target - goalProgress.current).toLocaleString() }} still needed</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Enhanced Donation Section -->
    <section id="donate" class="py-20 px-4 bg-gradient-to-br from-purple-50 to-pink-50">
      <div class="container mx-auto max-w-4xl">
        <div class="text-center mb-12">
          <h2 class="text-5xl font-bold mb-6 text-gradient">Your Moment to Create Magic ✨</h2>
          <p class="text-xl text-gray-600 mb-8">
            Choose the amount that feels right in your heart. Every dollar is a seed of hope that grows into a transformed life.
            <strong class="block mt-2 text-green-600">💚 100% goes directly to the children - zero admin fees!</strong>
          </p>
        </div>
        
        <div class="card p-8 mb-8 donation-card">
          <!-- Social Proof -->
          <div class="social-proof mb-6">
            <div class="flex items-center justify-center gap-2 text-sm text-gray-600">
              <div class="flex -space-x-2">
                <div class="w-8 h-8 rounded-full bg-gradient-to-r from-pink-400 to-purple-400"></div>
                <div class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-green-400"></div>
                <div class="w-8 h-8 rounded-full bg-gradient-to-r from-yellow-400 to-orange-400"></div>
              </div>
              <span><strong>{{ recentDonors }}</strong> people donated in the last 24 hours</span>
            </div>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <button 
              v-for="amount in donationAmounts" 
              :key="amount.value"
              class="amount-btn"
              :class="{ 'selected': selectedAmount === amount.value }"
              @click="selectAmount(amount.value)"
            >
              <div class="text-2xl font-bold">${{ amount.value }}</div>
              <div class="text-sm mt-1">{{ amount.impact }}</div>
            </button>
          </div>
          
          <div class="mb-6">
            <label class="form-label">💝 Or enter your heart's amount:</label>
            <input 
              type="number" 
              class="form-input" 
              placeholder="Enter custom amount" 
              v-model="customAmount"
              @input="updateSelectedAmount"
            />
          </div>
          
          <!-- What their donation does TODAY -->
          <div class="impact-preview mb-6 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl">
            <h4 class="text-lg font-bold text-gray-800 mb-2">Your ${{ actualDonationAmount }} will provide RIGHT NOW:</h4>
            <div class="text-green-700 font-semibold">{{ getDonationImpact(actualDonationAmount) }}</div>
          </div>
          
          <div class="text-center">
            <button class="btn-donate w-full md:w-auto text-xl py-4 px-12 mega-donate-btn" @click="handleDonate">
              💖 YES! Transform {{ getChildrenHelped(actualDonationAmount) }} Life Today - ${{ actualDonationAmount }}
            </button>
            <p class="text-sm text-gray-500 mt-3">🔒 Secure payment • 💯 Money-back guarantee • 📧 Instant receipt</p>
          </div>
        </div>
        
        <!-- What specific donations accomplish -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="card-child p-6 text-center hover-lift">
            <div class="text-4xl mb-4">📚</div>
            <h3 class="text-xl font-bold mb-2 text-purple-700">$25 Creates</h3>
            <p class="text-gray-600">A month of learning joy with complete school supplies</p>
            <div class="mt-3 text-sm text-green-600 font-semibold">✓ {{ Math.floor(Math.random() * 20) + 10 }} kids helped this month</div>
          </div>
          
          <div class="card-child p-6 text-center hover-lift selected-impact">
            <div class="text-4xl mb-4">🍎</div>
            <h3 class="text-xl font-bold mb-2 text-blue-700">$50 Provides</h3>
            <p class="text-gray-600">Nutritious meals for an entire week + vitamins</p>
            <div class="mt-3 text-sm text-green-600 font-semibold">✓ Most popular choice!</div>
          </div>
          
          <div class="card-child p-6 text-center hover-lift">
            <div class="text-4xl mb-4">🎨</div>
            <h3 class="text-xl font-bold mb-2 text-pink-700">$100 Unlocks</h3>
            <p class="text-gray-600">Creative therapy sessions that heal trauma</p>
            <div class="mt-3 text-sm text-green-600 font-semibold">✓ {{ Math.floor(Math.random() * 15) + 5 }} kids in therapy now</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Enhanced Success Stories with Emotional Impact -->
    <section id="stories" class="py-20 px-4 bg-white">
      <div class="container mx-auto">
        <h2 class="text-4xl font-bold text-center mb-6 text-gradient">Real Children, Real Dreams, Real Impact</h2>
        <p class="text-center text-lg text-gray-600 mb-12 max-w-2xl mx-auto">
          These aren't just stories - they're proof that your donation creates miracles. 
          <strong>Every child here started exactly where our current kids are today.</strong>
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <div class="story-card enhanced-story">
            <img src="https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80" 
                 alt="Happy child" 
                 class="w-full h-48 object-cover rounded-t-3xl" />
            <div class="p-6">
              <div class="story-impact mb-3">
                <span class="impact-badge">$75 donation impact</span>
              </div>
              <h3 class="text-2xl font-bold mb-3 text-purple-700">Sarah's Miracle Journey</h3>
              <p class="text-gray-600 mb-4">
                "I was sleeping on the streets when REACH found me. Someone donated $75 - enough for school supplies and meals for 2 weeks. 
                That person saved my life. Now I'm studying to become a teacher to help kids just like me!"
              </p>
              <div class="story-footer">
                <div class="text-sm text-orange-600 font-semibold">Age 16 • Now in University 🎓</div>
                <div class="text-xs text-gray-500 mt-1">Helped 2 years ago • Thriving today</div>
              </div>
            </div>
          </div>
          
          <div class="story-card enhanced-story">
            <img src="https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80" 
                 alt="Child learning" 
                 class="w-full h-48 object-cover rounded-t-3xl" />
            <div class="p-6">
              <div class="story-impact mb-3">
                <span class="impact-badge">$50 donation impact</span>
              </div>
              <h3 class="text-2xl font-bold mb-3 text-blue-700">Marcus's Transformation</h3>
              <p class="text-gray-600 mb-4">
                "I thought nobody cared about me. Then someone I'll never meet donated $50 for my meals. That act of love changed everything. 
                I learned my dreams DO matter and that there are people who believe in me."
              </p>
              <div class="story-footer">
                <div class="text-sm text-green-600 font-semibold">Age 14 • Art Program Graduate 🎨</div>
                <div class="text-xs text-gray-500 mt-1">From shy to confident in 6 months</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Testimonial from donor -->
        <div class="donor-testimonial mt-16 animate-slide-up">
          <div class="card p-8 max-w-3xl mx-auto text-center">
            <div class="text-3xl mb-4">💕</div>
            <blockquote class="text-xl italic text-gray-700 mb-4">
              "I donated $50 six months ago and just got a letter from the little girl my donation helped. She drew me a picture and said I'm her hero. 
              I've never felt more fulfilled in my entire life. This is the best $50 I've ever spent."
            </blockquote>
            <div class="text-gray-600 font-semibold">- Jennifer M., Monthly Donor</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Enhanced Call to Action with Urgency -->
    <section class="cta-section py-20 px-4 relative">
      <div class="container mx-auto text-center text-white relative z-10">
        <div class="urgency-final mb-6">
          ⏰ Don't let this moment pass - {{ waitingChildren }} children are counting on YOU right now
        </div>
        <h2 class="text-5xl font-bold mb-6">This Is Your Moment to Be Someone's Hero</h2>
        <p class="text-xl mb-8 max-w-3xl mx-auto">
          Years from now, a grown-up child will tell their own children about the stranger who believed in them when no one else would. 
          <strong class="text-yellow-300">That stranger could be you. That moment could be right now.</strong>
        </p>
        
        <div class="final-cta mb-8">
          <div class="countdown-urgency mb-4">
            Only {{ hoursLeft }} hours left to reach our emergency goal!
          </div>
        </div>
        
        <div class="flex flex-col md:flex-row gap-4 justify-center items-center">
          <button class="btn-donate text-xl final-donate-btn" @click="scrollToSection('donate')">
            🌟 YES! I'll Be Their Hero - ${{ selectedAmount }}
          </button>
          <button class="btn-ghost" @click="scrollToSection('stories')">
            💝 See More Transformations
          </button>
        </div>
        
        <!-- Final social proof -->
        <div class="final-social-proof mt-8">
          <p class="text-lg">Join {{ totalDonors.toLocaleString() }} amazing people who've already said YES to hope!</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Enhanced reactive data
const selectedAmount = ref(50)
const customAmount = ref('')
const waitingChildren = ref(147)
const daysLeft = ref(3)
const hoursLeft = ref(72)
const recentDonors = ref(234)
const totalDonors = ref(12847)

// Live stats that update
const liveStats = ref({
  helped: 1247,
  raised: 89750
})

// Animated stats
const animatedStats = ref({
  children: 0,
  funds: 0,
  successRate: 0,
  programs: 0
})

// Goal progress
const goalProgress = ref({
  current: 247890,
  target: 300000
})

// Donation amounts with impact descriptions
const donationAmounts = ref([
  { value: 25, impact: "School supplies" },
  { value: 50, impact: "Week of meals" },
  { value: 100, impact: "Art therapy" },
  { value: 250, impact: "Full support" }
])

// Computed property for the actual donation amount
const actualDonationAmount = computed(() => {
  return customAmount.value || selectedAmount.value
})

// Animate stats on mount
onMounted(() => {
  animateStats()
  startLiveUpdates()
})

const animateStats = () => {
  const targets = { children: 1250, funds: 2700000, successRate: 85, programs: 50 }
  
  Object.keys(targets).forEach(key => {
    let start = 0
    const end = targets[key]
    const duration = 2000
    const stepTime = 50
    const steps = duration / stepTime
    const increment = end / steps
    
    const timer = setInterval(() => {
      start += increment
      if (start >= end) {
        animatedStats.value[key] = end
        clearInterval(timer)
      } else {
        animatedStats.value[key] = Math.floor(start)
      }
    }, stepTime)
  })
}

const startLiveUpdates = () => {
  // Simulate live updates every 30 seconds
  setInterval(() => {
    liveStats.value.helped += Math.floor(Math.random() * 3) + 1
    liveStats.value.raised += Math.floor(Math.random() * 500) + 100
    recentDonors.value += Math.floor(Math.random() * 2)
  }, 30000)
}

// Function to select preset amounts
const selectAmount = (amount) => {
  selectedAmount.value = amount
  customAmount.value = ''
}

const updateSelectedAmount = () => {
  if (customAmount.value) {
    selectedAmount.value = Number(customAmount.value)
  }
}

const getDonationImpact = (amount) => {
  if (amount >= 250) return "✨ Complete support package for 1 child for a month + emergency fund"
  if (amount >= 100) return "🎨 Full month of art therapy + nutritious snacks + school supplies"
  if (amount >= 50) return "🍎 One week of nutritious meals + vitamin supplements"
  if (amount >= 25) return "📚 Complete school supplies for one month"
  return "💕 Contributes to our emergency fund for urgent needs"
}

const getChildrenHelped = (amount) => {
  if (amount >= 100) return "a"
  return "a"
}

// Handle donation process
const handleDonate = () => {
  console.log('Donation initiated:', actualDonationAmount.value)
  
  // Create more emotional success message
  const childNames = ['Sarah', 'Marcus', 'Elena', 'David', 'Maya', 'Alex']
  const randomChild = childNames[Math.floor(Math.random() * childNames.length)]
  
  alert(`🎉 AMAZING! Your $${actualDonationAmount.value} donation is going to change everything for a child like ${randomChild}! 

💝 You'll receive:
• Instant email receipt
• Photo & update from the child you help
• Monthly impact reports
• Tax-deductible confirmation

This normally redirects to secure payment processing. You're about to become someone's hero! 🌟`)
}

// Smooth scrolling for navigation links
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
/* Enhanced styles building on your existing theme */

.urgency-banner {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 700;
  display: inline-block;
  animation: gentle-pulse 2s ease-in-out infinite;
  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
}

.pulse-text {
  animation: gentle-pulse 1.5s ease-in-out infinite;
}

.pulsing-button {
  animation: gentle-pulse 2s ease-in-out infinite;
  position: relative;
  overflow: hidden;
}

.pulsing-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  animation: shimmer 3s ease-in-out infinite;
}

.mega-donate-btn:hover::before {
  left: 100%;
}

.selected-impact {
  border: 3px solid #10b981;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
  transform: scale(1.05);
}

.enhanced-story {
  position: relative;
  overflow: hidden;
}

.enhanced-story::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #8b5cf6, #3b82f6, #10b981);
}

.story-impact {
  text-align: center;
}

.impact-badge {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.story-footer {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
  margin-top: 1rem;
}

.donor-testimonial {
  opacity: 0;
  animation: slideInUp 0.8s ease-out 1s forwards;
}

.urgency-final {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 1rem 2rem;
  border-radius: 25px;
  font-weight: 700;
  display: inline-block;
  animation: gentle-pulse 1.5s ease-in-out infinite;
  box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
}

.countdown-urgency {
  background: rgba(239, 68, 68, 0.9);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  display: inline-block;
  animation: gentle-pulse 1s ease-in-out infinite;
}

.final-donate-btn {
  background: linear-gradient(135deg, #f59e0b, #d97706) !important;
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.5) !important;
  animation: gentle-pulse 1.5s ease-in-out infinite !important;
  transform: scale(1.1);
}

.final-social-proof {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: inline-block;
}

/* Enhanced animations */
@keyframes gentle-pulse {
  0%, 100% { 
    transform: scale(1);
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);
  }
  50% { 
    transform: scale(1.02);
    box-shadow: 0 12px 40px rgba(16, 185, 129, 0.6);
  }
}

@keyframes shimmer {
  0% { 
    transform: translateX(-100%);
  }
  100% { 
    transform: translateX(200%);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive enhancements */
@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .urgency-banner, .urgency-final {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  
  .final-donate-btn {
    transform: scale(1);
    padding: 1rem 1.5rem !important;
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .floating, 
  .floating-delayed, 
  .heart-beat,
  .animate-slide-up,
  .pulsing-button,
  .gentle-pulse,
  .shimmer,
  .mega-donate-btn,
  .final-donate-btn {
    animation: none !important;
  }
  
  .hover-lift:hover {
    transform: none !important;
  }
}

.impact-ticker {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInUp 0.8s ease-out;
}

.live-stats {
  margin-top: 2rem;
}

.stats-container {
  display: flex;
  justify-content: center;
  gap: 3rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  padding: 1.5rem 2rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #fbbf24;
  font-family: 'Poppins', sans-serif;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-top: 0.25rem;
}

.hover-lift {
  transition: transform 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-8px);
}

.progress-mini {
  width: 100%;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  margin-top: 0.5rem;
  overflow: hidden;
}

.progress-fill-mini {
  height: 100%;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 2px;
  transition: width 1s ease;
}

.goal-progress {
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.8s forwards;
}

.progress-bar-large {
  width: 100%;
  height: 16px;
  background: #f1f5f9;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-fill-large {
  height: 100%;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 12px;
  transition: width 2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.progress-fill-large::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s ease-in-out infinite;
}

.donation-card {
  position: relative;
  overflow: hidden;
}

.donation-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #10b981, #059669, #3b82f6);
  animation: shimmer 3s ease-in-out infinite;
}

.social-proof {
  background: rgba(16, 185, 129, 0.05);
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(16, 185, 129, 0.1);
}

.impact-preview {
  border: 2px solid #10b981;
  position: relative;
  overflow: hidden;
}

.impact-preview::before {
  content: '✨';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1.5rem;
  animation: gentle-float 2s ease-in-out infinite;
}

.mega-donate-btn {
  background: linear-gradient(135deg, #10b981, #059669) !important;
  box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4) !important;
  animation: gentle-pulse 2s ease-in-out infinite !important;
  position: relative;
  overflow: hidden;
}

.mega-donate-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
}
</style>