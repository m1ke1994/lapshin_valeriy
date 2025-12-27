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

const frameCount = 91
const firstAnimatedFrame = 2
const scrollSpeed = 1.6
const wrapper = ref(null)
const currentSrc = ref('/bg/ezgif-frame-001.png')
const previousSrc = ref('')
const showPrevious = ref(false)

const pad = (n) => String(n).padStart(3, '0')
const frameSrc = (i) => `/bg/ezgif-frame-${pad(i)}.png`

let images = []
let rafId = 0
let ticking = false
let latestScrollY = 0

const getScrollElement = () => document.scrollingElement || document.documentElement

const preloadFrames = () => {
  images = new Array(frameCount)
  for (let i = 1; i <= frameCount; i += 1) {
    const img = new Image()
    img.src = frameSrc(i)
    images[i - 1] = img
  }
}

const updateFrame = () => {
  ticking = false
  const scrollTop = latestScrollY
  const scrollEl = getScrollElement()
  const maxScroll = Math.max(1, scrollEl.scrollHeight - window.innerHeight)
  const progress = Math.min(1, Math.max(0, (scrollTop / maxScroll) * scrollSpeed))
  let nextFrame = 1

  if (progress > 0) {
    const animatedRange = frameCount - firstAnimatedFrame
    const animatedIndex = Math.min(
      animatedRange,
      Math.floor(progress * (animatedRange + 1))
    )
    nextFrame = Math.min(frameCount, firstAnimatedFrame + animatedIndex)
  }

  const nextSrc = frameSrc(nextFrame)

  if (currentSrc.value !== nextSrc) {
    previousSrc.value = currentSrc.value
    showPrevious.value = true
    currentSrc.value = nextSrc
    requestAnimationFrame(() => {
      showPrevious.value = false
    })
  }
}

const onScroll = () => {
  const scrollEl = getScrollElement()
  latestScrollY = scrollEl.scrollTop || window.scrollY || window.pageYOffset || 0
  if (!ticking) {
    ticking = true
    rafId = window.requestAnimationFrame(updateFrame)
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
  updateFrame()
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
  position: relative;
  width: 100vw;
  height: 500vh;
  z-index: 0;
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
  transition: opacity 0.45s ease;
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
