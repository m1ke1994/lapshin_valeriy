<template>
  <header class="header" :class="{ 'is-menu-open': isMenuOpen }">
    <nav class="nav" aria-label="Primary">
      <NuxtLink to="/" class="logo" @click.prevent="scrollToHash('#top')">
        <span class="logo-mark">IKB</span>
        <span class="logo-meta">
          <span class="logo-sep">-</span>
          <span class="logo-text">{{ headerCopy.logoTagline }}</span>
        </span>
      </NuxtLink>

      <div class="links" role="navigation" aria-label="Sections">
        <a
          v-for="item in navItems"
          :key="item.href"
          :href="item.href"
          class="nav-link"
          :class="{ active: activeHash === item.href }"
          @click.prevent="scrollToHash(item.href)"
        >
          <span class="nav-link__label">{{ item.label }}</span>
          <span class="nav-link__underline" aria-hidden="true"></span>
        </a>
      </div>

      <div class="actions">
        <div class="locale-switch" role="group" :aria-label="headerCopy.languageLabel">
          <button
            class="locale-btn"
            type="button"
            :aria-pressed="locale === 'ru'"
            :class="{ active: locale === 'ru' }"
            @click="changeLocale('ru')"
          >
            {{ headerCopy.languageShort.ru }}
          </button>
          <span class="locale-divider">/</span>
          <button
            class="locale-btn"
            type="button"
            :aria-pressed="locale === 'en'"
            :class="{ active: locale === 'en' }"
            @click="changeLocale('en')"
          >
            {{ headerCopy.languageShort.en }}
          </button>
        </div>

        <a href="#contacts" class="header-cta" @click.prevent="scrollToHash('#contacts')">
          <span class="cta-text">{{ headerCopy.cta }}</span>
          <span class="cta-shine" aria-hidden="true"></span>
        </a>

        <button
          class="burger"
          type="button"
          :aria-expanded="isMenuOpen ? 'true' : 'false'"
          aria-controls="mobileMenu"
          :aria-label="headerCopy.menuOpenLabel"
          @click="toggleMenu"
        >
          <span class="burger-lines" aria-hidden="true">
            <span></span><span></span><span></span>
          </span>
        </button>
      </div>
    </nav>

    <transition name="fade">
      <div v-if="isMenuOpen" class="overlay" @click="closeMenu" aria-hidden="true"></div>
    </transition>

    <transition name="slide">
      <div
        v-if="isMenuOpen"
        id="mobileMenu"
        class="mobile"
        role="dialog"
        aria-modal="true"
        :aria-label="headerCopy.menuTitle"
      >
        <div class="mobile-top">
          <div class="mobile-title">{{ headerCopy.menuTitle }}</div>
          <button class="mobile-close" type="button" :aria-label="headerCopy.menuClose" @click="closeMenu">
            ×
          </button>
        </div>

        <div class="mobile-links">
          <a
            v-for="item in navItems"
            :key="item.href"
            :href="item.href"
            class="mobile-link"
            :class="{ active: activeHash === item.href }"
            @click.prevent="scrollToHash(item.href)"
          >
            <span>{{ item.label }}</span>
            <span class="mobile-dot" aria-hidden="true"></span>
          </a>
        </div>

        <a href="#contacts" class="mobile-cta" @click.prevent="scrollToHash('#contacts')">
          {{ headerCopy.cta }}
        </a>
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useLocale } from '~/composables/useLocale'
import type { Locale } from '~/content/translations'

const navTargets = ['#values', '#approach', '#competencies', '#trust', '#projects', '#contacts']
const { locale, setLocale, t } = useLocale()
const headerCopy = computed(() => t.value.header)
const navItems = computed(() => navTargets.map((href, index) => ({ href, label: headerCopy.value.nav[index] || href })))

const isMenuOpen = ref(false)
const activeHash = ref('')

const changeLocale = (value: Locale) => {
  if (locale.value === value) return
  setLocale(value)
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
const closeMenu = () => {
  isMenuOpen.value = false
}

const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3)

const getHeaderOffset = () => {
  const headerEl = document.querySelector('.header') as HTMLElement | null
  return (headerEl?.offsetHeight || 80) + 10
}

const scrollToHash = (hash: string) => {
  if (typeof window === 'undefined') return
  closeMenu()
  activeHash.value = hash

  const target = document.querySelector(hash)
  const offset = getHeaderOffset()

  const start = window.scrollY || window.pageYOffset || 0
  const end = target ? target.getBoundingClientRect().top + start - offset : 0

  const duration = 900
  const startTs = performance.now()

  const step = (ts: number) => {
    const progress = Math.min(1, (ts - startTs) / duration)
    const eased = easeOutCubic(progress)
    const next = start + (end - start) * eased
    window.scrollTo(0, next)

    if (progress < 1) requestAnimationFrame(step)
    else if (hash) window.history.replaceState(null, '', hash)
  }

  requestAnimationFrame(step)
}

let observer: IntersectionObserver | null = null
let resizeTimer = 0

