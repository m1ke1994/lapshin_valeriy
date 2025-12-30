<template>
  <section ref="section" class="scroll-wrapper" aria-hidden="true">
    <div class="pin">
      <canvas ref="canvas"></canvas>
    </div>
    <div v-if="navLoading" class="nav-loader" role="status" aria-live="polite">
      <div class="nav-loader__spinner"></div>
    </div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const section = ref(null)
const canvas = ref(null)
const navLoading = ref(false)

const TOTAL_FRAMES = 1202
const FRAME_STEP = 2
const MOBILE_STEP = 15

const CACHE_LIMIT_DESKTOP = 32
const CACHE_LIMIT_MOBILE = 16

const WINDOW_FWD_DESKTOP = 8
const WINDOW_BACK_DESKTOP = 4
const WINDOW_FWD_MOBILE = 4
const WINDOW_BACK_MOBILE = 2

const CONCURRENT_DESKTOP = 2
const CONCURRENT_MOBILE = 1
const JUMP_ABORT_THRESHOLD = WINDOW_FWD_DESKTOP * 2

const anchorConfig = [
  { id: 'top', frameProgress: 0 },
  { id: 'values', frameProgress: 0.13 },
  { id: 'approach', frameProgress: 0.27 },
  { id: 'competencies', frameProgress: 0.52 },
  { id: 'trust', frameProgress: 0.6 },
  { id: 'certificates', frameProgress: 0.7 },
  { id: 'projects', frameProgress: 0.8 },
  { id: 'contacts', frameProgress: 0.98 },
]

const NAV_TO_FRAME = {
  philosophy: 0,
  methodology: 16,
  direction: 32,
  trust: 52,
  projects: 72,
  contacts: 96,
  consultation: 118,
}
const NAV_MAX = 118

const clamp = (v, min, max) => Math.min(max, Math.max(min, v))
const framePath = (idx) => `/bg/frame${idx + 1}.webp`

let ctx = null
let destroyed = false
let scrollRange = 1
let keyframes = []
let isMobileDevice = false

const desiredFrame = ref(0)
let lastAppliedFrame = -1
let rafId = 0
let lastPrefetchCenter = -1

// caches
const decoded = new Map() // idx -> ImageBitmap
const cacheOrder = [] // LRU order
const inFlight = new Map() // idx -> { promise, controller }
const queued = new Set()
const loadQueue = [] // { index, priority, resolve, reject, gen }
let activeLoads = 0
let generation = 0

const resizeCanvas = () => {
  const el = canvas.value
  if (!el) return
  const dpr = window.devicePixelRatio || 1
  const width = el.clientWidth || window.innerWidth
  const height = el.clientHeight || window.innerHeight
  const w = Math.floor(width * dpr)
  const h = Math.floor(height * dpr)
  if (el.width !== w || el.height !== h) {
    el.width = w
    el.height = h
    el.style.width = `${width}px`
    el.style.height = `${height}px`
    ctx = el.getContext('2d')
  }
}

const getCacheLimit = () => (isMobileDevice ? CACHE_LIMIT_MOBILE : CACHE_LIMIT_DESKTOP)
const getConcurrency = () => (isMobileDevice ? CONCURRENT_MOBILE : CONCURRENT_DESKTOP)
const getWindowConfig = () =>
  isMobileDevice
    ? { windowFwd: WINDOW_FWD_MOBILE, windowBack: WINDOW_BACK_MOBILE }
    : { windowFwd: WINDOW_FWD_DESKTOP, windowBack: WINDOW_BACK_DESKTOP }

const applyFrameStep = (frameRaw) => {
  const step = isMobileDevice ? MOBILE_STEP : FRAME_STEP
  const snapped = Math.round(frameRaw / step) * step
  return clamp(snapped, 0, TOTAL_FRAMES - 1)
}

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
      const targetFrame = Math.round(clamp(item.frameProgress ?? 0, 0, 1) * (TOTAL_FRAMES - 1))
      return { p, frame: clamp(targetFrame, 0, TOTAL_FRAMES - 1) }
    })
    .filter(Boolean)
    .sort((a, b) => a.p - b.p)

  const first = { p: 0, frame: 0 }
  const last = { p: 1, frame: TOTAL_FRAMES - 1 }

  if (!anchors.length) {
    keyframes = [first, last]
    return
  }

  if (anchors[0].p > 0) anchors.unshift(first)
  if (anchors[anchors.length - 1].p < 1) anchors.push(last)
  keyframes = anchors
}

