<template>
  <section class="hero" id="top">
    <div :class="['section-inner hero-inner reveal hero-animate', { 'is-visible': isHeroVisible }]">
      <div class="hero-copy glass-card">
        <p class="eyebrow">{{ copy.eyebrow }}</p>

        <h1 v-html="highlight(copy.title)"></h1>

        <p class="lead" v-html="highlight(copy.lead)"></p>

        <div class="hero-actions">
          <a class="btn btn-primary" href="#contacts">{{ copy.ctas.primary }}</a>
          <a class="btn btn-ghost" href="#projects">{{ copy.ctas.secondary }}</a>
        </div>

        <div class="hero-metrics">
          <div v-for="metric in copy.metrics" :key="metric.value" class="metric">
            <span class="metric-value">{{ metric.value }}</span>
            <span class="metric-label">{{ metric.label }}</span>
          </div>
        </div>
      </div>

      <div class="hero-aside">
        <div v-for="note in copy.notes" :key="note.title" class="glass-card hero-note">
          <h3 v-html="highlight(note.title)"></h3>
          <p v-html="highlight(note.body)"></p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useLocale } from '~/composables/useLocale'
import { useHighlight } from '~/composables/useHighlight'

const { t } = useLocale()
const copy = computed(() => t.value.hero)
const { highlight } = useHighlight()

const isHeroVisible = ref(false)

onMounted(() => {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      isHeroVisible.value = true
    })
  })
})
</script>
