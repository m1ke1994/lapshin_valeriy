<template>
  <section class="hero" id="top">
    <div :class="['section-inner hero-inner reveal hero-animate', { 'is-visible': isHeroVisible }]">
      <div class="hero-copy glass-card">
        <p class="eyebrow">{{ copy.eyebrow }}</p>

        <h1>{{ copy.title }}</h1>

        <p class="lead">{{ copy.lead }}</p>

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
          <h3>{{ note.title }}</h3>
          <p>{{ note.body }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useLocale } from '~/composables/useLocale'

const { t } = useLocale()
const copy = computed(() => t.value.hero)

const isHeroVisible = ref(false)

onMounted(() => {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      isHeroVisible.value = true
    })
  })
})
</script>
