import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'

/**
 * v-reveal-section
 * Навесьте на <section class="reveal-section" v-reveal-section>
 * Направление анимации циклами: left, right, bottom, top.
 * Опции (необязательные): v-reveal-section="{ repeat: true, distance: 60, duration: 0.8 }"
 */
export default defineNuxtPlugin((nuxtApp) => {
  if (process.server) return

  gsap.registerPlugin(ScrollTrigger)

  const directions = [
    { axis: 'x', sign: -1 }, // left
    { axis: 'x', sign: 1 }, // right
    { axis: 'y', sign: 1 }, // bottom -> up
    { axis: 'y', sign: -1 }, // top -> down
  ]

  let revealIndex = 0

  const directive = {
    mounted(el: HTMLElement, binding: { value?: { repeat?: boolean; distance?: number; duration?: number } }) {
      const repeat = Boolean(binding?.value?.repeat)
      const prefersReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
      if (prefersReduce) {
        gsap.set(el, { opacity: 1, clearProps: 'opacity,transform' })
        return
      }

      const dir = directions[revealIndex % directions.length]
      revealIndex += 1

      const isMobile = window.matchMedia('(max-width: 720px)').matches
      const distance = binding?.value?.distance ?? (isMobile ? 32 : 64)
      const duration = binding?.value?.duration ?? (isMobile ? 0.7 : 0.9)

      const fromVars: gsap.TweenVars = {
        opacity: 0,
        [dir.axis]: dir.sign * distance,
      }

      const toVars: gsap.TweenVars = {
        opacity: 1,
        [dir.axis]: 0,
        duration,
        ease: 'power2.out',
        clearProps: 'opacity,transform',
        overwrite: true,
        scrollTrigger: {
          trigger: el,
          start: 'top 80%',
          once: !repeat,
          toggleActions: repeat ? 'play none none reverse' : 'play none none none',
        },
      }

      gsap.set(el, fromVars)
      gsap.to(el, toVars)
    },
  }

  nuxtApp.vueApp.directive('reveal-section', directive)

  // Обновить триггеры после полной загрузки
  requestAnimationFrame(() => {
    ScrollTrigger.refresh()
  })
})
