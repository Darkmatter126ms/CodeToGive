<script setup>
import { ref } from 'vue'

/* --- Donation quick amounts --- */
const selected = ref(50)
const amounts = [25, 50, 100, 250]
function choose(a){ selected.value = a }
function donate(){
  // Replace with your real checkout or router link
  window.location.href = 'https://example.org/donate?amount=' + selected.value
}
</script>

<template>
<!-- HERO -->
<header
  class="hero-photo tint-dark text-white"
  style="--hero-bg:url('https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=2000')"
>
  <div class="container py-20 md:py-28 flex justify-center">
    <div class="max-w-3xl mx-auto animate-slide-up">
      <span class="trust-badge mb-6 inline-block">Registered Children’s Charity · Since 2012</span>
      <h1 class="hero-title">
        Give every child a <span class="text-gradient">brighter start</span>
      </h1>
      <p class="hero-lead mt-4 max-w-2xl">
        BrightSteps Foundation partners with schools and local groups to deliver meals, learning kits,
        and safe spaces so children can grow with confidence.
      </p>

      <div class="mt-8 flex flex-wrap items-center gap-4">
        <button class="btn-donate" @click="donate">Donate now</button>
        <a href="#about" class="btn-secondary">About BrightSteps</a>
      </div>

      <div class="social-proof mt-8">
        Trusted by 12,000+ donors • Top-rated transparency • Tax-deductible receipts
      </div>
    </div>
  </div>
