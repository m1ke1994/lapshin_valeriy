<template>
  <header class="header">
    <nav class="nav">
      <NuxtLink to="/" class="logo" @click.prevent="scrollToHash('#top')">IKB — Инженерное бюро</NuxtLink>

      <div class="links">
        <a
          v-for="item in navItems"
          :key="item.href"
          :href="item.href"
          @click.prevent="scrollToHash(item.href)"
        >
          {{ item.label }}
        </a>
      </div>

      <a href="#contacts" class="header-cta" @click.prevent="scrollToHash('#contacts')">Запланировать разговор</a>
    </nav>
  </header>
</template>

<script setup>
const navItems = [
  { label: 'Философия', href: '#values' },
  { label: 'Методика', href: '#approach' },
  { label: 'Направления', href: '#competencies' },
  { label: 'Доверие', href: '#trust' },
  { label: 'Проекты', href: '#projects' },
  { label: 'Контакты', href: '#contacts' },
]

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3)

const scrollToHash = (hash) => {
  if (typeof window === 'undefined') return
  const target = document.querySelector(hash)
  const headerEl = document.querySelector('.header')
  const offset = (headerEl?.offsetHeight || 80) + 10

  const start = window.scrollY || window.pageYOffset || 0
  const end = target
    ? target.getBoundingClientRect().top + start - offset
    : 0

  const duration = 900
  const startTs = performance.now()

  const step = (ts) => {
    const progress = Math.min(1, (ts - startTs) / duration)
    const eased = easeOutCubic(progress)
    const next = start + (end - start) * eased
    window.scrollTo(0, next)
    if (progress < 1) {
      requestAnimationFrame(step)
    } else if (hash) {
      window.location.hash = hash
    }
  }

  requestAnimationFrame(step)
}
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 50;
  backdrop-filter: blur(18px);
  background: rgba(255, 255, 255, 0.64);
  border-bottom: 1px solid rgba(27, 31, 40, 0.12);
}

.nav {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.logo {
  font-weight: 700;
  font-size: 16px;
  text-decoration: none;
  color: var(--text);
  letter-spacing: 0.28em;
  text-transform: uppercase;
}

.links a {
  margin-left: 24px;
  text-decoration: none;
  color: var(--text);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  opacity: 0.72;
  transition: opacity 0.2s ease, color 0.2s ease;
}

.links a:hover {
  opacity: 1;
  color: var(--accent);
}

.header-cta {
  padding: 10px 16px;
  border-radius: 999px;
  border: 1px solid rgba(200, 155, 60, 0.35);
  text-decoration: none;
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--text);
  background: rgba(255, 255, 255, 0.82);
  transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 12px 30px rgba(27, 31, 40, 0.16);
}

.header-cta:hover {
  border-color: rgba(184, 132, 26, 0.65);
  color: var(--accent-strong);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 18px 42px rgba(27, 31, 40, 0.2);
}

@media (max-width: 900px) {
  .links {
    display: none;
  }

  .nav {
    justify-content: space-between;
  }
}
</style>
