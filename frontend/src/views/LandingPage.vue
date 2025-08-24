<script setup>
import { ref } from 'vue'

/* --- Donation quick amounts --- */
const selected = ref(100)
const amounts = [50, 100, 250, 500]
function choose(a){ selected.value = a }
function donate(){
  // Replace with REACH's actual donation system
  window.location.href = 'mailto:info@reach.org.hk?subject=Donation%20Inquiry&body=I%20would%20like%20to%20donate%20HK$' + selected.value + '%20to%20support%20REACH%20programs.'
}
</script>

<template>
<!-- HERO -->
<header
  class="hero-photo tint-dark text-white"
  style="--hero-bg:url('https://reach.org.hk/_assets/media/bccd049f097f1b6c3fa333cefd16ff30.jpg')"
>
  <div class="container py-20 md:py-28 flex justify-center">
    <div class="max-w-4xl mx-auto animate-slide-up text-center">
      <span class="trust-badge mb-6 inline-block">Registered Education Charity • Since 2012</span>
      <h1 class="hero-title">
        Give every Hong Kong child a <span class="text-gradient">reading start</span>
      </h1>
      <p class="hero-lead mt-4 max-w-3xl mx-auto">
        REACH bridges the English proficiency gap for K3 students from low-income families, 
        preparing them for Primary 1 success through proven reading programs in Hong Kong's most underserved communities.
      </p>

      <div class="mt-8 flex flex-wrap justify-center items-center gap-4">
        <button class="btn-donate" @click="donate">Fund a child's future</button>
        <a href="#about" class="btn-secondary">Learn about REACH</a>
      </div>

      <div class="social-proof mt-8">
        12+ years of impact • Academic leadership • K3 transition specialists
      </div>
    </div>
  </div>
