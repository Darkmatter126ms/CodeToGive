import axios from 'axios'

// API base configuration
const API_BASE_URL = 'http://localhost:8084'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Payment API service
export const paymentAPI = {
  // Health check
  healthCheck() {
    return api.get('/payment/health')
  },

  // Get subscription plans
  getPlans() {
    return api.get('/payment/plans')
  },

  // Create payment intent for one-time donation
  createPaymentIntent(paymentData) {
    const requestData = {
      amount: paymentData.amount * 100, // Convert to cents
      currency: 'usd',
      email: paymentData.email,
      name: paymentData.name,
      campaign_id: paymentData.campaign_id || null
    }
    return api.post('/payment/create-payment-intent', requestData)
  },

  // Create subscription
  createSubscription(subscriptionData) {
    const requestData = {
      plan_id: subscriptionData.plan_id,
      email: subscriptionData.email,
      name: subscriptionData.name
    }
    return api.post('/payment/create-subscription', requestData)
  },

  // Test endpoint to complete payment (for development)
  testCompletePayment(paymentIntentId) {
    return api.post(`/payment/test-complete-payment/${paymentIntentId}`)
  },

  // Get payment statistics
  getPaymentStats() {
    return api.get('/payment/stats')
  }
}

// Campaign API placeholder (if needed)
export const campaignAPI = {
  // Add campaign-related endpoints here if needed
}

export default api
