<template>
  <section id="values" class="section">
    <div class="section-inner reveal">
      <div class="section-head">
        <p class="eyebrow">{{ copy.eyebrow }}</p>
        <h2>{{ copy.title }}</h2>
      </div>

      <div class="cards-grid">
        <article v-for="card in copy.cards" :key="card.title" class="glass-card">
          <h3>{{ card.title }}</h3>
          <p>{{ card.body }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useLocale } from '~/composables/useLocale'

const { t } = useLocale()
const copy = computed(() => t.value.values)
</script>