const setupActiveSectionObserver = () => {
  if (typeof window === 'undefined') return
  if (observer) observer.disconnect()

  const offset = getHeaderOffset()
  const sections = navTargets.map((href) => document.querySelector(href)).filter(Boolean) as Element[]

  if (!sections.length) return

  const ratios = new Map<string, number>()

  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const id = entry.target?.id ? `#${entry.target.id}` : ''
        if (!id) continue
        ratios.set(id, entry.isIntersecting ? entry.intersectionRatio : 0)
      }

      let bestHash = ''
      let bestRatio = 0
      for (const [hash, ratio] of ratios.entries()) {
        if (ratio > bestRatio) {
          bestRatio = ratio
          bestHash = hash
        }
      }

      if (!bestHash) {
        const y = window.scrollY || window.pageYOffset || 0
        let bestTop = -Infinity
        for (const el of sections) {
          const top = el.getBoundingClientRect().top + y - offset
          if (top <= y + 2 && top > bestTop) {
            bestTop = top
            bestHash = `#${el.id}`
          }
        }
      }

      activeHash.value = bestHash || ''
    },
    {
      root: null,
      rootMargin: `-${offset}px 0px -40% 0px`,
      threshold: [0.12, 0.22, 0.35, 0.5, 0.65, 0.8],
    }
  )

  sections.forEach((el) => observer?.observe(el))
}

const onResize = () => {
  clearTimeout(resizeTimer)
  resizeTimer = window.setTimeout(setupActiveSectionObserver, 150)
}

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') closeMenu()
}

onMounted(() => {
  if (typeof window === 'undefined') return
  setupActiveSectionObserver()
  window.addEventListener('resize', onResize, { passive: true })
  window.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
  window.removeEventListener('resize', onResize)
  window.removeEventListener('keydown', onKeydown)
  clearTimeout(resizeTimer)
})
</script>

<style scoped>
.header {
  position: fixed;
  inset: 0 0 auto 0;
  z-index: 50;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  background: rgba(255, 255, 255, 0.7);
  border-bottom: 1px solid rgba(var(--text-rgb), 0.08);
  box-shadow: 0 14px 46px rgba(27, 31, 40, 0.08);
}

.header::before {
  content: "";
  position: absolute;
  left: 24px;
  right: 24px;
  bottom: -1px;
  height: 1px;
  background: linear-gradient(
    90deg,
    rgba(var(--accent-rgb), 0),
    rgba(var(--accent-rgb), 0.35),
    rgba(var(--accent-rgb), 0)
  );
  pointer-events: none;
}

.nav {
  max-width: 1280px;
  margin: 0 auto;
  padding: 14px 28px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 18px;
}

.logo {
  justify-self: start;
  display: inline-flex;
  align-items: baseline;
  gap: 12px;
  text-decoration: none;
  color: var(--text);
  letter-spacing: 0.22em;
  text-transform: uppercase;
  line-height: 1;
  transition: transform 220ms ease, opacity 220ms ease;
}

.logo:hover {
  transform: translateY(-1px);
  opacity: 0.92;
}

.logo-mark {
  font-weight: 900;
  font-size: 18px;
  line-height: 1;
  letter-spacing: 0.24em;
}

.logo-meta {
  display: inline-flex;
  align-items: baseline;
  gap: 10px;
  line-height: 1;
}

.logo-sep {
  opacity: 0.35;
  font-weight: 700;
  font-size: 12px;
  line-height: 1;
}

.logo-text {
  font-weight: 700;
  font-size: 12px;
  opacity: 0.86;
  line-height: 1;
  letter-spacing: 0.2em;
}

.links {
  justify-self: center;
  display: flex;
  align-items: center;
  gap: 22px;
}

.nav-link {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text);
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  opacity: 0.72;
  transition: opacity 200ms ease, transform 200ms ease, color 200ms ease;
}

.nav-link:hover {
  opacity: 1;
  transform: translateY(-1px);
  color: var(--accent);
}

.nav-link.active {
  opacity: 1;
  color: var(--accent-strong);
}

.nav-link__underline {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -10px;
  height: 2px;
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    rgba(var(--accent-rgb), 0),
    rgba(var(--accent-rgb), 0.6),
    rgba(var(--accent-rgb), 0)
  );
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 240ms ease;
}

.nav-link:hover .nav-link__underline,
.nav-link.active .nav-link__underline {
  transform: scaleX(1);
}

.nav-link.active .nav-link__underline {
  filter: drop-shadow(0 10px 18px rgba(var(--accent-rgb), 0.22));
}

