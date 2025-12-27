<template>
  <main class="page">
    <ScrollBgAnimation />

    <section id="about" class="section section--about">
      <div class="section-inner">
        <p class="eyebrow">IKB Studio / 2025</p>
        <h2>Build the inevitable.</h2>
        <p class="lead">
          Premium digital presence for ambitious products. We blend motion,
          typography, and performance to make your brand feel inevitable.
        </p>
        <div class="chips">
          <span>Brand</span>
          <span>Product</span>
          <span>Motion</span>
          <span>Growth</span>
        </div>
      </div>
      <div class="glow glow--top" aria-hidden="true"></div>
    </section>

    <section id="services" class="section section--services">
      <div class="section-inner">
        <div class="section-head">
          <p class="eyebrow">Services</p>
          <h2>Design systems, cinematic scroll, fast shipping.</h2>
          <p class="lead">
            From first concept to production-ready UI, we focus on clarity,
            speed, and emotional impact.
          </p>
        </div>
        <div class="grid">
          <article class="card">
            <h3>Identity + Direction</h3>
            <p>Visual language, tone, and narrative that scales.</p>
          </article>
          <article class="card">
            <h3>Product UI</h3>
            <p>High-velocity interfaces built with Nuxt and Vue.</p>
          </article>
          <article class="card">
            <h3>Motion + Scroll</h3>
            <p>Frame-driven storytelling without heavy libraries.</p>
          </article>
        </div>
      </div>
    </section>

    <section id="projects" class="section section--projects">
      <div class="section-inner">
        <div class="section-head">
          <p class="eyebrow">Projects</p>
          <h2>Selected work.</h2>
          <p class="lead">
            Boutique launches, premium campaigns, and brand refreshes.
          </p>
        </div>
        <div class="list">
          <div class="list-item">
            <span class="list-title">Aurora Labs</span>
            <span class="list-meta">Brand + Web</span>
          </div>
          <div class="list-item">
            <span class="list-title">Vector Cloud</span>
            <span class="list-meta">Product UI</span>
          </div>
          <div class="list-item">
            <span class="list-title">Kite Protocol</span>
            <span class="list-meta">Campaign</span>
          </div>
        </div>
      </div>
      <div class="glow glow--side" aria-hidden="true"></div>
    </section>

    <section id="contacts" class="section section--contacts">
      <div class="section-inner">
        <p class="eyebrow">Contact</p>
        <h2>Let us build your next release.</h2>
        <p class="lead">
          Say hello and we will craft the experience around your goals.
        </p>
        <div class="cta">
          <a href="mailto:hello@ikb.studio">hello@ikb.studio</a>
          <span>+00 000 000 000</span>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
</script>

<style scoped>
.page {
  min-height: 100vh;
}

.section {
  position: relative;
  padding: 160px 24px;
  overflow: hidden;
}

.section-inner {
  max-width: 1100px;
  margin: 0 auto;
}

.section--about {
  background: linear-gradient(135deg, rgba(17, 18, 22, 0.9), rgba(10, 10, 12, 0.6));
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.section--services {
  background: rgba(15, 16, 19, 0.85);
}

.section--projects {
  background: linear-gradient(135deg, rgba(18, 20, 24, 0.95), rgba(11, 12, 14, 0.8));
}

.section--contacts {
  background: rgba(10, 11, 13, 0.95);
}

.eyebrow {
  margin: 0 0 12px;
  font-size: 12px;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.55);
}

h2 {
  font-size: clamp(36px, 5vw, 64px);
  line-height: 1.05;
  margin: 0 0 20px;
}

.lead {
  font-size: 18px;
  line-height: 1.7;
  margin: 0 0 28px;
  max-width: 720px;
  color: var(--muted);
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.chips span {
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
}

.section-head {
  margin-bottom: 48px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.card {
  padding: 28px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.card h3 {
  margin: 0 0 12px;
  font-size: 18px;
}

.card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.6;
}

.list {
  display: grid;
  gap: 18px;
}

.list-item {
  display: flex;
  justify-content: space-between;
  padding: 18px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 16px;
}

.list-title {
  font-weight: 500;
}

.list-meta {
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  font-size: 11px;
}

.cta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 18px;
}

.cta a {
  color: var(--accent);
  text-decoration: none;
}

.glow {
  position: absolute;
  pointer-events: none;
  filter: blur(70px);
  opacity: 0.45;
}

.glow--top {
  width: 400px;
  height: 240px;
  background: radial-gradient(circle, rgba(65, 240, 192, 0.6), transparent 70%);
  top: -120px;
  right: 10%;
}

.glow--side {
  width: 360px;
  height: 280px;
  background: radial-gradient(circle, rgba(242, 184, 109, 0.6), transparent 70%);
  bottom: -120px;
  left: 8%;
}

@media (max-width: 720px) {
  .section {
    padding: 120px 20px;
  }

  .list-item {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