const mapProgressToFrame = (progress) => {
  if (!keyframes.length) return progress * (TOTAL_FRAMES - 1)
  const p = clamp(progress, 0, 1)
  let prev = keyframes[0]
  for (let i = 1; i < keyframes.length; i += 1) {
    const next = keyframes[i]
    if (p <= next.p) {
      const span = Math.max(0.0001, next.p - prev.p)
      const local = clamp((p - prev.p) / span, 0, 1)
      return prev.frame + (next.frame - prev.frame) * local
    }
    prev = next
  }
  return keyframes[keyframes.length - 1].frame
}

const evictIfNeeded = () => {
  const limit = getCacheLimit()
  while (cacheOrder.length > limit) {
    const idx = cacheOrder.shift()
    if (idx === undefined) break
    const bmp = decoded.get(idx)
    if (bmp && typeof bmp.close === 'function') bmp.close()
    decoded.delete(idx)
  }
}

const touchCache = (index, bitmap) => {
  if (decoded.has(index)) {
    cacheOrder.splice(cacheOrder.indexOf(index), 1)
  }
  decoded.set(index, bitmap)
  cacheOrder.push(index)
  evictIfNeeded()
}

const abortAll = (keepIndex = null) => {
  for (const [idx, entry] of inFlight.entries()) {
    if (keepIndex !== null && idx === keepIndex) continue
    entry.controller?.abort()
    inFlight.delete(idx)
  }
  loadQueue.length = 0
  queued.clear()
  activeLoads = 0
  generation += 1
}

const startLoadTask = (task) => {
  const { index, resolve, reject, gen } = task
  const controller = new AbortController()
  const promise = (async () => {
    try {
      const resp = await fetch(framePath(index), { signal: controller.signal })
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const blob = await resp.blob()
      const bitmap = await createImageBitmap(blob)
      if (destroyed || gen !== generation) {
        bitmap?.close?.()
        return null
      }
      touchCache(index, bitmap)
      return bitmap
    } finally {
      activeLoads = Math.max(0, activeLoads - 1)
      inFlight.delete(index)
      queued.delete(index)
      pumpQueue()
    }
  })()

  inFlight.set(index, { promise, controller })
  promise.then(resolve).catch((err) => {
    if (err?.name === 'AbortError') return resolve(null)
    reject(err)
  })
}

const pumpQueue = () => {
  if (destroyed) return
  const concurrentLimit = getConcurrency()
  if (activeLoads >= concurrentLimit) return
  if (loadQueue.length > 1) loadQueue.sort((a, b) => a.priority - b.priority)
  while (activeLoads < concurrentLimit && loadQueue.length) {
    const next = loadQueue.shift()
    if (!next) break
    activeLoads += 1
    startLoadTask(next)
  }
}

const enqueueLoad = (index, priority = 0) => {
  const idx = clamp(Math.round(index), 0, TOTAL_FRAMES - 1)
  if (decoded.has(idx)) return Promise.resolve(decoded.get(idx))
  if (inFlight.has(idx)) return inFlight.get(idx).promise
  if (queued.has(idx)) {
    const existing = loadQueue.find((item) => item.index === idx)
    if (existing) existing.priority = Math.min(existing.priority, priority)
    return inFlight.get(idx)?.promise || Promise.resolve(null)
  }
  let resolveFn
  let rejectFn
  const promise = new Promise((resolve, reject) => {
    resolveFn = resolve
    rejectFn = reject
  })
  loadQueue.push({ index: idx, priority, resolve: resolveFn, reject: rejectFn, gen: generation })
  queued.add(idx)
  inFlight.set(idx, { promise, controller: null })
  pumpQueue()
  return promise
}

const ensureFrame = (index, priority = -10) => enqueueLoad(index, priority)

const schedulePrefetch = (center) => {
  const { windowFwd, windowBack } = getWindowConfig()
  const step = isMobileDevice ? MOBILE_STEP : FRAME_STEP
  for (let i = step; i <= windowFwd; i += step) {
    const idx = center + i
    if (idx < TOTAL_FRAMES) enqueueLoad(idx, 5 + i)
  }
  for (let i = step; i <= windowBack; i += step) {
    const idx = center - i
    if (idx >= 0) enqueueLoad(idx, 5 + i)
  }
}

