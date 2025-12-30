<template>
  <section id="approach" class="section">
    <div class="section-inner reveal">
      <div class="section-head">
        <p class="eyebrow">{{ copy.eyebrow }}</p>
        <h2 v-html="highlight(copy.title)"></h2>
        <p class="lead" v-html="highlight(copy.lead)"></p>
      </div>
      <div class="steps-grid">
        <div v-for="(step, index) in copy.steps" :key="step.title" class="glass-card step-card">
          <span class="step-index">{{ String(index + 1).padStart(2, '0') }}</span>
          <h3 v-html="highlight(step.title)"></h3>
          <p v-html="highlight(step.body)"></p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useLocale } from '~/composables/useLocale'
import { useHighlight } from '~/composables/useHighlight'

const { t } = useLocale()
const copy = computed(() => t.value.approach)
const { highlight } = useHighlight()
</script>
