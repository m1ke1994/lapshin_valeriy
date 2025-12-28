<template>
  <section ref="section" class="scroll-wrapper" aria-hidden="true">
    <div class="pin">
      <canvas ref="canvas"></canvas>
    </div>
  </section>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const section = ref(null)
const canvas = ref(null)

const totalAvailableFrames = 1546
const framesToUse = 120
const frameStep = Math.max(1, Math.floor(totalAvailableFrames / framesToUse))
const framePath = (idx) => {
  const frameIndex = Math.min(totalAvailableFrames, 1 + idx * frameStep)
  return `/bg/frame_${String(frameIndex).padStart(5, '0')}.jpg`
}

const frameCount = framesToUse
const frames = new Array(frameCount)

const MIN_EASE = 0.045
const MAX_EASE = 0.12

const anchorConfig = [
  { id: 'top', frame: 0 },
  { id: 'values', frame: 16 },
  { id: 'approach', frame: 32 },
  { id: 'competencies', frame: 52 },
  { id: 'trust', frame: 72 },
  { id: 'projects', frame: 96 },
  { id: 'contacts', frame: 118 },
]
let keyframes = []

const targetProgress = ref(0)
let currentProgress = 0
let rafId = 0
let resizeId = 0
let lastFrameIndex = -1
let lastFrameMix = 0
let isReady = false
let cleanupBg = null

const clamp = (value, min, max) => Math.min(max, Math.max(min, value))

const preloadImages = () => {
  const loaders = Array.from({ length: frameCount }, (_, index) =>
    new Promise((resolve) => {
      const img = new Image()
      img.decoding = 'async'
      img.loading = 'eager'
      img.src = framePath(index)
      img.onload = () => resolve(img)
      img.onerror = () => resolve(img)
    })
  )

  return Promise.all(loaders).then((loaded) => {
    loaded.forEach((img, index) => {
      frames[index] = img
    })
    isReady = true
  })
}

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

const getScrollProgress = () => {
  const scrollTop = window.scrollY || window.pageYOffset || 0
  const doc = document.documentElement
  const body = document.body
  const fullHeight = Math.max(
    body.scrollHeight,
    body.offsetHeight,
    doc.clientHeight,
    doc.scrollHeight,
    doc.offsetHeight
  )
  const maxScroll = Math.max(1, fullHeight - window.innerHeight)
  return clamp(scrollTop / maxScroll, 0, 1)
}

const rebuildKeyframes = () => {
  if (typeof window === 'undefined') return
  const doc = document.documentElement
  const body = document.body
  const fullHeight = Math.max(
    body.scrollHeight,
    body.offsetHeight,
    doc.clientHeight,
    doc.scrollHeight,
    doc.offsetHeight
  )
  const maxScroll = Math.max(1, fullHeight - window.innerHeight)

  const anchors = anchorConfig
    .map((item) => {
      const el = document.getElementById(item.id)
      if (!el) return null
      const top = (window.scrollY || window.pageYOffset || 0) + el.getBoundingClientRect().top
      const p = clamp(top / maxScroll, 0, 1)
      return { p, frame: clamp(item.frame, 0, frameCount - 1) }
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

const updateTarget = () => {
  targetProgress.value = getScrollProgress()
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
    lastFrameIndex = -1
  }
}

const drawFrame = (frameFloat) => {
  if (!isReady) return
  const el = canvas.value
  if (!el) return

  const ctx = el.getContext('2d')
  if (!ctx) return

  const total = frames.length - 1
  const baseIndex = clamp(Math.floor(frameFloat), 0, total)
  const mix = clamp(frameFloat - baseIndex, 0, 1)
  const nextIndex = Math.min(total, baseIndex + 1)

  const baseImg = frames[baseIndex]
  const nextImg = frames[nextIndex]
  if (!baseImg) return

  const canvasWidth = el.width
  const canvasHeight = el.height

  const imgWidth = baseImg.naturalWidth || baseImg.width
  const imgHeight = baseImg.naturalHeight || baseImg.height
  if (!imgWidth || !imgHeight) return

  const scale = Math.max(canvasWidth / imgWidth, canvasHeight / imgHeight)
  const drawWidth = imgWidth * scale
  const drawHeight = imgHeight * scale
  const offsetX = (canvasWidth - drawWidth) * 0.5
  const offsetY = (canvasHeight - drawHeight) * 0.5

  ctx.clearRect(0, 0, canvasWidth, canvasHeight)
  ctx.imageSmoothingEnabled = true
  ctx.drawImage(baseImg, offsetX, offsetY, drawWidth, drawHeight)

  if (nextImg && mix > 0.001) {
    ctx.globalAlpha = mix
    ctx.drawImage(nextImg, offsetX, offsetY, drawWidth, drawHeight)
    ctx.globalAlpha = 1
  }
}

const tick = () => {
  const delta = Math.abs(targetProgress.value - currentProgress)
  const t = clamp((delta - 0.015) / 0.25, 0, 1)
  const ease = MIN_EASE + (MAX_EASE - MIN_EASE) * t
  currentProgress += (targetProgress.value - currentProgress) * ease
  const mappedFrame = mapProgressToFrame(currentProgress)
  const frameFloat = clamp(mappedFrame, 0, frames.length - 1)
  const baseIndex = Math.floor(frameFloat)
  const mix = Math.round((frameFloat - baseIndex) * 1000) / 1000

  if (baseIndex !== lastFrameIndex || Math.abs(mix - lastFrameMix) > 0.01) {
    lastFrameIndex = baseIndex
    lastFrameMix = mix
    drawFrame(frameFloat)
  }

  rafId = window.requestAnimationFrame(tick)
}

const onResize = () => {
  if (resizeId) window.cancelAnimationFrame(resizeId)
  resizeId = window.requestAnimationFrame(() => {
    resizeCanvas()
    rebuildKeyframes()
    const currentFrame = lastFrameIndex === -1 ? 0 : lastFrameIndex + lastFrameMix
    drawFrame(currentFrame)
    updateTarget()
  })
}

onMounted(() => {
  if (typeof window === 'undefined') return

  clearStaticBackground()
  resizeCanvas()
  rebuildKeyframes()
  updateTarget()

  preloadImages().then(() => {
    drawFrame(0)
    tick()
  })

  window.addEventListener('scroll', updateTarget, { passive: true })
  window.addEventListener('resize', onResize, { passive: true })
})

onBeforeUnmount(() => {
  if (typeof window === 'undefined') return

  window.removeEventListener('scroll', updateTarget)
  window.removeEventListener('resize', onResize)

  if (rafId) window.cancelAnimationFrame(rafId)
  if (resizeId) window.cancelAnimationFrame(resizeId)
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
</style>
