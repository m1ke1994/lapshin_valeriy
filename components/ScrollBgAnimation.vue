<template>
  <section ref="wrapper" class="scroll-bg-wrapper" aria-hidden="true">
    <img
      class="scroll-bg-sticky"
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

const setRootBackground = (src) => {
  if (typeof document === 'undefined') return
  const value = `url('${src}')`
  document.documentElement.style.setProperty('--scroll-bg-image', value)
  document.body.style.backgroundImage = value
}

onMounted(() => {
  preloadFrames()
  latestScrollY = window.scrollY || window.pageYOffset
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
}
</style>
