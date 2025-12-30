<template>
  <section ref="section" class="scroll-wrapper" aria-hidden="true">
    <video
      ref="videoEl"
      class="scroll-video"
      muted
      playsinline
      preload="auto"
    >
      <source src="/bg/bg.webm" type="video/webm; codecs=vp9" />
      <source src="/bg/bg.mp4" type="video/mp4" />
    </video>
    <div v-if="navLoading" class="nav-loader" role="status" aria-live="polite">
      <div class="nav-loader__spinner"></div>
    </div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const section = ref(null)
const videoEl = ref(null)
const navLoading = ref(false)

const IDLE_TIMEOUT_MS = 200
const DEFAULT_THRESHOLD = 0.03
const SAVEDATA_THRESHOLD = 0.07
const DEFAULT_DAMPING = 0.2
const SAVEDATA_DAMPING = 0.1

const anchorConfig = [
  { id: 'top', progress: 0 },
  { id: 'values', progress: 0.13 },
  { id: 'approach', progress: 0.27 },
  { id: 'competencies', progress: 0.52 },
  { id: 'trust', progress: 0.6 },
  { id: 'certificates', progress: 0.7 },
  { id: 'projects', progress: 0.8 },
  { id: 'contacts', progress: 0.98 },
]

const NAV_TO_PROGRESS = {
  philosophy: 0,
  methodology: 16,
  direction: 32,
  trust: 52,
  projects: 72,
  contacts: 96,
  consultation: 118,
}
const NAV_MAX = 118

const clamp = (v, min = 0, max = 1) => Math.min(max, Math.max(min, v))

let destroyed = false
let scrollRange = 1
let keyframes = []
let rafId = 0
let lastActivity = 0
let prefersReducedMotion = false
let saveDataMode = false
let damping = DEFAULT_DAMPING
let threshold = DEFAULT_THRESHOLD
let duration = 0
let targetProgress = 0

const measureScrollRange = () => {
  const doc = document.documentElement
  const body = document.body
  const fullHeight = Math.max(body.scrollHeight, body.offsetHeight, doc.clientHeight, doc.scrollHeight, doc.offsetHeight)
  return Math.max(1, fullHeight - window.innerHeight)
}

const rebuildKeyframes = () => {
  const maxScroll = measureScrollRange()
  scrollRange = maxScroll

  const anchors = anchorConfig
    .map((item) => {
      const el = document.getElementById(item.id)
      if (!el) return null
      const top = (window.scrollY || window.pageYOffset || 0) + el.getBoundingClientRect().top
      const p = clamp(top / maxScroll, 0, 1)
      const progress = clamp(item.progress ?? 0, 0, 1)
      return { p, progress }
    })
    .filter(Boolean)
    .sort((a, b) => a.p - b.p)

  const first = { p: 0, progress: 0 }
  const last = { p: 1, progress: 1 }

  if (!anchors.length) {
    keyframes = [first, last]
    return
  }

  if (anchors[0].p > 0) anchors.unshift(first)
  if (anchors[anchors.length - 1].p < 1) anchors.push(last)
  keyframes = anchors
}

const mapScrollToProgress = (progress) => {
  if (!keyframes.length) return clamp(progress, 0, 1)
  const p = clamp(progress, 0, 1)
  let prev = keyframes[0]
  for (let i = 1; i < keyframes.length; i += 1) {
    const next = keyframes[i]
    if (p <= next.p) {
      const span = Math.max(0.0001, next.p - prev.p)
      const local = clamp((p - prev.p) / span, 0, 1)
      return prev.progress + (next.progress - prev.progress) * local
    }
    prev = next
  }
  return keyframes[keyframes.length - 1].progress
}

const updateEnvironmentFlags = () => {
  const connection = navigator.connection || navigator.webkitConnection || navigator.mozConnection
  saveDataMode = !!connection?.saveData
  prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  damping = saveDataMode ? SAVEDATA_DAMPING : DEFAULT_DAMPING
  threshold = saveDataMode ? SAVEDATA_THRESHOLD : DEFAULT_THRESHOLD
}

const requestTick = () => {
  if (destroyed || rafId) return
  rafId = window.requestAnimationFrame(tick)
}

