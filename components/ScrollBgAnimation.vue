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
const framesToUse = 81
const frameStep = Math.max(1, Math.floor(totalAvailableFrames / framesToUse))
const framePath = (idx) => {
  const frameIndex = Math.min(totalAvailableFrames, 1 + idx * frameStep)
  return `/bg/frame_${String(frameIndex).padStart(5, '0')}.jpg`
}

const frameCount = framesToUse
const frames = new Array(frameCount)

const targetProgress = ref(0)
let currentProgress = 0
let rafId = 0
let resizeId = 0
let lastFrameIndex = -1
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

const drawFrame = (frameIndex) => {
  if (!isReady) return
  const el = canvas.value
  if (!el) return

  const ctx = el.getContext('2d')
  if (!ctx) return

  const img = frames[frameIndex]
  if (!img) return

  const canvasWidth = el.width
  const canvasHeight = el.height

  const imgWidth = img.naturalWidth || img.width
  const imgHeight = img.naturalHeight || img.height
  if (!imgWidth || !imgHeight) return

  const scale = Math.max(canvasWidth / imgWidth, canvasHeight / imgHeight)
  const drawWidth = imgWidth * scale
  const drawHeight = imgHeight * scale
  const offsetX = (canvasWidth - drawWidth) * 0.5
  const offsetY = (canvasHeight - drawHeight) * 0.5

  ctx.clearRect(0, 0, canvasWidth, canvasHeight)
  ctx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight)
}

const tick = () => {
  const delta = Math.abs(targetProgress.value - currentProgress)
  const t = clamp((delta - 0.02) / 0.2, 0, 1)
  const ease = 0.07 + (0.18 - 0.07) * t
  currentProgress += (targetProgress.value - currentProgress) * ease
  const frameIndex = Math.round(currentProgress * (frames.length - 1))

  if (frameIndex !== lastFrameIndex) {
    lastFrameIndex = frameIndex
    drawFrame(frameIndex)
  }

  rafId = window.requestAnimationFrame(tick)
}

const onResize = () => {
  if (resizeId) window.cancelAnimationFrame(resizeId)
  resizeId = window.requestAnimationFrame(() => {
    resizeCanvas()
    drawFrame(lastFrameIndex === -1 ? 0 : lastFrameIndex)
    updateTarget()
  })
}

onMounted(() => {
  if (typeof window === 'undefined') return

  clearStaticBackground()
  resizeCanvas()
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