.actions {
  justify-self: end;
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.locale-switch {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(var(--accent-rgb), 0.32);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 12px 28px rgba(15, 18, 26, 0.12);
}

.locale-btn {
  border: none;
  background: transparent;
  color: var(--muted);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  padding: 4px 6px;
  border-radius: 10px;
  cursor: pointer;
  transition: color 180ms ease, background 180ms ease, transform 180ms ease;
}

.locale-btn.active {
  color: var(--accent-strong);
  background: rgba(var(--accent-rgb), 0.15);
  transform: translateY(-1px);
}

.locale-divider {
  font-size: 11px;
  color: rgba(var(--text-rgb), 0.5);
}

.header-cta {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border-radius: 999px;
  text-decoration: none;
  color: var(--text);
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(var(--accent-rgb), 0.3);
  box-shadow: 0 14px 36px rgba(27, 31, 40, 0.14);
  overflow: hidden;
  transition:
    transform 220ms ease,
    box-shadow 220ms ease,
    border-color 220ms ease,
    color 220ms ease,
    background 220ms ease;
}

.header-cta:hover {
  transform: translateY(-1px);
  border-color: rgba(var(--accent-rgb), 0.6);
  color: var(--accent-strong);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 18px 46px rgba(27, 31, 40, 0.18);
}

.cta-text {
  position: relative;
  z-index: 1;
}

.cta-shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.35) 35%,
    rgba(255, 255, 255, 0) 70%
  );
  transform: translateX(-120%);
  transition: transform 600ms ease;
}

.header-cta:hover .cta-shine {
  transform: translateX(120%);
}

.burger {
  display: none;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  border: 1px solid rgba(27, 31, 40, 0.12);
  background: rgba(255, 255, 255, 0.84);
  box-shadow: 0 10px 28px rgba(27, 31, 40, 0.12);
  cursor: pointer;
  transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
}

.burger:hover {
  transform: translateY(-1px);
  border-color: rgba(var(--accent-rgb), 0.35);
  box-shadow: 0 14px 36px rgba(27, 31, 40, 0.16);
}

.burger-lines {
  width: 18px;
  height: 14px;
  display: inline-flex;
  flex-direction: column;
  justify-content: space-between;
}

.burger-lines span {
  display: block;
  height: 2px;
  border-radius: 999px;
  background: rgba(27, 31, 40, 0.72);
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(13, 16, 22, 0.42);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 49;
}

.mobile {
  position: fixed;
  top: 12px;
  left: 12px;
  right: 12px;
  z-index: 60;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(27, 31, 40, 0.12);
  box-shadow: 0 22px 60px rgba(27, 31, 40, 0.22);
  overflow: hidden;
}

.mobile-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(27, 31, 40, 0.1);
  background: rgba(255, 255, 255, 0.7);
}

.mobile-title {
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  opacity: 0.82;
}

.mobile-close {
  width: 40px;
  height: 40px;
  border-radius: 14px;
  border: 1px solid rgba(27, 31, 40, 0.12);
  background: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: transform 200ms ease, border-color 200ms ease;
}

.mobile-close:hover {
  transform: translateY(-1px);
  border-color: rgba(var(--accent-rgb), 0.3);
}

.mobile-links {
  padding: 10px 10px 14px;
  display: grid;
  gap: 6px;
}

.mobile-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 14px;
  border-radius: 16px;
  text-decoration: none;
  color: var(--text);
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  border: 1px solid rgba(27, 31, 40, 0.1);
  background: rgba(255, 255, 255, 0.78);
  transition: transform 200ms ease, border-color 200ms ease, background 200ms ease, color 200ms ease;
}

.mobile-link:hover {
  transform: translateY(-1px);
  border-color: rgba(var(--accent-rgb), 0.32);
  background: rgba(255, 255, 255, 0.92);
  color: var(--accent);
}

.mobile-link.active {
  border-color: rgba(var(--accent-rgb), 0.4);
  color: var(--accent-strong);
}

.mobile-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: rgba(var(--accent-rgb), 0.55);
  box-shadow: 0 0 0 6px rgba(var(--accent-rgb), 0.12);
}

.mobile-cta {
  margin: 0 10px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px 16px;
  border-radius: 18px;
  text-decoration: none;
  color: var(--text);
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  border: 1px solid rgba(var(--accent-rgb), 0.34);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 16px 40px rgba(27, 31, 40, 0.14);
  transition: transform 200ms ease, box-shadow 200ms ease, color 200ms ease;
}

.mobile-cta:hover {
  transform: translateY(-1px);
  color: var(--accent-strong);
  box-shadow: 0 20px 52px rgba(27, 31, 40, 0.18);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 180ms ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 220ms ease, opacity 220ms ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateY(-8px);
  opacity: 0;
}

@media (max-width: 980px) {
  .nav {
    grid-template-columns: 1fr auto;
  }
  .links {
    display: none;
  }
  .burger {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .header-cta {
    padding: 10px 14px;
    letter-spacing: 0.18em;
  }
  .logo-text {
    display: none;
  }
}

@media (max-width: 420px) {
  .nav {
    padding: 12px 16px;
  }
  .header-cta {
    display: none;
  }
  .locale-switch {
    padding: 6px 8px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .logo,
  .nav-link,
  .nav-link__underline,
  .header-cta,
  .cta-shine,
  .burger,
  .mobile-link,
  .mobile-cta,
  .fade-enter-active,
  .fade-leave-active,
  .slide-enter-active,
  .slide-leave-active,
  .locale-switch,
  .locale-btn {
    transition: none !important;
  }
}
</style>