const drawFrame = (index) => {
  if (destroyed) return
  const bmp = decoded.get(index)
  const el = canvas.value
  if (!el || !bmp) return
  if (!ctx) ctx = el.getContext('2d')
  if (!ctx) return

  const canvasWidth = el.width || 0
  const canvasHeight = el.height || 0
  if (!canvasWidth || !canvasHeight) return

  const imgWidth = bmp.width
  const imgHeight = bmp.height
  if (!imgWidth || !imgHeight) return

  const scale = Math.max(canvasWidth / imgWidth, canvasHeight / imgHeight)
  const drawWidth = imgWidth * scale
  const drawHeight = imgHeight * scale
  const offsetX = (canvasWidth - drawWidth) * 0.5
  const offsetY = (canvasHeight - drawHeight) * 0.5

  ctx.setTransform(1, 0, 0, 1, 0, 0)
  ctx.globalAlpha = 1
  ctx.imageSmoothingEnabled = true
  ctx.drawImage(bmp, offsetX, offsetY, drawWidth, drawHeight)
  lastAppliedFrame = index
}

const tick = () => {
  rafId = window.requestAnimationFrame(tick)
  if (destroyed) return
  const targetFrame = applyFrameStep(desiredFrame.value)
  if (targetFrame === lastAppliedFrame) {
    schedulePrefetch(targetFrame)
    return
  }

  const jumpThreshold = (isMobileDevice ? WINDOW_FWD_MOBILE : WINDOW_FWD_DESKTOP) * 2 || JUMP_ABORT_THRESHOLD
  if (lastPrefetchCenter === -1 || Math.abs(targetFrame - lastPrefetchCenter) > jumpThreshold) {
    abortAll(targetFrame)
  }
  lastPrefetchCenter = targetFrame

  ensureFrame(targetFrame, -20)
    .then((bmp) => {
      if (!bmp || destroyed) return
      if (applyFrameStep(desiredFrame.value) !== targetFrame) return
      drawFrame(targetFrame)
    })
    .catch(() => {})

  schedulePrefetch(targetFrame)

  if (decoded.has(targetFrame)) {
    drawFrame(targetFrame)
  }
}

const onScroll = () => {
  if (destroyed) return
  const scrollTop = window.scrollY || window.pageYOffset || 0
  const ratio = scrollRange ? clamp(scrollTop / scrollRange, 0, 1) : 0
  desiredFrame.value = mapProgressToFrame(ratio)
}

const onResize = () => {
  if (destroyed) return
  resizeCanvas()
  rebuildKeyframes()
  onScroll()
}

const resolveNavTargetFrame = (sectionId) => {
  const raw = NAV_TO_FRAME[sectionId]
  if (typeof raw !== 'number' || Number.isNaN(raw)) return null
  return Math.round((raw / NAV_MAX) * (TOTAL_FRAMES - 1))
}

const scrollSectionIntoView = (sectionId) => {
  const domId = sectionId
  const target = document.getElementById(domId) || document.querySelector(`#${domId}`)
  if (!target) return
  const headerEl = document.querySelector('.header')
  const offset = (headerEl?.offsetHeight || 80) + 10
  const start = window.scrollY || window.pageYOffset || 0
  const end = target.getBoundingClientRect().top + start - offset
  window.scrollTo({ top: end, behavior: 'smooth' })
}

const handleNavNavigate = (event) => {
  const detail = event?.detail || {}
  const sectionId = (detail.sectionId || detail.hash || '').replace(/^#/, '').trim()
  const target = resolveNavTargetFrame(sectionId)
  if (typeof target === 'number') {
    desiredFrame.value = target
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

onMounted(() => {
  isMobileDevice = window.matchMedia('(max-width: 768px)').matches
  clearStaticBackground()
  resizeCanvas()
  rebuildKeyframes()
  onScroll()

  ensureFrame(0, -30)
    .then(() => drawFrame(0))
    .catch(() => {})

  if (!rafId) rafId = window.requestAnimationFrame(tick)

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

  abortAll()
  for (const bmp of decoded.values()) {
    if (bmp && typeof bmp.close === 'function') bmp.close()
  }
  decoded.clear()
  cacheOrder.length = 0
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

.pin {
  position: static;
  width: 100%;
  height: 0;
  overflow: visible;
  pointer-events: none;
}

.pin canvas {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
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
