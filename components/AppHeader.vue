<template>
  <header class="header">
    <nav class="nav">
      <NuxtLink to="/" class="logo">IKB</NuxtLink>

      <div class="links">
        <a href="#about">About</a>
        <a href="#services">Services</a>
        <a href="#projects">Projects</a>
        <a href="#contacts">Contacts</a>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 50;
  backdrop-filter: blur(14px);
  background: rgba(9, 10, 12, 0.55);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.nav {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-weight: 600;
  font-size: 18px;
  text-decoration: none;
  color: var(--text);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.links a {
  margin-left: 24px;
  text-decoration: none;
  color: var(--text);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  opacity: 0.75;
  transition: opacity 0.2s ease, color 0.2s ease;
}

.links a:hover {
  opacity: 1;
  color: var(--accent);
}
</style>
