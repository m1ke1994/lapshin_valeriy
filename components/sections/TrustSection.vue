<template>
  <section id="trust" class="section">
    <div class="section-inner reveal">
      <div class="section-head">
        <p class="eyebrow">{{ copy.eyebrow }}</p>
        <h2 v-html="highlight(copy.title)"></h2>
        <p class="lead" v-html="highlight(copy.lead)"></p>
      </div>
      <div class="cert-grid">
        <div v-for="card in copy.cards" :key="card.title" class="glass-card cert-card">
          <div class="cert-placeholder">{{ card.title }}</div>
          <p v-html="highlight(card.body)"></p>
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
const copy = computed(() => t.value.trust)
const { highlight } = useHighlight()
</script>
