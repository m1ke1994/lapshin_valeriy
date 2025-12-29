<template>
  <!-- Canvas always decorative; loader is the only “interactive” thing -->
  <section ref="section" class="scroll-wrapper" :aria-hidden="!navLoading">
    <div class="pin">
      <canvas ref="canvas"></canvas>
    </div>

    <!-- Loader overlay -->
    <div v-if="navLoading" class="nav-loader" role="status" aria-live="polite" aria-label="Загрузка кадров фона">
      <div class="nav-loader__spinner"></div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const section = ref(null)
const canvas = ref(null)

const totalAvailableFrames = 1202
const framesToUse = totalAvailableFrames
const frameStep = 1

const clamp = (v, min, max) => Math.min(max, Math.max(min, v))

const framePath = (idx) => {
  const frameIndex = Math.min(totalAvailableFrames, 1 + idx * frameStep)
  return `/bg/frame${frameIndex}.webp`
}

const frameCount = framesToUse
const MOBILE_STEP = 2
const mqMobile =
  typeof window !== 'undefined'
    ? window.matchMedia('(max-width: 768px)')
    : {
        matches: false,
        addEventListener: () => {},
        removeEventListener: () => {},
        addListener: () => {},
        removeListener: () => {},
      }
const isMobile = () => mqMobile.matches

// caches / queues
const frameCache = new Map() // idx -> ImageBitmap | HTMLImageElement
const pending = new Map() // idx -> Promise
const queued = new Set() // idx
const loadQueue = [] // { index, resolve, reject, prio, gen }
const abortControllers = new Map() // idx -> AbortController
let activeLoads = 0

// --- tuning ---
const MAX_NEAREST_SEARCH = 24

const SNAP_EPS = 0.001
const SNAP_DELTA = 0.25
const SNAP_LERP = 0.45

const MIN_EASE = 0.1
const MAX_EASE = 0.22
const EASE_FAST_BONUS = 0.05

const FAST_SCROLL_DELTA = 0.08
const BOOST_FORWARD = 6
const PRUNE_MARGIN = 2

const FPS_WINDOW = 30
const FPS_DEGRADE_MS = 23
const FPS_RECOVER_MS = 18
const GOOD_STREAK_TARGET = 80

const MAX_NO_DRAW_FRAMES = 22
const LAYOUT_THROTTLE_MS = 200

// fast scroll reprioritize / coarse mode
const JUMP_THRESHOLD_FRAMES = 120
const FAST_JUMP_THRESHOLD_FRAMES = 60
const FAST_EXIT_STREAK = 6
const STRIDE_FAST = 4
const STRIDE_FAST_LOW = 8
const STRIDE_SLOW_LOW = 2

const BASE_LIMITS_DESKTOP = { concurrent: 4, windowFwd: 18, windowBack: 8 }
const BASE_LIMITS_MOBILE = { concurrent: 2, windowFwd: 12, windowBack: 6 }
const LOW_QUALITY_LIMITS = { windowFwd: 10, windowBack: 5, concurrentDesktop: 3, concurrentMobile: 2 }
const REDUCED_LIMITS = { windowFwd: 6, windowBack: 3, concurrentDesktop: 2, concurrentMobile: 1 }

// anchors (scroll -> frames mapping)
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

// NAV: заданные значения 0..118 (шкала), конвертируем в 0..frameCount-1
const NAV_TO_FRAME = {
  philosophy: 0,
  methodology: 16,
  direction: 32,
  trust: 52,
  projects: 72,
  contacts: 96,
  consultation: 118,
}
const NAV_TO_DOM_ID = {
  philosophy: 'values',
  methodology: 'approach',
  direction: 'competencies',
  trust: 'trust',
  projects: 'projects',
  contacts: 'contacts',
  consultation: 'contacts',
}
const NAV_MAX = 118

// nav smoothing
const NAV_PRELOAD_RADIUS = 6                  // меньше окно перед твином для быстрого старта
const NAV_NEARBY_READY_RADIUS = 3
const NAV_TWEEN_DURATION = 950

// corridor preload to reduce jerks on long jumps
const NAV_CORRIDOR_BACK = 10
const NAV_CORRIDOR_FORWARD_MIN = 26
const NAV_CORRIDOR_FORWARD_MAX = 180

const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
let keyframes = []

// state
const targetProgress = ref(0)
const navLoading = ref(false)
let currentProgress = 0

let rafId = 0
let resizeId = 0
let layoutObserver = null
let layoutObserverId = 0
let layoutThrottleTimeout = 0
let lastLayoutRefreshTs = 0

let scrollRange = 1

let lastTickTs = 0
let lastProgressForSpeed = 0
let lastAvgFrameMs = 0
let lowQuality = false
let fastScrollActive = false
let fastExitStreak = 0
let goodFpsStreak = 0
let badFpsStreak = 0

let reduceMotion = false
let isTouchDevice = false
let isSafari = false

let ctx = null
let ctxConfigured = false
let cleanupBg = null
let destroyed = false

let lastDesiredBase = 0
let lastJumpBaseIndex = -1
let noDrawFrameStreak = 0

// draw cache state
let lastDrawnIndex = -1
let lastDrawnMix = 0
let lastDrawnHadExact = false
let lastDrawnBaseRef = null
let lastDrawnNextRef = null

let lastRenderedFrame = null
let lastRenderedIndex = -1

// loader generation to ignore stale completions after jumps
let loadGeneration = 0

// NAV runtime
let isNavAnimating = false
let navTweenId = 0
let navGen = 0

const frameTimes = []