</header>


  <!-- ABOUT -->
  <section id="about" class="section-white">
    <div class="container py-16">
      <div class="grid md:grid-cols-2 gap-8 items-center">
        <div class="card p-8 animate-slide-left">
          <h2>Who we are</h2>
          <p class="mt-3">
            <strong>BrightSteps Foundation</strong> is a non-profit focused on child wellbeing and education across
            underserved communities in Southeast Asia. We work directly with teachers, caregivers, and community leaders
            to make sure support reaches the kids who need it most.
          </p>
          <p>
            Our approach is simple: listen locally, act transparently, and measure outcomes. Every program is co-designed
            with partners on the ground and tracked for long-term impact.
          </p>
          <div class="impact-highlight">
            “Because of you, I can read my first book.” — Aisha, 8
          </div>
        </div>

        <div class="grid gap-6 animate-slide-right">
          <article class="story-card">
            <img alt="Children learning" class="w-full h-44 object-cover"
                 src="https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1600" />
            <div class="p-6">
              <h3>Learning Kits</h3>
              <p>Backpacks, books, stationery, and after-school tutoring for early grades.</p>
            </div>
          </article>
          <article class="story-card">
            <img alt="Nutritious meals" class="w-full h-44 object-cover"
                 src="https://images.unsplash.com/photo-1498721406610-899c1d4eb77d?q=80&w=1600" />
            <div class="p-6">
              <h3>Daily Nutrition</h3>
              <p>Nutritious meals and micro-gardens run with local kitchens and volunteers.</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- MISSION / VALUES -->
  <section class="section-light">
    <div class="container py-16">
      <h2 class="text-center">Our mission & values</h2>
      <p class="text-center mt-2">Everything we do is anchored in dignity, equity, and evidence.</p>

      <div class="grid md:grid-cols-3 gap-6 mt-10">
        <div class="card p-6">
          <h3>Community-first</h3>
          <p>Programs are co-created with parents, teachers, and local partners for cultural fit.</p>
        </div>
        <div class="card p-6">
          <h3>Transparent</h3>
          <p>Budgets, audits, and outcomes are published in our open annual report.</p>
        </div>
        <div class="card p-6">
          <h3>Data-guided</h3>
          <p>We measure attendance, learning outcomes, and nutrition markers every term.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- IMPACT STATS -->
  <section id="impact" class="section-white">
    <div class="container py-16">
      <h2 class="text-center">Your impact at a glance</h2>
      <p class="text-center mt-2">We focus on transparency and measurable outcomes.</p>

      <div class="grid md:grid-cols-4 gap-6 mt-10">
        <div class="stat-card">
          <div class="stat-number">260k</div>
          <p>Meals served</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">13k</div>
          <p>Children supported</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">340</div>
          <p>Communities reached</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">95%</div>
          <p>Funds to programs</p>
        </div>
      </div>
    </div>
  </section>

  <!-- PROGRAMS -->
  <section class="section-light">
    <div class="container py-16">
      <div class="grid md:grid-cols-3 gap-6">
        <article class="card p-6">
          <h3>Early Readers</h3>
          <p class="mt-2">Literacy clubs, mobile libraries, and mentorship to build a love of reading.</p>
          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 72%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">72% funded</p>
          </div>
        </article>
        <article class="card p-6">
          <h3>Healthy Starts</h3>
          <p class="mt-2">Nutrition kits and school meals to improve focus and attendance.</p>
          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 58%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">58% funded</p>
          </div>
        </article>
        <article class="card p-6">
          <h3>Safe Spaces</h3>
          <p class="mt-2">After-school clubs with sports, art, and mental wellness activities.</p>
          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 41%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">41% funded</p>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- QUICK DONATE -->
  <section id="donate" class="section-white">
    <div class="container py-16">
      <div class="grid md:grid-cols-2 gap-8 items-center">
        <div class="donation-card card p-8 animate-slide-left">
          <h2>Make a gift today</h2>
          <p class="mt-2">100% of your gift supports children directly.</p>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <button
              v-for="a in amounts" :key="a"
              class="amount-btn"
              :class="{'selected': selected===a}"
              @click="choose(a)"
            >
              ${{ a }}
              <div class="progress-mini mt-2">
                <div class="progress-fill-mini" :style="{ width: (Math.min(a/250,1)*100)+'%' }"></div>
              </div>
            </button>
          </div>

          <div class="donation-highlight mt-6">
            <strong>${{ selected }}</strong> can provide <strong>{{ Math.round(selected/2.5) }} learning hours</strong>.
          </div>

          <div class="mt-6 flex gap-4">
            <button class="btn-donate flex-1" @click="donate">Donate ${{ selected }}</button>
            <a class="btn-secondary flex-1" href="/donate">Other amount</a>
          </div>

          <p class="mt-4 text-sm text-slate-600">
            Secure payment • Instant receipt • Tax-deductible
          </p>
        </div>

        <div class="impact-preview p-8 animate-slide-right">
          <h3 class="mb-3">How your donation helps</h3>
          <ul class="list-disc ml-5 space-y-2">
            <li>$25 provides 10 classroom meals</li>
            <li>$50 equips a child with a term’s stationery</li>
            <li>$100 sponsors weekly literacy support</li>
            <li>$250 funds a community reading corner</li>
          </ul>

          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 64%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">Campaign: $64,000 raised of $100,000 goal</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- TESTIMONIALS -->
  <section class="section-white">
    <div class="container py-16">
      <h2 class="text-center">What supporters say</h2>
      <div class="grid md:grid-cols-3 gap-6 mt-10">
        <article class="story-card p-6">
          <p>“Regular updates and clear budgets. I always see where my gift goes.”</p>
          <p class="mt-3 text-slate-600">— Mei Lin, monthly donor</p>
        </article>
        <article class="story-card p-6">
          <p>“Our students show up eager to read. The kits truly changed our classroom.”</p>
          <p class="mt-3 text-slate-600">— Mr. Rahman, teacher</p>
        </article>
        <article class="story-card p-6">
          <p>“Volunteering was seamless and meaningful. The team is warm and organized.”</p>
          <p class="mt-3 text-slate-600">— Daniel, volunteer</p>
        </article>
      </div>
    </div>
  </section>

  <!-- PARTNERS -->
  <section class="section-light">
    <div class="container py-16">
      <h2 class="text-center">Our partners</h2>
      <p class="text-center mt-2">We collaborate with schools, clinics, NGOs, and local councils.</p>
      <div class="grid md:grid-cols-4 gap-6 mt-10">
        <div class="card p-6 text-center">EduReach</div>
        <div class="card p-6 text-center">NutriCare</div>
        <div class="card p-6 text-center">SafePlay</div>
        <div class="card p-6 text-center">Books4All</div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section-white">
    <div class="container py-16">
      <h2 class="text-center">Frequently asked questions</h2>
      <div class="grid md:grid-cols-2 gap-6 mt-10">
        <details class="card p-6">
          <summary><strong>Is my donation tax-deductible?</strong></summary>
          <p class="mt-3">Yes. You’ll receive an instant receipt by email after donating.</p>
        </details>
        <details class="card p-6">
          <summary><strong>How do you report impact?</strong></summary>
          <p class="mt-3">We publish audited financials and termly dashboards for each program.</p>
        </details>
        <details class="card p-6">
          <summary><strong>Can I volunteer?</strong></summary>
          <p class="mt-3">Absolutely. We run monthly reading circles and community events.</p>
        </details>
        <details class="card p-6">
          <summary><strong>Where do you operate?</strong></summary>
          <p class="mt-3">Currently Singapore, Malaysia, Indonesia, and the Philippines.</p>
        </details>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="cta-section">
    <div class="container py-16 text-white text-center">
      <h2 class="text-shadow">Ready to change a child’s day?</h2>
      <p class="mt-3 opacity-90">Make a one-time gift or start a monthly donation.</p>
      <div class="mt-6 flex justify-center gap-4">
        <button class="btn-donate" @click="donate">Donate ${{ selected }}</button>
        <a class="btn-secondary" href="/donate-monthly">Give monthly</a>
      </div>
      <p class="mt-4 text-sm opacity-80">Receipts issued instantly • Cancel anytime</p>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="section-white">
    <div class="container py-10">
      <div class="grid md:grid-cols-3 gap-6 text-slate-600">
        <div>
          <h3 class="text-slate-900">BrightSteps Foundation</h3>
          <p class="mt-2">
            UEN 201234567A · 21 Orchard Blvd, Singapore<br />
            hello@brightsteps.org · +65 6000 0000
          </p>
        </div>
        <div>
          <h3 class="text-slate-900">Transparency</h3>
          <p class="mt-2">Annual report · Impact dashboards · Independent audits</p>
        </div>
        <div>
          <h3 class="text-slate-900">Get involved</h3>
          <p class="mt-2">Volunteer · Corporate giving · School partnerships</p>
        </div>
      </div>
      <div class="mt-8 text-sm text-slate-500">© {{ new Date().getFullYear() }} BrightSteps Foundation</div>
    </div>
  </footer>
</template>
