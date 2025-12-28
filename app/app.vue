<template>
  <div class="app-root">
    <AppHeader />
    <NuxtPage />
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted } from 'vue'
import AppHeader from '../components/AppHeader.vue'

let revealObserver

const setupScrollReveal = async () => {
  if (typeof window === 'undefined') return
  if (!('IntersectionObserver' in window)) return

  await nextTick()

  const targets = Array.from(document.querySelectorAll('.reveal'))
  if (!targets.length) return

  document.documentElement.classList.add('reveal-ready')
  revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        entry.target.classList.add('is-visible')
        observer.unobserve(entry.target)
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -10% 0px' }
  )

  targets.forEach((target) => revealObserver.observe(target))
}

onMounted(() => {
  if (typeof window === 'undefined') return
  if ('scrollRestoration' in window.history) {
    window.history.scrollRestoration = 'manual'
  }
  window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
  setupScrollReveal()
})

onBeforeUnmount(() => {
  if (revealObserver) {
    revealObserver.disconnect()
    revealObserver = null
  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');
@import url('@/assets/styles/sections.css');

:root {
  --bg: transparent;
  --scroll-bg-image: none;
  --surface: rgba(255, 255, 255, 1);
  --surface-strong: rgba(255, 255, 255, 0.9);
  --surface-soft: rgba(255, 255, 255, 0.24);
  --text: #1b1f28;
  --muted: #4b5462;
  --accent: #2f5b7c;
  --accent-strong: #20445d;
  --accent-warm: #9a7b58;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  background-color: transparent;
}

html,
body,
#__nuxt,
.app-root {
  background: transparent;
}

html,
body {
  overflow-x: hidden;
}

body {
  margin: 0;
  font-family: "Manrope", "Segoe UI", sans-serif;
  background: transparent;
  color: var(--text);
}

a {
  color: inherit;
}

.app-root {
  min-height: 100vh;
  color: var(--text);
  position: relative;
  z-index: 1;
}
</style>
