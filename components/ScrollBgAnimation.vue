<template>
  <section ref="wrapper" class="scroll-bg-wrapper">
    <div class="scroll-bg-sticky" :style="{ backgroundImage: `url('${currentSrc}')` }" />
  </section>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const frameCount = 91
const firstAnimatedFrame = 2
const wrapper = ref(null)
const currentSrc = ref('/bg/ezgif-frame-001.png')

const pad = (n) => String(n).padStart(3, '0')
const frameSrc = (i) => `/bg/ezgif-frame-${pad(i)}.png`

let images = []
let rafId = 0
let ticking = false
let latestScrollY = 0

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
  if (!wrapper.value) return

  const rect = wrapper.value.getBoundingClientRect()
  const scrollTop = latestScrollY
  const wrapperTop = scrollTop + rect.top
  const wrapperHeight = rect.height
  const viewportHeight = window.innerHeight
  const maxScroll = Math.max(1, wrapperHeight - viewportHeight)
  const progress = Math.min(1, Math.max(0, (scrollTop - wrapperTop) / maxScroll))
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
    currentSrc.value = nextSrc
  }
}

const onScroll = () => {
  latestScrollY = window.scrollY || window.pageYOffset
  if (!ticking) {
    ticking = true
    rafId = window.requestAnimationFrame(updateFrame)
  }
}

const onResize = () => {
  onScroll()
}

onMounted(() => {
  preloadFrames()
  latestScrollY = window.scrollY || window.pageYOffset
  updateFrame()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onResize, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onResize)
  if (rafId) window.cancelAnimationFrame(rafId)
})
</script>

<style scoped>
.scroll-bg-wrapper {
  position: relative;
  width: 100vw;
  height: 220vh;
  z-index: 0;
}

.scroll-bg-sticky {
  position: sticky;
  top: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  will-change: background-image;
}

.scroll-bg-sticky::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(120% 120% at 50% 0%, rgba(0, 0, 0, 0.08), rgba(0, 0, 0, 0.35));
  pointer-events: none;
}
</style>
