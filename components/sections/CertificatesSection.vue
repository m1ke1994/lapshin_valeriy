<template>
  <section id="certificates" class="section certificates">
    <div class="section-inner reveal">
      <div class="section-head cert-head">
        <div class="cert-copy">
          <p class="eyebrow">{{ copy.eyebrow }}</p>
          <h2>{{ copy.title }}</h2>
          <p class="lead">{{ copy.lead }}</p>
        </div>
      </div>

      <div class="cert-grid premium-grid">
        <button
          v-for="item in items"
          :key="item.id"
          type="button"
          class="cert-card glass-card"
          @click="openById(item.id)"
        >
          <div class="cert-media">
            <span class="cert-shine" aria-hidden="true"></span>
            <span class="cert-ring" aria-hidden="true"></span>
            <img :src="item.src" :alt="item.title" loading="lazy" />
            <span class="cert-badge">{{ typeLabel(item.type) }}</span>
          </div>

          <div class="cert-body">
            <div class="cert-title">{{ item.title }}</div>
            <p class="cert-subtitle">{{ item.subtitle }}</p>
          </div>
        </button>
      </div>
    </div>

    <teleport to="body">
      <transition name="fade">
        <div v-if="isOpen" class="viewer-overlay" role="dialog" aria-modal="true" @click="close">
          <div class="viewer-shell" @click.stop>
            <div class="viewer-top">
              <div class="viewer-meta">
                <span class="viewer-type">{{ typeLabel(activeItem?.type || 'certificate') }}</span>
                <h3 class="viewer-title">{{ activeItem?.title }}</h3>
                <p class="viewer-subtitle">{{ activeItem?.subtitle }}</p>
              </div>
              <button ref="closeBtn" type="button" class="viewer-close" @click="close">
                {{ copy.actions.close }}
              </button>
            </div>

            <div class="viewer-body">
              <button
                type="button"
                class="viewer-nav prev"
                @click="prev"
                :aria-label="copy.actions.prev"
              >
                &larr;
              </button>

              <figure class="viewer-figure">
                <img :src="activeItem?.src" :alt="activeItem?.title" draggable="false" />
              </figure>

              <button
                type="button"
                class="viewer-nav next"
                @click="next"
                :aria-label="copy.actions.next"
              >
                &rarr;
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useLocale } from '~/composables/useLocale'
import type { DocType } from '~/content/translations'

const { t } = useLocale()
const copy = computed(() => t.value.certificates)
const items = computed(() => copy.value.items)

function typeLabel(type: DocType) {
  return copy.value.typeLabels[type] || type
}

const isOpen = ref(false)
const activeIndex = ref<number>(0)
const closeBtn = ref<HTMLButtonElement | null>(null)

const activeItem = computed(() => items.value[activeIndex.value])

let lastFocused: Element | null = null
let prevBodyOverflow = ''

function open(index: number) {
  lastFocused = document.activeElement
  prevBodyOverflow = document.body.style.overflow
  document.body.style.overflow = 'hidden'

  activeIndex.value = index
  isOpen.value = true

  nextTick(() => closeBtn.value?.focus())
}

function openById(id: string) {
  const idx = items.value.findIndex((x) => x.id === id)
  if (idx >= 0) open(idx)
}

function close() {
  isOpen.value = false
  document.body.style.overflow = prevBodyOverflow || ''

  if (lastFocused instanceof HTMLElement) {
    nextTick(() => lastFocused?.focus())
  }
}

function next() {
  activeIndex.value = (activeIndex.value + 1) % items.value.length
}

function prev() {
  activeIndex.value = (activeIndex.value - 1 + items.value.length) % items.value.length
}

function onKeydown(e: KeyboardEvent) {
  if (!isOpen.value) return
  if (e.key === 'Escape') close()
  if (e.key === 'ArrowRight') next()
  if (e.key === 'ArrowLeft') prev()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))
</script>

<style scoped>
.certificates {
  position: relative;
  overflow: hidden;
}

.certificates::before,
.certificates::after {
  content: "";
  position: absolute;
  inset: 6% 10% auto auto;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(var(--accent-rgb), 0.22), rgba(var(--accent-rgb), 0));
  filter: blur(16px);
  pointer-events: none;
}

.certificates::after {
  inset: auto auto 4% 6%;
  width: 380px;
  height: 380px;
  background: radial-gradient(circle, rgba(15, 18, 26, 0.18), rgba(15, 18, 26, 0));
}