const clearStaticBackground = () => {
  const doc = document.documentElement
  const body = document.body
  const prev = {
    htmlBg: doc.style.backgroundImage,
    bodyBg: body.style.backgroundImage,
    varBg: doc.style.getPropertyValue('--scroll-bg-image'),
  }
  doc.style.setProperty('--scroll-bg-image', 'none')
  doc.style.backgroundImage = 'none'
  body.style.backgroundImage = 'none'
  cleanupBg = () => {
    doc.style.setProperty('--scroll-bg-image', prev.varBg)
    doc.style.backgroundImage = prev.htmlBg
    body.style.backgroundImage = prev.bodyBg
  }
}

const measureScrollRange = () => {
  const doc = document.documentElement
  const body = document.body
  const fullHeight = Math.max(body.scrollHeight, body.offsetHeight, doc.clientHeight, doc.scrollHeight, doc.offsetHeight)
  return Math.max(1, fullHeight - window.innerHeight)
}

const syncScrollState = () => {
  const scrollTop = window.scrollY || window.pageYOffset || 0
  const ratio = scrollRange ? clamp(scrollTop / scrollRange, 0, 1) : 0
  targetProgress.value = ratio
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
      const targetFrame = Math.round(clamp(item.frameProgress ?? 0, 0, 1) * (frameCount - 1))
      return { p, frame: clamp(targetFrame, 0, frameCount - 1) }
    })
    .filter(Boolean)
    .sort((a, b) => a.p - b.p)

  const first = { p: 0, frame: 0 }
  const last = { p: 1, frame: frameCount - 1 }

  if (!anchors.length) {
    keyframes = [first, last]
    return
  }

  if (anchors[0].p > 0) anchors.unshift(first)
  if (anchors[anchors.length - 1].p < 1) anchors.push(last)
  keyframes = anchors
}

