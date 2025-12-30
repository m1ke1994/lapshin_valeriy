<template>
  <div class="app-root">
    <AppHeader />
    <NuxtPage />
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted } from 'vue'
import { useHead } from '#imports'
import AppHeader from '../components/AppHeader.vue'

const REVEAL_SCROLL_START = 60
let revealObserver
let revealTargets = []
let revealStarted = false

useHead({
  link: [
    { rel: 'preload', as: 'image', href: '/bg/frame1.webp' },
    { rel: 'preload', as: 'image', href: '/bg/frame2.webp' },
    { rel: 'preload', as: 'image', href: '/bg/frame3.webp' },
    { rel: 'preload', as: 'image', href: '/bg/frame4.webp' },
    { rel: 'preload', as: 'image', href: '/bg/frame5.webp' },
  ],
})

const prepareRevealTargets = async () => {
  if (typeof window === 'undefined') return
  document.documentElement.classList.add('reveal-ready')
  await nextTick()

  revealTargets = Array.from(document.querySelectorAll('.reveal'))
}

const startRevealObserver = () => {
  if (revealStarted) return
  revealStarted = true

  if (!revealTargets.length) return

  if (!('IntersectionObserver' in window)) {
    revealTargets.forEach((target) => target.classList.add('is-visible'))
    return
  }

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

  revealTargets.forEach((target) => revealObserver.observe(target))
}

const handleRevealScroll = () => {
  if (typeof window === 'undefined') return
  const scrollTop = window.scrollY || window.pageYOffset || 0
  if (scrollTop < REVEAL_SCROLL_START) return
  startRevealObserver()
  window.removeEventListener('scroll', handleRevealScroll)
}

const setupScrollReveal = async () => {
  if (typeof window === 'undefined') return
  await prepareRevealTargets()
  handleRevealScroll()
  window.addEventListener('scroll', handleRevealScroll, { passive: true })
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
  if (typeof window !== 'undefined') {
    window.removeEventListener('scroll', handleRevealScroll)
  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');
@import url('@/assets/styles/sections.css');

:root {
  --bg: #f7f4ec;
  --scroll-bg-image: none;
  --surface: rgba(255, 255, 255, 0.82);
  --surface-strong: rgba(255, 255, 255, 0.94);
  --surface-soft: rgba(255, 255, 255, 0.14);
  --text: #0f121a;
  --text-rgb: 15, 18, 26;
  --muted: #3d4554;
  --muted-rgb: 61, 69, 84;
  --accent: #d6b36a;
  --accent-strong: #b88935;
  --accent-rgb: 214, 179, 106;
  --accent-soft: rgba(var(--accent-rgb), 0.16);
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  background-color: var(--bg);
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
  background: var(--bg);
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