.cert-head {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
  gap: 18px;
  align-items: flex-end;
}

.cert-copy {
  display: grid;
  gap: 8px;
}

.cert-grid {
  margin-top: 18px;
}

.premium-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.cert-card {
  position: relative;
  display: grid;
  gap: 12px;
  padding: 14px;
  border-radius: 18px;
  text-align: left;
  border: 1px solid rgba(var(--accent-rgb), 0.32);
  background: linear-gradient(140deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.78));
  cursor: pointer;
  transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
}

.cert-card:hover {
  transform: translateY(-4px);
  border-color: rgba(var(--accent-rgb), 0.55);
  box-shadow: 0 22px 46px rgba(15, 18, 26, 0.22);
}

.cert-card:focus-visible {
  outline: 3px solid rgba(var(--accent-rgb), 0.55);
  outline-offset: 2px;
}

.cert-media {
  position: relative;
  overflow: hidden;
  border-radius: 14px;
  aspect-ratio: 3 / 4;
  background: linear-gradient(135deg, rgba(15, 18, 26, 0.06), rgba(15, 18, 26, 0.02));
}

.cert-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 260ms ease;
}

.cert-card:hover img {
  transform: scale(1.03);
}

.cert-badge {
  position: absolute;
  left: 12px;
  top: 12px;
  padding: 7px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  color: var(--text);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  border: 1px solid rgba(var(--accent-rgb), 0.36);
  box-shadow: 0 12px 26px rgba(15, 18, 26, 0.18);
}

.cert-shine,
.cert-ring {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.cert-shine {
  background: radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.32), transparent 45%);
  mix-blend-mode: screen;
}

.cert-ring {
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 16px;
}

.cert-body {
  display: grid;
  gap: 6px;
}

.cert-title {
  font-weight: 700;
  font-size: 15px;
}

.cert-subtitle {
  margin: 0;
  color: var(--muted);
  line-height: 1.6;
}

.viewer-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background:
    radial-gradient(circle at 20% 20%, rgba(var(--accent-rgb), 0.12), transparent 42%),
    rgba(5, 7, 10, 0.86);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px;
}

.viewer-shell {
  width: min(1180px, 94vw);
  border-radius: 20px;
  background: rgba(15, 18, 26, 0.86);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.38);
  padding: 18px;
  display: grid;
  gap: 14px;
}

.viewer-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}

.viewer-meta {
  display: grid;
  gap: 6px;
}

.viewer-type {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.72);
}

.viewer-title {
  margin: 0;
  font-size: 20px;
  color: #fff;
  letter-spacing: -0.01em;
}

.viewer-subtitle {
  margin: 0;
  color: rgba(255, 255, 255, 0.75);
}

.viewer-close {
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-size: 11px;
  cursor: pointer;
  transition: transform 180ms ease, background 180ms ease, border-color 180ms ease;
}

.viewer-close:hover {
  transform: translateY(-1px);
  background: rgba(255, 255, 255, 0.16);
  border-color: rgba(var(--accent-rgb), 0.5);
}

.viewer-body {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: linear-gradient(140deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 420px;
}

.viewer-figure {
  margin: 0;
  padding: 16px;
}

.viewer-figure img {
  max-width: min(1080px, 82vw);
  max-height: 80vh;
  border-radius: 12px;
  box-shadow: 0 18px 52px rgba(0, 0, 0, 0.36);
  display: block;
}

.viewer-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.24);
  background: rgba(15, 18, 26, 0.6);
  color: #fff;
  display: grid;
  place-items: center;
  font-size: 22px;
  cursor: pointer;
  transition: transform 180ms ease, background 180ms ease, border-color 180ms ease;
}

.viewer-nav:hover {
  transform: translateY(-50%) scale(1.05);
  border-color: rgba(var(--accent-rgb), 0.5);
  background: rgba(15, 18, 26, 0.78);
}

.viewer-nav.prev {
  left: 14px;
}

.viewer-nav.next {
  right: 14px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 160ms ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 980px) {
  .cert-head {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .cert-card {
    padding: 12px;
  }

  .viewer-shell {
    padding: 14px;
  }

  .viewer-body {
    min-height: 320px;
  }

  .viewer-nav {
    width: 38px;
    height: 38px;
  }
}
</style>