const tick = () => {
  rafId = 0
  if (destroyed) return
  const video = videoEl.value
  if (!video) return

  const now = performance.now()
  const idleTime = now - lastActivity
  const shouldStop = idleTime > IDLE_TIMEOUT_MS

  duration = video.duration || duration || 0

  if (prefersReducedMotion) {
    if (duration && video.currentTime !== 0) video.currentTime = 0
    if (!shouldStop) requestTick()
    return
  }

  if (!duration) {
    if (!shouldStop) requestTick()
    return
  }

  const targetTime = clamp(targetProgress, 0, 1) * duration
  const current = video.currentTime || 0
  const delta = targetTime - current
  const absDelta = Math.abs(delta)

  if (absDelta > threshold) {
    const nextTime = current + delta * damping
    video.currentTime = clamp(nextTime, 0, duration)
  }

  if (!shouldStop && (absDelta > threshold || idleTime <= IDLE_TIMEOUT_MS)) {
    requestTick()
  }
}

const onScroll = () => {
  if (destroyed) return
  const scrollTop = window.scrollY || window.pageYOffset || 0
  const ratio = scrollRange ? clamp(scrollTop / scrollRange, 0, 1) : 0
  targetProgress = mapScrollToProgress(ratio)
  lastActivity = performance.now()
  requestTick()
}

const onResize = () => {
  if (destroyed) return
  updateEnvironmentFlags()
  rebuildKeyframes()
  onScroll()
}

const resolveNavTargetProgress = (sectionId) => {
  const raw = NAV_TO_PROGRESS[sectionId]
  if (typeof raw !== 'number' || Number.isNaN(raw)) return null
  return clamp(raw / NAV_MAX, 0, 1)
}

const scrollSectionIntoView = (sectionId) => {
  const target = document.getElementById(sectionId) || document.querySelector(`#${sectionId}`)
  if (!target) return
  const headerEl = document.querySelector('.header')
  const offset = (headerEl?.offsetHeight || 80) + 10
  const start = window.scrollY || window.pageYOffset || 0
  const end = target.getBoundingClientRect().top + start - offset
  window.scrollTo({ top: end, behavior: prefersReducedMotion ? 'auto' : 'smooth' })
}

const handleNavNavigate = (event) => {
  const detail = event?.detail || {}
  const sectionId = (detail.sectionId || detail.hash || '').replace(/^#/, '').trim()
  const target = resolveNavTargetProgress(sectionId)
  if (typeof target === 'number') {
    targetProgress = target
    lastActivity = performance.now()
    requestTick()
    scrollSectionIntoView(sectionId)
  }
}

const clearStaticBackground = () => {
  const doc = document.documentElement
  const body = document.body
  doc.style.setProperty('--scroll-bg-image', 'none')
  doc.style.backgroundImage = 'none'
  body.style.backgroundImage = 'none'
}

const handleLoadedMetadata = () => {
  const video = videoEl.value
  if (!video) return
  duration = video.duration || duration
  const startTime = clamp(targetProgress, 0, 1) * (duration || 0)
  if (Number.isFinite(startTime)) {
    video.currentTime = startTime
  }
}

onMounted(() => {
  updateEnvironmentFlags()
  clearStaticBackground()
  rebuildKeyframes()
  onScroll()

  const video = videoEl.value
  if (video) {
    video.addEventListener('loadedmetadata', handleLoadedMetadata)
    video.play().catch(() => {})
  }

  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onResize, { passive: true })
  window.addEventListener('scroll-bg:navigate', handleNavNavigate, false)
})

onBeforeUnmount(() => {
  destroyed = true
  if (rafId) window.cancelAnimationFrame(rafId)
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('scroll-bg:navigate', handleNavNavigate, false)

  const video = videoEl.value
  if (video) {
    video.removeEventListener('loadedmetadata', handleLoadedMetadata)
  }
})
</script>

<style scoped>
.scroll-wrapper {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 0;
  z-index: 0;
  pointer-events: none;
}

.scroll-video {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
  z-index: 0;
}

.nav-loader {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 18, 26, 0.28);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 9999;
  pointer-events: all;
}

.nav-loader__spinner {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.38);
  border-top-color: rgba(var(--accent-rgb), 0.9);
  animation: nav-spin 0.9s linear infinite;
  box-shadow: 0 10px 32px rgba(0, 0, 0, 0.16);
}

@keyframes nav-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
