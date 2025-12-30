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
    { rel: 'preload', as: 'video', href: '/bg/bg.webm', type: 'video/webm; codecs=vp9' },
    { rel: 'preload', as: 'video', href: '/bg/bg.mp4', type: 'video/mp4' },
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
  --heading-color: #BB8E3D;
  --field-bg: rgba(255, 255, 255, 0.88);
  --field-bg-hover: rgba(255, 255, 255, 0.94);
  --field-border: rgba(var(--text-rgb), 0.18);
  --field-border-strong: rgba(var(--text-rgb), 0.28);
  --field-placeholder: rgba(var(--text-rgb), 0.55);
  --field-disabled: rgba(var(--text-rgb), 0.35);
  --field-invalid: #d65a5a;
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

.ikb-highlight {
  color: var(--heading-color);
  font-weight: 700;
}

.ikb-field,
.ikb-field input,
.ikb-field textarea,
.ikb-field select,
input.ikb-field,
textarea.ikb-field,
select.ikb-field {
  width: 100%;
  padding: 14px 14px;
  border-radius: 12px;
  border: 1px solid var(--field-border);
  background: var(--field-bg);
  color: var(--text);
  font-size: 16px;
  line-height: 1.5;
  outline: none;
  transition:
    border-color 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease,
    color 160ms ease;
  box-shadow: 0 8px 22px rgba(15, 18, 26, 0.08);
  appearance: none;
}

.ikb-field::placeholder,
input.ikb-field::placeholder,
textarea.ikb-field::placeholder {
  color: var(--field-placeholder);
}

.ikb-field:hover,
input.ikb-field:hover,
textarea.ikb-field:hover,
select.ikb-field:hover {
  border-color: var(--field-border-strong);
  background: var(--field-bg-hover);
}

.ikb-field:focus,
.ikb-field:focus-visible,
input.ikb-field:focus,
input.ikb-field:focus-visible,
textarea.ikb-field:focus,
textarea.ikb-field:focus-visible,
select.ikb-field:focus,
select.ikb-field:focus-visible {
  border-color: rgba(var(--accent-rgb), 0.75);
  background: #fff;
  box-shadow:
    0 10px 28px rgba(15, 18, 26, 0.12),
    0 0 0 3px rgba(var(--accent-rgb), 0.2);
  outline: 2px solid rgba(var(--accent-rgb), 0.18);
  outline-offset: 1px;
}

.ikb-field:disabled,
input.ikb-field:disabled,
textarea.ikb-field:disabled,
select.ikb-field:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background: rgba(255, 255, 255, 0.65);
  border-color: rgba(var(--text-rgb), 0.16);
  color: var(--field-disabled);
  box-shadow: none;
}

.ikb-field[aria-invalid='true'],
input.ikb-field[aria-invalid='true'],
textarea.ikb-field[aria-invalid='true'],
select.ikb-field[aria-invalid='true'],
.ikb-field.is-invalid {
  border-color: var(--field-invalid);
  box-shadow: 0 0 0 3px rgba(214, 90, 90, 0.15);
}

.ikb-field[type='date'],
.ikb-field[type='time'],
input.ikb-field[type='date'],
input.ikb-field[type='time'] {
  -webkit-appearance: none;
  appearance: none;
  padding-right: 48px;
  font-variant-numeric: tabular-nums;
  min-height: 52px;
}

.ikb-field[type='date']::-webkit-calendar-picker-indicator,
.ikb-field[type='time']::-webkit-calendar-picker-indicator,
input.ikb-field[type='date']::-webkit-calendar-picker-indicator,
input.ikb-field[type='time']::-webkit-calendar-picker-indicator {
  cursor: pointer;
  padding: 8px;
  margin-right: 4px;
  border-radius: 12px;
  background-color: transparent;
  filter: none;
}

.ikb-field[type='date']::-webkit-datetime-edit,
.ikb-field[type='time']::-webkit-datetime-edit {
  padding: 2px 0;
  color: var(--text);
}

.ikb-field[type='date']::-webkit-datetime-edit-fields-wrapper,
.ikb-field[type='time']::-webkit-datetime-edit-fields-wrapper {
  letter-spacing: 0.04em;
}

@media (max-width: 720px) {
  .ikb-field,
  .ikb-field input,
  .ikb-field textarea,
  .ikb-field select,
  input.ikb-field,
  textarea.ikb-field,
  select.ikb-field {
    padding: 16px 16px;
    border-radius: 14px;
    box-shadow: 0 12px 26px rgba(15, 18, 26, 0.12);
  }

  .ikb-field[type='date'],
  .ikb-field[type='time'],
  input.ikb-field[type='date'],
  input.ikb-field[type='time'] {
    padding-right: 54px;
    min-height: 56px;
  }
}
</style>
