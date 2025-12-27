<template>
  <header class="header">
    <nav class="nav">
      <NuxtLink to="/" class="logo">IKB БЮРО</NuxtLink>

      <div class="links">
        <a href="#values">Ценности</a>
        <a href="#approach">Подход</a>
        <a href="#competencies">Компетенции</a>
        <a href="#trust">Доверие</a>
        <a href="#projects">Проекты</a>
        <a href="#contacts">Контакты</a>
      </div>

      <a href="#contacts" class="header-cta">Запросить консультацию</a>
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
  backdrop-filter: blur(18px);
  background: rgba(255, 255, 255, 0.6);
  border-bottom: 1px solid rgba(27, 31, 40, 0.12);
}

.nav {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.logo {
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  color: var(--text);
  letter-spacing: 0.32em;
  text-transform: uppercase;
}

.links a {
  margin-left: 24px;
  text-decoration: none;
  color: var(--text);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  opacity: 0.7;
  transition: opacity 0.2s ease, color 0.2s ease;
}

.links a:hover {
  opacity: 1;
  color: var(--accent);
}

.header-cta {
  padding: 10px 16px;
  border-radius: 999px;
  border: 1px solid rgba(32, 68, 93, 0.25);
  text-decoration: none;
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--text);
  background: rgba(255, 255, 255, 0.7);
  transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 12px 30px rgba(27, 31, 40, 0.12);
}

.header-cta:hover {
  border-color: rgba(32, 68, 93, 0.55);
  color: var(--accent-strong);
  background: rgba(255, 255, 255, 0.88);
}

@media (max-width: 900px) {
  .links {
    display: none;
  }

  .nav {
    justify-content: space-between;
  }
}
</style>
