<template>
  <div class="app-root">
    <AppHeader />
    <NuxtPage />
  </div>
</template>

<script setup>

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
  --bg: #0b0b0c;
  --surface: #121316;
  --surface-2: #1a1c20;
  --text: #f6f6f8;
  --muted: rgba(246, 246, 248, 0.72);
  --accent: #41f0c0;
  --accent-warm: #f2b86d;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: "Space Grotesk", "Satoshi", "Neue Montreal", sans-serif;
  background:
    radial-gradient(1200px 800px at 20% -10%, rgba(65, 240, 192, 0.12), transparent 60%),
    radial-gradient(900px 600px at 80% -20%, rgba(242, 184, 109, 0.15), transparent 55%),
    var(--bg);
  color: var(--text);
}

a {
  color: inherit;
}

.app-root {
  min-height: 100vh;
  background: transparent;
  color: var(--text);
}
</style>
