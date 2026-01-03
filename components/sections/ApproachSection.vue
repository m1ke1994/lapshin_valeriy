<template>
  <section id="approach" class="section">
    <div class="section-inner reveal">
      <div class="section-head">
        <p class="eyebrow">{{ copy.eyebrow }}</p>
        <h2>{{ copy.title }}</h2>
        <p class="lead">{{ copy.lead }}</p>
      </div>
      <div class="steps-grid">
        <div v-for="(step, index) in copy.steps" :key="step.title" class="glass-card step-card">
          <span class="step-index">{{ String(index + 1).padStart(2, '0') }}</span>
          <h3>{{ step.title }}</h3>
          <p>{{ step.body }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useContent } from '~/composables/useContent'

type ApproachCopy = (typeof import('~/content/translations').translations)['ru']['approach']

const { t } = useContent()
const copy = computed<ApproachCopy>(() => t('approach') as ApproachCopy)
</script>
