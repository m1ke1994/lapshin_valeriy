<template>
  <div class="app-root">
    <AppHeader />
    <NuxtPage />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from '../components/AppHeader.vue'

onMounted(() => {
  if (typeof window === 'undefined') return
  if ('scrollRestoration' in window.history) {
    window.history.scrollRestoration = 'manual'
  }
  window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');

:root {
  --bg: transparent;
  --scroll-bg-image: url('/bg/ezgif-frame-001.png');
  --surface: rgba(255, 255, 255, 0.62);
  --surface-strong: rgba(255, 255, 255, 0.72);
  --surface-soft: rgba(255, 255, 255, 0.52);
  --text: #1b1f28;
  --muted: #4b5462;
  --accent: #2f5b7c;
  --accent-strong: #20445d;
  --accent-warm: #9a7b58;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  background-color: transparent;
  background-image: var(--scroll-bg-image);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

html,
body,
#__nuxt,
.app-root {
  background: transparent;
}

html,
body {
  overflow-x: hidden;
}

body {
  margin: 0;
  font-family: "Manrope", "Segoe UI", sans-serif;
  background: transparent;
  background-image: var(--scroll-bg-image);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  color: var(--text);
}

a {
  color: inherit;
}

.app-root {
  min-height: 100vh;
  color: var(--text);
}
</style>
