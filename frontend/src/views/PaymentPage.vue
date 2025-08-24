<script>
import { ref, computed, onMounted } from "vue";
import { loadStripe } from "@stripe/stripe-js";
import axios from "axios";

export default {
  data() {
    return {
      publishableKey:
        "pk_test_51Rz3MGHFWfzbh85tTZOD9DWZxquKZ1afy4HRYpd6tJStNRqI013Y551VHX9BV6HW4oBjAUJgugD7oKvK3YLM1vpO00mn3W5fir",
      stripe: null,
      elements: null,
      cardElement: null,
      amount: 50,
      cardError: "",
      isLoading: false,
      paymentSuccess: false,
      paymentError: "",
      campaigns: [
        {
          id: 1,
          title: "Emergency School Meals",
          description:
            "Provide nutritious meals to children affected by recent floods",
          image:
            "https://images.unsplash.com/photo-1498721406610-899c1d4eb77d?q=80&w=400",
        },
        {
          id: 2,
          title: "Digital Learning Kits",
          description:
            "Tablets and educational apps for children in remote areas",
          image:
            "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=400",
        },
        {
          id: 3,
          title: "Safe Play Spaces",
          description:
            "Building secure playgrounds in underserved neighborhoods",
          image:
            "https://images.unsplash.com/photo-1544717297-fa95b6ee9643?q=80&w=400",
        },
      ],
      // Payment type selection
      paymentType: "one-time", // 'one-time' or 'subscription'

      // One-time donation amounts
      selectedAmount: 50,
      predefinedAmounts: [25, 50, 100, 250],
      customAmount: "",
      useCustomAmount: false,

      // Donor information
      donorInfo: {
        name: "",
        email: "",
      },

      // Form validation
      errors: {},

      // Payment processing states
      isLoading: false,
      paymentSuccess: false,
      paymentError: "",

      // Campaign selection (automatically set to first campaign)
      selectedCampaign: 0, // Always use the first campaign

      // Stripe
      stripe: null,
      elements: null,
      cardElement: null,
    };
  },
  computed: {
    finalAmount() {
      return this.useCustomAmount
        ? parseFloat(this.customAmount) || 0
        : this.selectedAmount;
    },

    isFormValid() {
      return (
        this.donorInfo.name &&
        this.donorInfo.email &&
        this.finalAmount > 0 &&
        !this.isLoading
      );
    },
  },
  async mounted() {
    console.log("PaymentPage mounted, initializing Stripe...");
    console.log("Available campaigns:", this.campaigns);

    try {
      console.log("Loading Stripe...");
      // Load Stripe with your publishable key
      this.stripe = await loadStripe(this.publishableKey);

      this.elements = this.stripe.elements();

      // Setup card element
      setTimeout(() => {
        this.setupCardElement();
      }, 100);
    } catch (error) {
      console.error("Error loading Stripe:", error);
    }
  },
  methods: {
    async setupCardElement() {
      console.log("Setting up card element...");

      await this.$nextTick();

      const cardElementContainer = document.getElementById("card-element");
      if (!cardElementContainer) {
        console.error("Card element container not found!");
        return;
      }

      if (!this.stripe || !this.elements) {
        console.error("Stripe not initialized");
        return;
      }

      // Clear any existing content
      cardElementContainer.innerHTML = "";

      // Create card element
      this.cardElement = this.elements.create("card", {
        style: {
          base: {
            color: "#32325d",
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
              color: "#aab7c4",
            },
          },
          invalid: {
            color: "#fa755a",
            iconColor: "#fa755a",
          },
        },
        hidePostalCode: true,
      });

      try {
        this.cardElement.mount("#card-element");
        console.log("✅ Card element mounted successfully");

        // Handle card changes
        this.cardElement.on("change", (event) => {
          if (event.error) {
            this.cardError = event.error.message;
          } else {
            this.cardError = "";
          }
        });
      } catch (error) {
        console.error("Error mounting card element:", error);
        this.cardError = "Failed to initialize payment form";
      }
    },

    selectAmount(amount) {
      this.selectedAmount = amount;
      this.useCustomAmount = false;
      this.customAmount = "";
    },

    selectCustomAmount() {
      this.useCustomAmount = true;
    },

    validateForm() {
      this.errors = {};

      if (!this.donorInfo.name) this.errors.name = "Name is required";
      if (!this.donorInfo.email) this.errors.email = "Email is required";

      return Object.keys(this.errors).length === 0;
    },

    async processPayment() {
      if (!this.validateForm()) return;

      // Reset previous states
      this.paymentError = "";
      this.paymentSuccess = false;
      this.isLoading = true;

      try {
        const { token, error } = await this.stripe.createToken(
          this.cardElement,
          {
            name: this.donorInfo.name,
            email: this.donorInfo.email,
          }
        );

        if (error) {
          console.error("Error creating token:", error);
          this.cardError = error.message;
          return;
        }

        console.log("✅ Stripe Token created:", token);

        // Prepare payment data for backend
        const paymentData = {
          campaign_id: this.selectedCampaign,
          email: this.donorInfo.email,
          amount: this.finalAmount,
          charge: {
            amount: Math.round(this.finalAmount * 100),
            currency: "sgd",
            description: `Donation for ${this.campaigns[this.selectedCampaign]?.title || 'Campaign'}`,
            source: token.id
          }
        };

        console.log("Sending payment data:", paymentData);

        // Send to makedonation service
        const BASE_URL = 'http://127.0.0.1:8086/makedonation';
        
        const response = await axios.post(`${BASE_URL}/donate`, paymentData);
        
        console.log("Payment response:", response.data);
        
        if (response.data && response.data.success) {
          // Payment successful
          this.paymentSuccess = true;
        } else {
          throw new Error(response.data?.error || "Payment failed");
        }

        setTimeout(() => {
          this.resetForm();
          this.paymentSuccess = false;
        }, 3000); // Reset after 3 seconds

      } catch (error) {
        console.error("Payment error:", error);
        this.paymentError =
          error.response?.data?.error || "Payment failed. Please try again.";
      } finally {
        this.isLoading = false;
      }
    },

    async processOneTimePayment() {
      const paymentData = {
        amount: this.finalAmount,
        email: this.donorInfo.email,
        name: this.donorInfo.name,
        campaign_id: this.selectedCampaign || null,
      };

      // For demo purposes, we'll simulate a successful payment
      console.log("Processing one-time payment:", paymentData);

      // Simulated delay
      await new Promise((resolve) => setTimeout(resolve, 2000));

      console.log("✅ Payment processed successfully!");
    },

    resetForm() {
      this.donorInfo = {
        name: "",
        email: "",
      };
      this.selectedAmount = 50;
      this.customAmount = "";
      this.useCustomAmount = false;
      this.errors = {};

      // Reset payment states
      this.isLoading = false;
      this.paymentSuccess = false;
      this.paymentError = "";

      // Clear the Stripe card element
      if (this.cardElement) {
        this.cardElement.clear();
      }
    },

    formatAmount(amount) {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "SGD",
        minimumFractionDigits: 0,
      }).format(amount);
    },
  },
};
</script>

