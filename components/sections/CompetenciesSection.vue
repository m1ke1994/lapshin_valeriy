<template>
  <section id="competencies" class="section">
    <div class="section-inner reveal">
      <div class="section-head">
        <p class="eyebrow">{{ copy.eyebrow }}</p>
        <h2 v-html="highlight(copy.title)"></h2>
      </div>
      <div class="cards-grid">
        <article v-for="card in copy.cards" :key="card.title" class="glass-card">
          <h3 v-html="highlight(card.title)"></h3>
          <p v-html="highlight(card.body)"></p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useLocale } from '~/composables/useLocale'
import { useHighlight } from '~/composables/useHighlight'

const { t } = useLocale()
const copy = computed(() => t.value.competencies)
const { highlight } = useHighlight()
</script>
