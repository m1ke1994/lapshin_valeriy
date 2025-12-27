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
  --bg: transparent;
  --scroll-bg-image: url('/bg/ezgif-frame-001.png');
  --surface: rgba(12, 14, 18, 0.45);
  --surface-strong: rgba(12, 14, 18, 0.6);
  --surface-soft: rgba(18, 22, 28, 0.38);
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

body {
  margin: 0;
  font-family: "Sora", "Manrope", sans-serif;
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
