<template>
  <div class="app-root">
    <AppHeader />
    <NuxtPage />
  </div>
</template>

<script setup>

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Unbounded:wght@400;500;600;700&display=swap');

:root {
  --bg: #07080b;
  --surface: rgba(16, 18, 23, 0.72);
  --surface-strong: rgba(16, 18, 23, 0.92);
  --surface-soft: rgba(24, 28, 36, 0.62);
  --text: #f7f7f8;
  --muted: rgba(246, 246, 248, 0.72);
  --accent: #d2a66d;
  --accent-strong: #f1c17d;
  --accent-cool: #7dd8f1;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

html,
body,
#__nuxt,
.app-root {
  background: transparent;
}

body {
  margin: 0;
  font-family: "Sora", "Manrope", sans-serif;
  background: var(--bg);
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