const mapProgressToFrame = (progress) => {
  if (!keyframes.length) return progress * (frameCount - 1)
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

const resizeCanvas = () => {
  const el = canvas.value
  if (!el) return

  const dpr = window.devicePixelRatio || 1
  const width = el.clientWidth || window.innerWidth
  const height = el.clientHeight || window.innerHeight

  const nextWidth = Math.floor(width * dpr)
  const nextHeight = Math.floor(height * dpr)

  if (el.width !== nextWidth || el.height !== nextHeight) {
    el.width = nextWidth
    el.height = nextHeight
    el.style.width = `${width}px`
    el.style.height = `${height}px`

    // reset draw caches
    lastDrawnIndex = -1
    lastDrawnMix = 0
    lastDrawnHadExact = false
    lastDrawnBaseRef = null
    lastDrawnNextRef = null
    lastRenderedIndex = -1
    lastRenderedFrame = null

    ctxConfigured = false
  }
}

const configureContext = () => {
  const el = canvas.value
  if (!el) return
  if (!ctx) ctx = el.getContext('2d')
  if (ctx && !ctxConfigured) {
    ctx.imageSmoothingEnabled = true
    ctxConfigured = true
  }
}

const decodeWithImage = (src, revoke = false) =>
  new Promise((resolve, reject) => {
    const img = new Image()
    img.decoding = 'async'
    img.loading = 'eager'
    img.src = src
    img.onload = () => {
      if (revoke) URL.revokeObjectURL(src)
      resolve(img)
    }
    img.onerror = (err) => {
      if (revoke) URL.revokeObjectURL(src)
      reject(err)
    }
  })

const recordFrameTime = (ms) => {
  if (!Number.isFinite(ms)) return lastAvgFrameMs
  frameTimes.push(ms)
  if (frameTimes.length > FPS_WINDOW) frameTimes.shift()
  const total = frameTimes.reduce((acc, v) => acc + v, 0)
  lastAvgFrameMs = frameTimes.length ? total / frameTimes.length : ms
  return lastAvgFrameMs
}

const applyMobileFrameStep = (frameRaw) => {
  let frameFinal = frameRaw
  if (isMobile()) {
    frameFinal = Math.round(frameRaw / MOBILE_STEP) * MOBILE_STEP
  }
  return clamp(frameFinal, 0, frameCount - 1)
}

const getBaseLimits = () => (isTouchDevice || isSafari ? BASE_LIMITS_MOBILE : BASE_LIMITS_DESKTOP)

const getEffectiveLimits = (fastScroll = false) => {
  const base = getBaseLimits()
  let windowFwd = base.windowFwd
  let windowBack = base.windowBack
  let maxConcurrent = base.concurrent

  if (lowQuality) {
    windowFwd = Math.max(LOW_QUALITY_LIMITS.windowFwd, windowFwd - 6)
    windowBack = Math.max(LOW_QUALITY_LIMITS.windowBack, windowBack - 3)
    maxConcurrent = isTouchDevice || isSafari ? LOW_QUALITY_LIMITS.concurrentMobile : LOW_QUALITY_LIMITS.concurrentDesktop
  }

  if (reduceMotion) {
    windowFwd = REDUCED_LIMITS.windowFwd
    windowBack = REDUCED_LIMITS.windowBack
    maxConcurrent = isTouchDevice || isSafari ? REDUCED_LIMITS.concurrentMobile : REDUCED_LIMITS.concurrentDesktop
  }

  if (fastScroll && !reduceMotion && !isTouchDevice && !isSafari) {
    maxConcurrent = Math.min(8, maxConcurrent + 2)
  }

  const boostedFwd = fastScroll ? windowFwd + BOOST_FORWARD : windowFwd
  return { windowFwd, windowBack, boostedFwd, maxConcurrent }
}

const getDynamicStride = (fast) => {
  if (reduceMotion) return 1
  if (fast) return lowQuality ? STRIDE_FAST_LOW : STRIDE_FAST
  return lowQuality ? STRIDE_SLOW_LOW : 1
}

// --- Priority queue helpers ---
const computePrio = (index, direction = 1) => {
  const dist = Math.abs(index - lastDesiredBase)
  const bias = direction >= 0 ? (index >= lastDesiredBase ? 0 : 0.35) : (index <= lastDesiredBase ? 0 : 0.35)
  return dist + bias
}

const enqueueTask = (index, resolve, reject, { front = false, prio = null } = {}) => {
  if (destroyed) {
    resolve?.(null)
    return
  }
  const idx = clamp(Math.floor(index), 0, frameCount - 1)
  if (frameCache.has(idx) || pending.has(idx) || queued.has(idx)) {
    resolve?.(frameCache.get(idx) ?? null)
    return
  }
  const task = {
    index: idx,
    resolve,
    reject,
    prio: prio ?? computePrio(idx, idx >= lastDesiredBase ? 1 : -1),
    gen: loadGeneration,
  }
  if (front) loadQueue.unshift(task)
  else loadQueue.push(task)
  queued.add(idx)
}

const pumpQueue = () => {
  if (destroyed) return
  const { maxConcurrent } = getEffectiveLimits(fastScrollActive)

  if (loadQueue.length > 1) loadQueue.sort((a, b) => a.prio - b.prio)

  while (activeLoads < maxConcurrent && loadQueue.length) {
    const next = loadQueue.shift()
    if (!next) break
    queued.delete(next.index)
    startLoadTask(next.index, next.resolve, next.reject, next.gen)
  }
}

const loadFrame = (index, { front = false, prio = null } = {}) => {
  if (destroyed) return Promise.resolve(null)
  const idx = clamp(Math.floor(index), 0, frameCount - 1)
  if (frameCache.has(idx)) return Promise.resolve(frameCache.get(idx))
  if (pending.has(idx)) return pending.get(idx)

  const promise = new Promise((resolve, reject) => {
    enqueueTask(idx, resolve, reject, { front, prio })
    pumpQueue()
  })

  pending.set(idx, promise)
  return promise
}

// --- reprioritize on big jumps ---
const abortFarLoadsAndClearQueue = (centerIndex, direction = 1, fast = false) => {
  const { windowFwd, windowBack, boostedFwd } = getEffectiveLimits(fast)

  const keepBack = fast ? 2 : windowBack + PRUNE_MARGIN
  const keepFwd = fast ? Math.max(10, Math.floor((boostedFwd + 4) / 2)) : boostedFwd + PRUNE_MARGIN
  const minKeep = centerIndex - keepBack
  const maxKeep = centerIndex + keepFwd

  loadQueue.length = 0
  queued.clear()

  for (const [idx, controller] of abortControllers.entries()) {
    if (idx < minKeep || idx > maxKeep) {
      controller.abort()
      abortControllers.delete(idx)
      pending.delete(idx)
    }
  }

  const stride = getDynamicStride(fastScrollActive)
  const center = clamp(centerIndex, 0, frameCount - 1)
  const c1 = clamp(center + stride, 0, frameCount - 1)
  const c2 = clamp(center - stride, 0, frameCount - 1)

  loadFrame(center, { front: true, prio: -3 })
  loadFrame(c1, { front: true, prio: -2 })
  loadFrame(c2, { front: true, prio: -1 })
}

const maybeReprioritizeOnJump = (baseIndex, direction = 1) => {
  const dist = lastJumpBaseIndex === -1 ? 0 : Math.abs(baseIndex - lastJumpBaseIndex)
  const threshold = fastScrollActive ? FAST_JUMP_THRESHOLD_FRAMES : JUMP_THRESHOLD_FRAMES
  if (lastJumpBaseIndex === -1 || dist >= threshold) {
    lastJumpBaseIndex = baseIndex
    loadGeneration += 1
    abortFarLoadsAndClearQueue(baseIndex, direction, fastScrollActive)
    pumpQueue()
  }
}

// --- windowing / pruning ---
const ensureWindow = (centerIndex, direction = 1, fast = false) => {
  if (destroyed) return
  const { windowFwd, windowBack, boostedFwd } = getEffectiveLimits(fast)
  const stride = getDynamicStride(fast)

  const backCount = fast ? Math.min(2, windowBack) : windowBack
  const fwdCount = fast ? boostedFwd : boostedFwd

  loadFrame(centerIndex, { front: true, prio: -10 }).catch(() => {})

  for (let i = stride; i <= fwdCount; i += stride) {
    const idx = centerIndex + i
    if (idx < 0 || idx >= frameCount) continue
    loadFrame(idx).catch(() => {})
  }

  for (let i = stride; i <= backCount; i += stride) {
    const idx = centerIndex - i
    if (idx < 0 || idx >= frameCount) continue
    loadFrame(idx).catch(() => {})
  }
}

const pruneCache = (centerIndex) => {
  const { windowFwd, windowBack } = getEffectiveLimits(false)
  const minKeep = centerIndex - windowBack - PRUNE_MARGIN
  const maxKeep = centerIndex + windowFwd + PRUNE_MARGIN
  for (const idx of Array.from(frameCache.keys())) {
    if (idx < minKeep || idx > maxKeep) {
      const frame = frameCache.get(idx)
      if (frame && typeof frame.close === 'function') frame.close()
      frameCache.delete(idx)
    }
  }
}

const findNearbyFrame = (desired) => {
  if (frameCache.has(desired)) return { index: desired, frame: frameCache.get(desired) }
  for (let offset = 1; offset <= MAX_NEAREST_SEARCH; offset += 1) {
    const left = desired - offset
    const right = desired + offset
    if (left >= 0 && frameCache.has(left)) return { index: left, frame: frameCache.get(left) }
    if (right < frameCount && frameCache.has(right)) return { index: right, frame: frameCache.get(right) }
  }
  return null
}

// --- loading ---
const startLoadTask = (index, resolve, reject, gen) => {
  if (destroyed) {
    pending.delete(index)
    resolve(null)
    return
  }

  activeLoads += 1
  const url = framePath(index)
  const controller = new AbortController()
  abortControllers.set(index, controller)

  const settle = () => {
    pending.delete(index)
    abortControllers.delete(index)
    activeLoads = Math.max(0, activeLoads - 1)
  }

  const finish = (frame) => {
    settle()

    if (destroyed || gen !== loadGeneration) {
      if (frame && typeof frame.close === 'function') frame.close()
      resolve(null)
      if (!destroyed) pumpQueue()
      return
    }

    frameCache.set(index, frame)

    if (Math.abs(index - lastDesiredBase) <= 1) {
      if (reduceMotion) scheduleReducedRender()
      else if (!rafId) startRafIfNeeded()
    }

    resolve(frame)
    pumpQueue()
  }

  const fail = (err, aborted = false) => {
    settle()
    if (aborted || destroyed || gen !== loadGeneration) {
      resolve(null)
      if (!destroyed) pumpQueue()
      return
    }
    reject(err)
    pumpQueue()
  }

  const attemptFetch = async () => {
    try {
      const resp = await fetch(url, { signal: controller.signal })
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const blob = await resp.blob()
      if (controller.signal.aborted) throw new DOMException('Aborted', 'AbortError')

      if (typeof createImageBitmap === 'function') {
        const bitmap = await createImageBitmap(blob)
        finish(bitmap)
        return
      }

      const objectUrl = URL.createObjectURL(blob)
      const img = await decodeWithImage(objectUrl, true)
      finish(img)
    } catch (e) {
      if (e?.name === 'AbortError' || controller.signal.aborted) {
        fail(e, true)
        return
      }
      try {
        if (controller.signal.aborted) throw new DOMException('Aborted', 'AbortError')
        const img = await decodeWithImage(url)
        finish(img)
      } catch (err) {
        if (err?.name === 'AbortError' || controller.signal.aborted) {
          fail(err, true)
          return
        }
        fail(err)
      }
    }
  }

  attemptFetch()
}

// --- NAV helpers ---
const isFrameWindowReady = (targetFrame, radius = NAV_NEARBY_READY_RADIUS) => {
  const start = Math.max(0, targetFrame - radius)
  const end = Math.min(frameCount - 1, targetFrame + radius)
  for (let i = start; i <= end; i += 1) {
    if (!frameCache.has(i)) return false
  }
  return true
}

const ensureFramesAround = async (targetFrame, radius = NAV_PRELOAD_RADIUS) => {
  const start = Math.max(0, targetFrame - radius)
  const end = Math.min(frameCount - 1, targetFrame + radius)
  const targetPromise = loadFrame(targetFrame, { front: true, prio: -40 })
    .then((frame) => frame || null)
    .catch(() => null)

  // fire-and-forget остальное окно, чтобы не держать лоадер
  const extras = []
  for (let i = start; i <= end; i += 1) {
    if (i === targetFrame) continue
    extras.push(loadFrame(i).catch(() => null))
  }
  Promise.allSettled(extras).catch(() => {})

  const targetResult = await targetPromise
  return Boolean(targetResult)
}

// коридор: грузим “полосу” по направлению движения, чтобы не прыгать на nearby кадры
const ensureNavCorridor = async (fromFrameFloat, toFrame) => {
  const total = frameCount - 1
  const from = clamp(Math.floor(fromFrameFloat), 0, total)
  const to = clamp(Math.floor(toFrame), 0, total)
  const dir = to >= from ? 1 : -1
  const span = Math.abs(to - from)

  const forward = clamp(Math.floor(span * 0.25), NAV_CORRIDOR_FORWARD_MIN, NAV_CORRIDOR_FORWARD_MAX)
  const start = clamp(from - NAV_CORRIDOR_BACK, 0, total)
  const end = clamp(from + dir * forward, 0, total)

  // шаг можно увеличить на очень больших прыжках, чтобы не забить сеть
  const step = span > 700 ? 3 : span > 400 ? 2 : 1

  const tasks = []
  if (dir > 0) {
    for (let i = start; i <= end; i += step) {
      tasks.push(loadFrame(i, { prio: i === from ? -60 : null }).catch(() => null))
    }
  } else {
    for (let i = start; i >= end; i -= step) {
      tasks.push(loadFrame(i, { prio: i === from ? -60 : null }).catch(() => null))
    }
  }

  await Promise.allSettled(tasks)
}

const resolveNavTargetFrame = (sectionId) => {
  const raw = NAV_TO_FRAME[sectionId]
  if (typeof raw !== 'number' || Number.isNaN(raw)) return null
  // 0..118 -> 0..(frameCount-1)
  return Math.round((raw / NAV_MAX) * (frameCount - 1))
}

// --- drawing ---
// обычная рисовалка (со “nearby” фолбэком) — для scroll режима
const drawFrame = (frameFloat, { fast = false, stride = 1 } = {}) => {
  if (destroyed) return false
  const el = canvas.value
  if (!el) return false
  configureContext()
  if (!ctx) return false

  const total = frameCount - 1
  const desiredBase = clamp(Math.floor(frameFloat), 0, total)
  lastDesiredBase = desiredBase
  const mix = clamp(frameFloat - desiredBase, 0, 1)

  const baseEntry = findNearbyFrame(desiredBase)
  const baseImg = baseEntry?.frame || lastRenderedFrame
  const hasExactBase = Boolean(baseEntry && baseEntry.index === desiredBase)
  if (!baseImg) return false

  const allowMix = !lowQuality && !reduceMotion && !fast && stride === 1
  const canMix = allowMix && hasExactBase && mix > 0.001
  const nextImg = canMix ? frameCache.get(Math.min(total, desiredBase + 1)) : null
  const renderMix = nextImg ? mix : 0

  const baseIndexToRender =
    baseEntry && Number.isFinite(baseEntry.index)
      ? baseEntry.index
      : lastRenderedIndex !== -1
        ? lastRenderedIndex
        : desiredBase

  const unchanged =
    baseIndexToRender === lastDrawnIndex &&
    Math.abs(renderMix - lastDrawnMix) < 0.01 &&
    hasExactBase === lastDrawnHadExact &&
    baseImg === lastDrawnBaseRef &&
    (nextImg || null) === (lastDrawnNextRef || null)

  if (unchanged) return true

  const canvasWidth = el.width || 0
  const canvasHeight = el.height || 0
  if (!canvasWidth || !canvasHeight) return false

  const imgWidth = baseImg.naturalWidth || baseImg.width
  const imgHeight = baseImg.naturalHeight || baseImg.height
  if (!imgWidth || !imgHeight) return false

  const scale = Math.max(canvasWidth / imgWidth, canvasHeight / imgHeight)
  const drawWidth = imgWidth * scale
  const drawHeight = imgHeight * scale
  const offsetX = (canvasWidth - drawWidth) * 0.5
  const offsetY = (canvasHeight - drawHeight) * 0.5

  ctx.imageSmoothingEnabled = !(lowQuality || reduceMotion || fast)
  ctx.setTransform(1, 0, 0, 1, 0, 0)
  ctx.globalAlpha = 1
  ctx.drawImage(baseImg, offsetX, offsetY, drawWidth, drawHeight)

  if (nextImg && renderMix > 0.001) {
    ctx.globalAlpha = renderMix
    ctx.drawImage(nextImg, offsetX, offsetY, drawWidth, drawHeight)
    ctx.globalAlpha = 1
  }

  lastDrawnIndex = baseIndexToRender
  lastDrawnMix = renderMix
  lastDrawnHadExact = hasExactBase
  lastDrawnBaseRef = baseImg
  lastDrawnNextRef = nextImg

  lastRenderedFrame = baseImg
  lastRenderedIndex = baseIndexToRender

  return true
}

// строгая рисовалка (без nearby-fallback) — только для NAV твина, чтобы не было “рывков”
const drawFrameStrict = (frameFloat) => {
  if (destroyed) return false
  const el = canvas.value
  if (!el) return false
  configureContext()
  if (!ctx) return false

  const total = frameCount - 1
  const base = clamp(Math.floor(frameFloat), 0, total)
  const mix = clamp(frameFloat - base, 0, 1)

  const baseImg = frameCache.get(base)
  if (!baseImg) return false

  const allowMix = !lowQuality && !reduceMotion
  const nextImg = allowMix && mix > 0.001 ? frameCache.get(Math.min(total, base + 1)) : null
  const renderMix = nextImg ? mix : 0

  const canvasWidth = el.width || 0
  const canvasHeight = el.height || 0
  if (!canvasWidth || !canvasHeight) return false

  const imgWidth = baseImg.naturalWidth || baseImg.width
  const imgHeight = baseImg.naturalHeight || baseImg.height
  if (!imgWidth || !imgHeight) return false

  const scale = Math.max(canvasWidth / imgWidth, canvasHeight / imgHeight)
  const drawWidth = imgWidth * scale
  const drawHeight = imgHeight * scale
  const offsetX = (canvasWidth - drawWidth) * 0.5
  const offsetY = (canvasHeight - drawHeight) * 0.5

  ctx.imageSmoothingEnabled = !(lowQuality || reduceMotion)
  ctx.setTransform(1, 0, 0, 1, 0, 0)
  ctx.globalAlpha = 1
  ctx.drawImage(baseImg, offsetX, offsetY, drawWidth, drawHeight)

  if (nextImg && renderMix > 0.001) {
    ctx.globalAlpha = renderMix
    ctx.drawImage(nextImg, offsetX, offsetY, drawWidth, drawHeight)
    ctx.globalAlpha = 1
  }

  // обновим кэши “последнего нарисованного”, чтобы nav стартовал от факта
  lastDrawnIndex = base
  lastDrawnMix = renderMix
  lastRenderedFrame = baseImg
  lastRenderedIndex = base
  lastDrawnHadExact = true
  lastDrawnBaseRef = baseImg
  lastDrawnNextRef = nextImg || null

  return true
}

const updateQuality = (frameMs, progressDelta) => {
  if (reduceMotion) return
  const avg = recordFrameTime(frameMs)
  const badFrame = avg > FPS_DEGRADE_MS || progressDelta > FAST_SCROLL_DELTA

  if (badFrame) {
    badFpsStreak += 1
    goodFpsStreak = 0
    if (badFpsStreak >= 2) lowQuality = true
  } else if (avg < FPS_RECOVER_MS) {
    goodFpsStreak += 1
    if (goodFpsStreak >= GOOD_STREAK_TARGET) {
      lowQuality = false
      badFpsStreak = 0
    }
  } else {
    goodFpsStreak = 0
  }
}

// RAF tick (scroll mode)
const tick = () => {
  rafId = 0
  if (destroyed) return

  const now = performance.now()
  const frameMs = lastTickTs ? now - lastTickTs : 16.7
  const dt = clamp(frameMs / 16.67, 0.5, 2)
  lastTickTs = now

  const progressDelta = Math.abs(targetProgress.value - lastProgressForSpeed)
  lastProgressForSpeed = targetProgress.value
  const wasFast = fastScrollActive
  fastScrollActive = progressDelta > FAST_SCROLL_DELTA

  if (!fastScrollActive) fastExitStreak += 1
  else fastExitStreak = 0

  const delta = Math.abs(targetProgress.value - currentProgress)
  if (delta > SNAP_DELTA) {
    currentProgress = currentProgress + (targetProgress.value - currentProgress) * SNAP_LERP
  } else if (delta < SNAP_EPS) {
    currentProgress = targetProgress.value
  } else {
    const t = clamp((delta - 0.01) / 0.3, 0, 1)
    let ease = MIN_EASE + (MAX_EASE - MIN_EASE) * t
    if (fastScrollActive) ease = Math.min(MAX_EASE + EASE_FAST_BONUS, ease + EASE_FAST_BONUS)
    const blendedEase = 1 - Math.pow(1 - ease, dt)
    currentProgress += (targetProgress.value - currentProgress) * blendedEase
  }

  if (targetProgress.value === 0) currentProgress = 0
  if (targetProgress.value === 1) currentProgress = 1

  const mappedFrame = mapProgressToFrame(currentProgress)
  const rawFrameFloat = clamp(mappedFrame, 0, frameCount - 1)

  const direction = targetProgress.value >= currentProgress ? 1 : -1
  const stride = getDynamicStride(fastScrollActive)

  const rawBaseIndex = Math.floor(rawFrameFloat)
  const quantBase = stride > 1 ? clamp(Math.round(rawBaseIndex / stride) * stride, 0, frameCount - 1) : rawBaseIndex

  maybeReprioritizeOnJump(quantBase, direction)

  const fast = fastScrollActive
  const drawFloat = fast && stride > 1 ? quantBase : rawFrameFloat
  const frameToDraw = applyMobileFrameStep(drawFloat)
  const windowBase = isMobile() ? Math.floor(frameToDraw) : quantBase

  ensureWindow(windowBase, direction, fast)
  pruneCache(windowBase)

  const drew = drawFrame(frameToDraw, { fast, stride })

  updateQuality(frameMs, progressDelta)

  if (wasFast && !fastScrollActive && fastExitStreak >= FAST_EXIT_STREAK) {
    const recoveryBase = isMobile() ? Math.floor(frameToDraw) : rawBaseIndex
    loadGeneration += 1
    abortFarLoadsAndClearQueue(recoveryBase, direction, false)
    ensureWindow(recoveryBase, direction, false)
    pumpQueue()
  }

  const progressGap = Math.abs(targetProgress.value - currentProgress)
  const waitingForFrames = pending.size > 0 || activeLoads > 0 || queued.size > 0

  if (drew) noDrawFrameStreak = 0
  else if (progressGap > SNAP_EPS || waitingForFrames) noDrawFrameStreak += 1

  const allowRetry = noDrawFrameStreak < MAX_NO_DRAW_FRAMES
  const shouldContinue =
    (!destroyed && progressGap > SNAP_EPS && (drew || allowRetry)) ||
    (!destroyed && waitingForFrames && allowRetry)

  if (shouldContinue) rafId = window.requestAnimationFrame(tick)
}

const renderReducedFrame = () => {
  rafId = 0
  if (destroyed) return
  syncScrollState()
  currentProgress = targetProgress.value
  const mappedFrame = mapProgressToFrame(currentProgress)
  const frameFloat = clamp(mappedFrame, 0, frameCount - 1)
  const frameToRender = applyMobileFrameStep(frameFloat)
  const baseIndex = Math.floor(frameToRender)
  ensureWindow(baseIndex, 1, false)
  pruneCache(baseIndex)
  drawFrame(frameToRender, { fast: false, stride: 1 })
}

const scheduleReducedRender = () => {
  if (destroyed) return
  if (rafId) return
  rafId = window.requestAnimationFrame(renderReducedFrame)
}

const startRafIfNeeded = () => {
  if (destroyed) return
  if (reduceMotion) {
    scheduleReducedRender()
    return
  }
  if (rafId) return
  rafId = window.requestAnimationFrame(tick)
}

const renderWithMobileStep = () => {
  if (destroyed) return
  syncScrollState()
  currentProgress = targetProgress.value
  const mappedFrame = mapProgressToFrame(currentProgress)
  const frameFloat = clamp(mappedFrame, 0, frameCount - 1)
  const frameToRender = applyMobileFrameStep(frameFloat)
  const baseIndex = Math.floor(frameToRender)
  ensureWindow(baseIndex, 1, false)
  pruneCache(baseIndex)
  drawFrame(frameToRender, { fast: false, stride: 1 })
}

const handleMobileModeChange = () => {
  renderWithMobileStep()
  if (!reduceMotion) startRafIfNeeded()
}

const stopRaf = () => {
  if (!rafId) return
  window.cancelAnimationFrame(rafId)
  rafId = 0
}

// IMPORTANT: ignore scroll-driven updates while nav animation is active
const onScroll = () => {
  if (destroyed || isNavAnimating) return
  syncScrollState()
  startRafIfNeeded()
}

const onVisibilityChange = () => {
  if (destroyed) return
  if (document.hidden) {
    stopRaf()
    return
  }
  syncScrollState()
  startRafIfNeeded()
}

const refreshLayout = () => {
  if (destroyed) return
  rebuildKeyframes()
  syncScrollState()
  const currentFrame = lastDrawnIndex === -1 ? 0 : lastDrawnIndex + lastDrawnMix
  const frameToRender = applyMobileFrameStep(currentFrame)
  drawFrame(frameToRender, { fast: false, stride: 1 })
  if (!reduceMotion) startRafIfNeeded()
}

const scheduleLayoutRefresh = () => {
  if (destroyed || layoutObserverId) return

  const now = performance.now()
  const sinceLast = now - lastLayoutRefreshTs
  if (sinceLast < LAYOUT_THROTTLE_MS) {
    if (!layoutThrottleTimeout) {
      layoutThrottleTimeout = window.setTimeout(() => {
        layoutThrottleTimeout = 0
        scheduleLayoutRefresh()
      }, Math.max(0, LAYOUT_THROTTLE_MS - sinceLast))
    }
    return
  }

  layoutObserverId = window.requestAnimationFrame(() => {
    layoutObserverId = 0
    lastLayoutRefreshTs = performance.now()
    refreshLayout()
  })
}

const onResize = () => {
  if (destroyed) return
  if (resizeId) window.cancelAnimationFrame(resizeId)
  resizeId = window.requestAnimationFrame(() => {
    resizeCanvas()
    scheduleLayoutRefresh()
  })
}

const setupLayoutObserver = () => {
  if (typeof ResizeObserver === 'undefined') return
  const observer = new ResizeObserver(() => scheduleLayoutRefresh())
  observer.observe(document.documentElement)
  observer.observe(document.body)
  layoutObserver = observer
}

const normalizeSectionId = (value = '') => value.replace(/^#/, '').trim() || 'top'

const scrollSectionIntoView = (hash, sectionId) =>
  new Promise((resolve) => {
    const domId = NAV_TO_DOM_ID[sectionId] || sectionId
    const target =
      (hash ? document.querySelector(hash) : null) ||
      document.getElementById(domId) ||
      document.querySelector(`#${domId}`)

    if (!target) {
      resolve()
      return
    }

    const headerEl = document.querySelector('.header')
    const offset = (headerEl?.offsetHeight || 80) + 10
    const start = window.scrollY || window.pageYOffset || 0
    const end = target.getBoundingClientRect().top + start - offset
    const duration = 900
    const started = performance.now()

    const step = (ts) => {
      const t = clamp((ts - started) / duration, 0, 1)
      const eased = easeInOutCubic(t)
      const next = start + (end - start) * eased
      window.scrollTo(0, next)
      if (t < 1) {
        window.requestAnimationFrame(step)
      } else {
        if (hash) window.history.replaceState(null, '', hash)
        resolve()
      }
    }

    window.requestAnimationFrame(step)
  })

/**
 * NAV tween:
 * - does NOT touch targetProgress/currentProgress (scroll model must stay consistent)
 * - draws only if required frames are ready (strict)
 * - keeps loading corridor while tweening
 */
const tweenFrameToNav = (targetFrame, durationMs = NAV_TWEEN_DURATION, currentGen) =>
  new Promise((resolve) => {
    if (destroyed || currentGen !== navGen) return resolve()

    if (navTweenId) cancelAnimationFrame(navTweenId)
    stopRaf()

    const total = frameCount - 1
    const fromFrame = applyMobileFrameStep(
      clamp(lastDrawnIndex === -1 ? mapProgressToFrame(currentProgress) : lastDrawnIndex + lastDrawnMix, 0, total)
    )
    const toFrame = applyMobileFrameStep(clamp(targetFrame, 0, total))
    const direction = toFrame >= fromFrame ? 1 : -1
    const startTs = performance.now()

    const step = (ts) => {
      if (destroyed || currentGen !== navGen) {
        navTweenId = 0
        return resolve()
      }

      const t = clamp((ts - startTs) / durationMs, 0, 1)
      const eased = easeInOutCubic(t)
      const frameFloat = fromFrame + (toFrame - fromFrame) * eased
      const frameToRender = applyMobileFrameStep(frameFloat)
      const baseIndex = Math.floor(frameToRender)

      ensureWindow(baseIndex, direction, false)
      pruneCache(baseIndex)

      // strict draw: if missing frames, do NOT jump to nearby
      const drew = drawFrameStrict(frameToRender)

      // if we couldn't draw (frames not ready), keep trying; loader is already hidden,
      // but frames are being fetched; we still resolve at time end.
      if (t < 1) {
        navTweenId = requestAnimationFrame(step)
      } else {
        navTweenId = 0
        // final: try to draw exact target once more (best effort)
        drawFrameStrict(applyMobileFrameStep(toFrame))
        resolve(drew)
      }
    }

    navTweenId = requestAnimationFrame(step)
  })

const handleNavNavigate = async (event) => {
  const detail = event?.detail || {}
  const sectionId = normalizeSectionId(detail.sectionId || detail.hash || '')
  const targetFrameRaw = resolveNavTargetFrame(sectionId)
  if (typeof targetFrameRaw !== 'number') return
  const targetFrame = applyMobileFrameStep(targetFrameRaw)

  event?.preventDefault?.()

  const currentGen = ++navGen

  // всегда сбрасываем лоадер на старте (лечит “залипания” при быстрых кликах)
  navLoading.value = false

  // cancel any running tween
  if (navTweenId) {
    cancelAnimationFrame(navTweenId)
    navTweenId = 0
  }

  // enter nav mode: stop scroll-driven changes
  isNavAnimating = true

  // reprioritize loaders towards target
  loadGeneration += 1
  const fromFrameFloat = applyMobileFrameStep(
    clamp(lastDrawnIndex === -1 ? mapProgressToFrame(currentProgress) : lastDrawnIndex + lastDrawnMix, 0, frameCount - 1)
  )
  const dir = targetFrame >= fromFrameFloat ? 1 : -1
  abortFarLoadsAndClearQueue(Math.floor(targetFrame), dir, false)
  pumpQueue()

  // show loader only if we are not ready
  const needsLoader = !isFrameWindowReady(targetFrame, NAV_NEARBY_READY_RADIUS)
  if (needsLoader) navLoading.value = true

  let ready = false
  try {
    // 1) гарантируем точку назначения (+окрестность)
    const okTarget = await ensureFramesAround(targetFrame, NAV_PRELOAD_RADIUS)
    if (currentGen !== navGen) return

    // 2) грузим коридор от текущего кадра в сторону движения — резко снижает “дёрганье”
    await ensureNavCorridor(fromFrameFloat, targetFrame)
    if (currentGen !== navGen) return

    // 3) ещё раз проверяем цель (на случай, если сеть отвалилась)
    ready = okTarget && frameCache.has(targetFrame)
  } catch (err) {
    console.error('Failed to preload nav frames', err)
  } finally {
    if (currentGen === navGen) navLoading.value = false
  }

  if (currentGen !== navGen) return

  if (!ready) {
    // exit nav mode safely
    isNavAnimating = false
    syncScrollState()
    startRafIfNeeded()
    return
  }

  // reduced motion: no “cinema” tween
  if (reduceMotion) {
    drawFrameStrict(targetFrame)
    await scrollSectionIntoView(detail.hash, sectionId)
    if (currentGen !== navGen) return
    isNavAnimating = false
    syncScrollState()
    startRafIfNeeded()
    return
  }

  try {
    await tweenFrameToNav(targetFrame, NAV_TWEEN_DURATION, currentGen)
  } catch (err) {
    console.error('Failed to tween to nav frame', err)
  }

  if (currentGen !== navGen) return

  await scrollSectionIntoView(detail.hash, sectionId)

  if (currentGen !== navGen) return

  // exit nav mode: resync with real scroll model
  isNavAnimating = false
  syncScrollState()
  startRafIfNeeded()
}

onMounted(() => {
  const ua = navigator.userAgent || ''
  isTouchDevice = window.matchMedia('(pointer:coarse)').matches || /Android|iPhone|iPad|iPod/i.test(ua)
  isSafari = /^((?!chrome|android).)*safari/i.test(ua)
  reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  clearStaticBackground()
  resizeCanvas()
  rebuildKeyframes()
  syncScrollState()

  // warmup: first frames
  loadFrame(0, { front: true, prio: -80 })
    .then(() => {
      drawFrame(0, { fast: false, stride: 1 })
      ensureWindow(0, 1, false)
      return Promise.all([loadFrame(1), loadFrame(2), loadFrame(3)].map((p) => p.catch(() => {})))
    })
    .catch(() => {})
    .finally(() => {
      startRafIfNeeded()
    })

  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onResize, { passive: true })
  window.addEventListener('orientationchange', handleMobileModeChange)
  if (mqMobile?.addEventListener) mqMobile.addEventListener('change', handleMobileModeChange)
  else if (mqMobile?.addListener) mqMobile.addListener(handleMobileModeChange)
  document.addEventListener('visibilitychange', onVisibilityChange)

  // NAV channel
  window.addEventListener('scroll-bg:navigate', handleNavNavigate, false)

  setupLayoutObserver()
})

onBeforeUnmount(() => {
  destroyed = true

  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('orientationchange', handleMobileModeChange)
  if (mqMobile?.removeEventListener) mqMobile.removeEventListener('change', handleMobileModeChange)
  else if (mqMobile?.removeListener) mqMobile.removeListener(handleMobileModeChange)
  document.removeEventListener('visibilitychange', onVisibilityChange)
  window.removeEventListener('scroll-bg:navigate', handleNavNavigate, false)

  if (layoutObserver) layoutObserver.disconnect()
  if (layoutObserverId) window.cancelAnimationFrame(layoutObserverId)
  if (layoutThrottleTimeout) {
    clearTimeout(layoutThrottleTimeout)
    layoutThrottleTimeout = 0
  }

  if (rafId) window.cancelAnimationFrame(rafId)
  if (resizeId) window.cancelAnimationFrame(resizeId)
  if (navTweenId) window.cancelAnimationFrame(navTweenId)

  for (const controller of abortControllers.values()) controller.abort()
  abortControllers.clear()

  pending.clear()
  queued.clear()
  loadQueue.length = 0
  activeLoads = 0

  for (const frame of frameCache.values()) {
    if (frame && typeof frame.close === 'function') frame.close()
  }
  frameCache.clear()

  if (lastRenderedFrame && typeof lastRenderedFrame.close === 'function') {
    lastRenderedFrame.close()
  }
  lastRenderedFrame = null

  if (cleanupBg) cleanupBg()
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