<template>
  <!-- HERO SECTION -->
  <header class="hero-gradient hero-pattern">
    <div class="container py-20 md:py-28">
      <div class="max-w-4xl mx-auto text-center animate-slide-up">
        <span class="trust-badge mb-6 inline-block"
          >🔒 Secure Payment Gateway</span
        >
        <h1 class="hero-title text-white text-shadow">
          Complete Your <span class="text-gradient">Donation</span>
        </h1>
        <p class="hero-lead mt-4 text-white opacity-95">
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
      <div class="max-w-6xl mx-auto">
        <div class="grid lg:grid-cols-3 gap-8">
          <!-- MAIN PAYMENT FORM -->
          <div class="lg:col-span-2 space-y-8">
            <!-- AMOUNT SELECTION -->
            <section class="card p-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">
                Select Amount
              </h3>

              <!-- One-time amounts -->
              <div v-if="paymentType === 'one-time'" class="space-y-6">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <button
                    v-for="amount in predefinedAmounts"
                    :key="amount"
                    class="amount-btn"
                    :class="{
                      selected: selectedAmount === amount && !useCustomAmount,
                    }"
                  >
                    {{ formatAmount(amount) }}
                    <div class="progress-mini mt-2">
                      <div
                        class="progress-fill-mini"
                        :style="{
                          width: Math.min(amount / 250, 1) * 100 + '%',
                        }"
                      ></div>
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
                  <span class="text-slate-600">SGD</span>
                </div>

                <div class="impact-highlight">
                  <strong>{{ formatAmount(finalAmount) }}</strong> can provide
                  <strong
                    >{{ Math.round(finalAmount / 2.5) }} learning hours</strong
                  >
                  for children in need.
                </div>
              </div>
            </section>

            <!-- CAMPAIGN DETAILS -->
            <section class="card p-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">
                Campaign Details
              </h3>

              <div
                v-if="campaigns.length > 0"
                class="flex gap-6 p-4 border-2 border-slate-200 rounded-lg bg-slate-50"
              >
                <!-- Campaign Image -->
                <div class="flex-shrink-0">
                  <img
                    :src="campaigns[0].image"
                    :alt="campaigns[0].title"
                    class="w-24 h-24 object-cover rounded-lg"
                  />
                </div>

                <!-- Campaign Info -->
                <div class="flex-1">
                  <h4 class="font-weight-700 text-slate-900 text-lg mb-2">
                    {{ campaigns[0].title }}
                  </h4>
                  <p class="text-slate-600 text-sm leading-relaxed">
                    {{ campaigns[0].description }}
                  </p>
                  <div class="mt-3">
                    <span
                      class="inline-block bg-purple-100 text-purple-700 text-xs px-3 py-1 rounded-full"
                    >
                      Your donation will support this campaign
                    </span>
                  </div>
                </div>
              </div>

              <!-- Fallback if no campaigns -->
              <div v-else class="text-center p-8 text-slate-600">
                <p>Loading campaign details...</p>
              </div>
            </section>

            <!-- DONOR INFORMATION & PAYMENT METHOD -->
            <section class="card p-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">
                Your Information & Payment
              </h3>

              <div class="grid md:grid-cols-2 gap-8">
                <!-- Left Side: Donor Information -->
                <div>
                  <h4 class="text-lg font-weight-600 text-slate-900 mb-4">
                    Personal Details
                  </h4>

                  <div class="space-y-6">
                    <div>
                      <label
                        class="block text-sm font-weight-600 text-slate-900 mb-2"
                        >Full Name *</label
                      >
                      <input
                        v-model="donorInfo.name"
                        type="text"
                        class="form-input w-full"
                        :class="{ 'border-red-500': errors.name }"
                        placeholder="John Doe"
                      />
                      <p v-if="errors.name" class="text-red-500 text-sm mt-1">
                        {{ errors.name }}
                      </p>
                    </div>

                    <div>
                      <label
                        class="block text-sm font-weight-600 text-slate-900 mb-2"
                        >Email Address *</label
                      >
                      <input
                        v-model="donorInfo.email"
                        type="email"
                        class="form-input w-full"
                        :class="{ 'border-red-500': errors.email }"
                        placeholder="john@example.com"
                      />
                      <p v-if="errors.email" class="text-red-500 text-sm mt-1">
                        {{ errors.email }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Right Side: Payment Method -->
                <div>
                  <h4 class="text-lg font-weight-600 text-slate-900 mb-4">
                    Payment Method
                  </h4>

                  <div class="space-y-6">
                    <!-- Card form with Stripe Elements -->
                    <div>
                      <label
                        class="block text-sm font-weight-600 text-slate-900 mb-2"
                        >Card Information *</label
                      >
                      <!-- Stripe Elements will be mounted here -->
                      <div class="form-group">
                        <label>Card Information</label>
                        <div id="card-element" class="card-element"></div>
                        <div v-if="cardError" class="error">
                          {{ cardError }}
                        </div>
                      </div>
                      <!-- Display form errors -->
                      <div
                        id="card-errors"
                        class="text-red-500 text-sm mt-1"
                        role="alert"
                      ></div>

                      <!-- Debug info (remove in production) -->
                      <div class="text-xs text-slate-400 mt-1">
                        Card element container ready for Stripe mounting
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- PAYMENT SUMMARY SIDEBAR -->
          <div class="lg:col-span-1">
            <div class="card p-8 sticky top-8">
              <h3 class="text-xl font-weight-700 text-slate-900 mb-6">
                Payment Summary
              </h3>

              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-slate-600">Type:</span>
                  <span class="font-weight-600 text-slate-900">
                    {{
                      paymentType === "subscription"
                        ? "Monthly Subscription"
                        : "One-time Donation"
                    }}
                  </span>
                </div>

                <div
                  v-if="paymentType === 'subscription'"
                  class="flex justify-between items-center"
                >
                  <span class="text-slate-600">Plan:</span>
                  <span class="font-weight-600 text-slate-900">
                    {{
                      subscriptionPlans.find((p) => p.id === selectedPlan)?.name
                    }}
                  </span>
                </div>

                <hr class="border-slate-200" />

                <div class="flex justify-between items-center">
                  <span class="text-lg font-weight-600 text-slate-900"
                    >Total:</span
                  >
                  <span class="text-2xl font-weight-800 text-slate-900">
                    {{ formatAmount(finalAmount) }}
                    <span
                      v-if="paymentType === 'subscription'"
                      class="text-sm font-weight-500 text-slate-600"
                      >/month</span
                    >
                  </span>
                </div>

                <div class="impact-highlight">
                  <div class="text-center">
                    <div class="font-weight-600 text-slate-900 mb-2">
                      Your Impact
                    </div>
                    <div class="text-sm text-slate-600">
                      {{
                        paymentType === "subscription" ? "Monthly" : "One-time"
                      }}
                      support of
                      <strong
                        >{{ Math.round(finalAmount / 2.5) }} learning
                        hours</strong
                      >
                    </div>
                  </div>
                </div>

                <!-- Error Message -->
                <div
                  v-if="paymentError"
                  class="card p-6 mb-4"
                  style="border-left: 4px solid #dc2626"
                >
                  <div class="flex items-center gap-4">
                    <div class="trust-badge urgent-high">❌ Failed</div>
                    <div>
                      <h4 class="font-weight-700 text-slate-900 mb-1">
                        Payment Failed
                      </h4>
                      <p class="text-slate-600 text-sm">{{ paymentError }}</p>
                    </div>
                  </div>
                </div>

                <!-- Success Message -->
                <div v-if="paymentSuccess" class="impact-highlight mb-4">
                  <div class="flex items-center gap-4">
                    <div class="trust-badge urgent-low">✅ Success</div>
                    <div>
                      <div class="font-weight-700 text-slate-900 mb-1">
                        Payment Successful!
                      </div>
                      <div class="text-slate-600 text-sm">
                        {{
                          paymentType === "subscription"
                            ? "Subscription"
                            : "Donation"
                        }}
                        of <strong>{{ formatAmount(finalAmount) }}</strong> has
                        been processed successfully.
                      </div>
                    </div>
                  </div>
                </div>

                <button
                  @click="processPayment"
                  class="btn-donate w-full"
                  :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }"
                  :disabled="!isFormValid"
                >
                  <span
                    v-if="isLoading"
                    class="flex items-center justify-center"
                  >
                    <svg
                      class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        class="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        stroke-width="4"
                      ></circle>
                      <path
                        class="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    Processing...
                  </span>
                  <span v-else>
                    {{
                      paymentType === "subscription"
                        ? "Start Subscription"
                        : "Complete Donation"
                    }}
                  </span>
                </button>

                <div class="text-center">
                  <div class="trust-badge mb-3">🔒 Secure Payment</div>
                  <p class="text-xs text-slate-600 leading-relaxed">
                    Your payment is processed securely by Stripe. We never store
                    your card details.
                    {{
                      paymentType === "subscription"
                        ? "You can cancel your subscription anytime."
                        : ""
                    }}
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
            <p class="text-sm text-slate-600">
              Bank-level security for all transactions
            </p>
          </div>

          <div class="card p-6 text-center">
            <div class="text-3xl mb-4">💳</div>
            <h3 class="font-weight-600 text-slate-900 mb-2">Stripe Powered</h3>
            <p class="text-sm text-slate-600">Trusted by millions worldwide</p>
          </div>

          <div class="card p-6 text-center">
            <div class="text-3xl mb-4">📧</div>
            <h3 class="font-weight-600 text-slate-900 mb-2">Instant Receipt</h3>
            <p class="text-sm text-slate-600">
              Immediate confirmation and tax receipt
            </p>
          </div>

          <div class="card p-6 text-center">
            <div class="text-3xl mb-4">🛡️</div>
            <h3 class="font-weight-600 text-slate-900 mb-2">
              Privacy Protected
            </h3>
            <p class="text-sm text-slate-600">
              Your data is never shared or sold
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Form input styling already defined in main.css, just adding validation state */
.form-input.border-red-500 {
  border-color: #ef4444;
}

/* Urgency color variants for trust-badge (matching ViewCampaigns.vue) */
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

/* Sticky sidebar */
.sticky {
  position: sticky;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .sticky {
    position: static;
  }
}
</style>