</header>

  <!-- ABOUT -->
  <section id="about" class="section-white">
    <div class="container py-16">
      <div class="grid md:grid-cols-2 gap-8 items-center">
        <div class="card p-8 animate-slide-left">
          <h2>Breaking barriers at the start</h2>
          <p class="mt-3">
            <strong>REACH</strong> (Race for Education Accessibilities for Every Child) targets the critical K3-to-Primary-1 transition 
            where English proficiency gaps can determine a child's entire educational trajectory.
          </p>
          <p>
            Founded by education expert Vivian Chung, we deliver intensive English programs directly in kindergartens 
            across Hong Kong's poorest districts, serving families in sub-divided flats who need it most.
          </p>
          <div class="impact-highlight">
            "Reading ability is the most effective and sustainable means for opening doors to better academic and life-long development." — REACH Mission
          </div>
        </div>

        <div class="grid gap-6 animate-slide-right">
          <article class="story-card">
            <img alt="Children in classroom learning English" class="w-full h-44 object-cover"
                 src="https://images.unsplash.com/photo-1497486751825-1233686d5d80?q=80&w=1600" />
            <div class="p-6">
              <h3>K3 Bridge Program</h3>
              <p>Weekly 45-60 minute sessions with proprietary curriculum and learning app assessments.</p>
            </div>
          </article>
          <article class="story-card">
            <img alt="Parents helping children with homework" class="w-full h-44 object-cover"
                 src="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=1600" />
            <div class="p-6">
              <h3>Parent Support</h3>
              <p>Home learning materials with video instructions to extend classroom impact.</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- MISSION / VALUES -->
  <section class="section-light">
    <div class="container py-16">
      <h2 class="text-center font-weight-700 text-slate-900" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">Why the K3 transition matters</h2>
      <p class="text-center mt-2 text-lg text-slate-600 font-weight-500">This critical year shapes everything that follows in a child's education.</p>

      <div class="grid md:grid-cols-3 gap-6 mt-10">
        <div class="card p-6">
          <h3>Early intervention</h3>
          <p>Age 5-6 is when reading foundations solidify. Missing this window creates gaps that compound yearly.</p>
        </div>
        <div class="card p-6">
          <h3>Proven impact</h3>
          <p>12+ years serving Hong Kong families with measurable pre/post assessments and graduation celebrations.</p>
        </div>
        <div class="card p-6">
          <h3>Expert leadership</h3>
          <p>Led by education psychologist Vivian Chung with 20+ years experience and Columbia University training.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- IMPACT STATS -->
  <section id="impact" class="section-white">
    <div class="container py-16">
      <h2 class="text-center font-weight-700 text-slate-900" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">Your impact in Hong Kong</h2>
      <p class="text-center mt-2 text-lg text-slate-600 font-weight-500">Every donation directly supports children facing the greatest educational challenges.</p>

      <div class="grid md:grid-cols-4 gap-6 mt-10">
        <div class="stat-card">
          <div class="stat-number">12+</div>
          <p>Years of operation</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">K3</div>
          <p>Critical transition age</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">20+</div>
          <p>Hours weekly programming</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">100%</div>
          <p>Graduation success rate</p>
        </div>
      </div>
    </div>
  </section>

  <!-- PROGRAMS -->
  <section class="section-light">
    <div class="container py-16">
      <h2 class="text-center mb-10 font-weight-700 text-slate-900" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">Programs needing your support</h2>
      <div class="grid md:grid-cols-3 gap-6">
        <article class="card p-6">
          <h3>English Bridge Program</h3>
          <p class="mt-2">Intensive K3 curriculum with proprietary assessment app and minimum 12-lesson cycles.</p>
          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 45%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">Seeking expansion funding</p>
          </div>
        </article>
        <article class="card p-6">
          <h3>Home Learning Support</h3>
          <p class="mt-2">Parent education materials with video guides to reinforce classroom learning at home.</p>
          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 30%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">Technology development needed</p>
          </div>
        </article>
        <article class="card p-6">
          <h3>Teacher Training</h3>
          <p class="mt-2">Professional development workshops for volunteer educators and curriculum enhancement.</p>
          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 60%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">Volunteer training ongoing</p>
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
          <h2>Fund a child's reading future</h2>
          <p class="mt-2">Your donation bridges the gap between poverty and Primary 1 success.</p>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <button
              v-for="a in amounts" :key="a"
              class="amount-btn"
              :class="{'selected': selected===a}"
              @click="choose(a)"
            >
              HK${{ a }}
              <div class="progress-mini mt-2">
                <div class="progress-fill-mini" :style="{ width: (Math.min(a/500,1)*100)+'%' }"></div>
              </div>
            </button>
          </div>

          <div class="donation-highlight mt-6">
            <strong>HK${{ selected }}</strong> can provide <strong>{{ Math.round(selected/50) }} weeks</strong> of K3 bridge programming.
          </div>

          <div class="mt-6 flex gap-4">
            <button class="btn-donate flex-1" @click="donate">Donate HK${{ selected }}</button>
            <a class="btn-secondary flex-1" href="mailto:info@reach.org.hk">Contact us</a>
          </div>

          <p class="mt-4 text-sm text-slate-600">
            Registered charity • Tax-deductible • Direct school impact
          </p>
        </div>

        <div class="impact-preview p-8 animate-slide-right">
          <h3 class="mb-3">How your donation creates change</h3>
          <ul class="list-disc ml-5 space-y-2">
            <li>HK$50 funds one child's weekly K3 lesson</li>
            <li>HK$100 provides learning materials for 2 students</li>
            <li>HK$250 sponsors a full month of programming</li>
            <li>HK$500 covers assessment app development</li>
          </ul>

          <div class="mt-6">
            <div class="progress-bar-large">
              <div class="progress-fill-large" style="width: 35%"></div>
            </div>
            <p class="mt-2 text-sm text-slate-600">Campaign: Expanding to 3 new kindergartens in 2025</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- SUCCESS STORIES -->
  <section class="section-light">
    <div class="container py-16">
      <h2 class="text-center font-weight-700 text-slate-900" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">Real impact in Hong Kong communities</h2>
      <div class="grid md:grid-cols-3 gap-6 mt-10">
        <article class="story-card p-6">
          <p>"27 students graduated our K3 program at Yan Oi Tong Pang Hung Cheung Kindergarten—every single child ready for Primary 1."</p>
          <p class="mt-3 text-slate-600">— 2023 Program Success</p>
        </article>
        <article class="story-card p-6">
          <p>"REACH doesn't just teach English—they transform confidence. Parents see the difference at home immediately."</p>
          <p class="mt-3 text-slate-600">— Partner kindergarten teacher</p>
        </article>
        <article class="story-card p-6">
          <p>"Professional curriculum with Columbia University standards, delivered where it matters most."</p>
          <p class="mt-3 text-slate-600">— Education sector review</p>
        </article>
      </div>
    </div>
  </section>

  <!-- PARTNERS -->
  <section class="section-white">
    <div class="container py-16">
      <h2 class="text-center font-weight-700 text-slate-900" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">Trusted partnerships across Hong Kong</h2>
      <p class="text-center mt-2 text-lg text-slate-600 font-weight-500">We work directly with kindergartens and schools in the most underserved districts.</p>
      <div class="grid md:grid-cols-4 gap-6 mt-10">
        <div class="card p-6 text-center">Yan Oi Tong Kindergarten</div>
        <div class="card p-6 text-center">Story Jungle English Centre</div>
        <div class="card p-6 text-center">Time Auction</div>
        <div class="card p-6 text-center">Columbia University Alumni</div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section-light">
    <div class="container py-16">
      <h2 class="text-center font-weight-700 text-slate-900" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">Frequently asked questions</h2>
      <div class="grid md:grid-cols-2 gap-6 mt-10">
        <details class="card p-6">
          <summary><strong>Is REACH a registered charity?</strong></summary>
          <p class="mt-3">Yes, REACH is a registered education charity in Hong Kong, incorporated February 9, 2012, with tax-exempt status.</p>
        </details>
        <details class="card p-6">
          <summary><strong>Why focus specifically on K3 students?</strong></summary>
          <p class="mt-3">K3 is the critical transition year to Primary 1. Reading foundations set at age 5-6 determine long-term academic success.</p>
        </details>
        <details class="card p-6">
          <summary><strong>How do you measure impact?</strong></summary>
          <p class="mt-3">We use proprietary assessment apps for pre/post evaluation and celebrate graduation ceremonies showcasing student progress.</p>
        </details>
        <details class="card p-6">
          <summary><strong>Who leads REACH programs?</strong></summary>
          <p class="mt-3">Founder Vivian Chung holds an MA in Psychology in Education from Columbia University with 20+ years in Hong Kong education.</p>
        </details>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="cta-section">
    <div class="container py-16 text-white text-center">
      <h2 class="text-shadow">Ready to bridge the gap?</h2>
      <p class="mt-3 opacity-90">Fund K3 students' transition to Primary 1 success.</p>
      <div class="mt-6 flex justify-center gap-4">
        <button class="btn-donate" @click="donate">Donate HK${{ selected }}</button>
        <a class="btn-secondary" href="mailto:info@reach.org.hk">Partnership inquiry</a>
      </div>
      <p class="mt-4 text-sm opacity-80">Supporting Hong Kong's most vulnerable students since 2012</p>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="section-white">
    <div class="container py-10">
      <div class="grid md:grid-cols-3 gap-6 text-slate-600">
        <div>
          <h3 class="text-slate-900">REACH Foundation</h3>
          <p class="mt-2">
            Incorporated 9 Feb 2012 • Room 902, 9/F, 168 Queen's Road Central<br />
            info@reach.org.hk • (852) 3100 0135
          </p>
        </div>
        <div>
          <h3 class="text-slate-900">Our Impact</h3>
          <p class="mt-2">K3 bridge programs • Parent support • Assessment technology</p>
        </div>
        <div>
          <h3 class="text-slate-900">Get Involved</h3>
          <p class="mt-2">Volunteer teaching • School partnerships • Corporate giving</p>
        </div>
      </div>
      <div class="mt-8 text-sm text-slate-500">© {{ new Date().getFullYear() }} REACH Foundation Hong Kong</div>
    </div>
  </footer>
</template>