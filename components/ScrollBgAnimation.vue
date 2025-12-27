<template>
  <section ref="wrapper" class="scroll-bg-wrapper" aria-hidden="true">
    <img
      class="scroll-bg-sticky scroll-bg-previous"
      :class="{ 'is-visible': showPrevious }"
      :src="previousSrc || currentSrc"
      alt=""
      role="presentation"
      aria-hidden="true"
      decoding="async"
    />
    <img
      class="scroll-bg-sticky scroll-bg-current"
      :src="currentSrc"
      alt=""
      role="presentation"
      aria-hidden="true"
      decoding="async"
    />
  </section>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'

const frameCount = 81
const firstAnimatedFrame = 1
const scrollSpeed = 1
const smoothFactor = 0.06
const wrapper = ref(null)
const previousSrc = ref('')
const showPrevious = ref(false)

const pad = (n) => String(n).padStart(3, '0')
const frameSrc = (i) => encodeURI(`/bg/img (${i}).webp`)
const currentSrc = ref(frameSrc(1))

let images = []
let rafId = 0
let latestScrollY = 0
let targetFrame = firstAnimatedFrame
let currentFrame = firstAnimatedFrame
let animating = false

const getScrollElement = () => document.scrollingElement || document.documentElement

const preloadFrames = () => {
  images = new Array(frameCount)
  for (let i = 1; i <= frameCount; i += 1) {
    const img = new Image()
    img.src = frameSrc(i)
    images[i - 1] = img
  }
}

const clamp = (value, min, max) => Math.min(max, Math.max(min, value))

const renderFrame = () => {
  const scrollTop = latestScrollY
  const scrollEl = getScrollElement()
  const maxScroll = Math.max(1, scrollEl.scrollHeight - window.innerHeight)
  const progress = clamp((scrollTop / maxScroll) * scrollSpeed, 0, 1)
  const animatedRange = frameCount - firstAnimatedFrame

  targetFrame = firstAnimatedFrame + progress * animatedRange

  const delta = targetFrame - currentFrame
  if (Math.abs(delta) < 0.01) {
    currentFrame = targetFrame
    animating = false
  } else {
    currentFrame += delta * smoothFactor
  }

  const nextFrame = clamp(Math.round(currentFrame), 1, frameCount)

  const nextSrc = frameSrc(nextFrame)

  if (currentSrc.value !== nextSrc) {
    previousSrc.value = currentSrc.value
    showPrevious.value = true
    currentSrc.value = nextSrc
    requestAnimationFrame(() => {
      showPrevious.value = false
    })
  }

  if (animating) {
    rafId = window.requestAnimationFrame(renderFrame)
  } else {
    rafId = 0
  }
}

const onScroll = () => {
  const scrollEl = getScrollElement()
  latestScrollY = scrollEl.scrollTop || window.scrollY || window.pageYOffset || 0
  if (!animating) {
    animating = true
    rafId = window.requestAnimationFrame(renderFrame)
  }
}

const onResize = () => {
  onScroll()
}

const setRootBackground = (src) => {
  if (typeof document === 'undefined') return
  const value = `url('${src}')`
  document.documentElement.style.setProperty('--scroll-bg-image', value)
  document.body.style.backgroundImage = value
}

onMounted(() => {
  preloadFrames()
  onScroll()
  renderFrame()
  setRootBackground(currentSrc.value)
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onResize, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onResize)
  if (rafId) window.cancelAnimationFrame(rafId)
})

watch(currentSrc, (src) => {
  setRootBackground(src)
})
</script>

<style scoped>
.scroll-bg-wrapper {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
}

.scroll-bg-sticky {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  object-fit: cover;
  object-position: center;
  pointer-events: none;
  background: transparent;
  transition: opacity 0.7s ease;
  will-change: opacity;
}

.scroll-bg-previous {
  opacity: 0;
}

.scroll-bg-previous.is-visible {
  opacity: 1;
}

.scroll-bg-current {
  opacity: 1;
}
</style>
