<template>
  <main class="page">
    <ScrollBgAnimation />

    <section class="hero" id="top">
      <div class="section-inner hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">Инновационное конструкторское бюро</p>
          <h1>Проектируем инженерные системы, которые запускаются без компромиссов.</h1>
          <p class="lead">
            От научно-технической концепции до опытной партии: моделирование,
            испытания, документация, подготовка производства. Ваш продукт получает
            точную механику, красивую форму и прогнозируемую себестоимость.
          </p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#contacts">Обсудить проект</a>
            <a class="btn btn-ghost" href="#projects">Смотреть кейсы</a>
          </div>
          <div class="hero-metrics">
            <div class="metric">
              <span class="metric-value">60+ инженеров</span>
              <span class="metric-label">механика, электроника, софт</span>
            </div>
            <div class="metric">
              <span class="metric-value">18 недель</span>
              <span class="metric-label">средний цикл прототипа</span>
            </div>
            <div class="metric">
              <span class="metric-value">94%</span>
              <span class="metric-label">проектов доходят до серии</span>
            </div>
          </div>
        </div>

        <div class="hero-panel">
          <div class="panel-card reveal" style="--delay: 0.1s">
            <p class="panel-title">Фокус бюро</p>
            <ul>
              <li>Промышленный дизайн сложных устройств</li>
              <li>Высокоточная механика и компоновка</li>
              <li>Интеграция электроники и ПО</li>
              <li>Подготовка к серийному выпуску</li>
            </ul>
          </div>
          <div class="panel-card highlight reveal" style="--delay: 0.25s">
            <p class="panel-title">Экспертиза</p>
            <p class="panel-text">
              Робототехника, медицинские приборы, энергетика, инструментальные
              системы, транспортные платформы.
            </p>
            <div class="panel-tags">
              <span>R&D</span>
              <span>DFM</span>
              <span>CAE</span>
              <span>Prototype Lab</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="about" class="section section--about">
      <div class="section-inner grid-two">
        <div>
          <p class="eyebrow">О бюро</p>
          <h2>Мы превращаем инженерную идею в продукт, готовый к масштабированию.</h2>
          <p class="lead">
            Бюро работает как внешний центр компетенций: системная архитектура,
            глубокая инженерия и контроль всех узлов. Мы берём на себя ответственность
            за итог, оставаясь гибкими в процессе.
          </p>
        </div>
        <div class="feature-stack">
          <article class="feature-card reveal" style="--delay: 0.1s">
            <h3>Компоновка и цифровой двойник</h3>
            <p>
              Прорабатываем механику и тепловые режимы в CAE до первого металла.
              Это экономит месяцы итераций в прототипах.
            </p>
          </article>
          <article class="feature-card reveal" style="--delay: 0.2s">
            <h3>Функциональные прототипы</h3>
            <p>
              Собственная лаборатория, 3D-печать, ЧПУ и сборка под задачи R&D.
              Проверяем гипотезы в реальном масштабе.
            </p>
          </article>
          <article class="feature-card reveal" style="--delay: 0.3s">
            <h3>Готовность к серии</h3>
            <p>
              Документация по ГОСТ, подбор поставщиков, DFM/DFX, тестовые стенды.
              Продукт выходит в производство без сюрпризов.
            </p>
          </article>
        </div>
      </div>
    </section>

    <section id="services" class="section section--services">
      <div class="section-inner">
        <div class="section-head">
          <p class="eyebrow">Компетенции</p>
          <h2>Набор решений для технологического лидерства.</h2>
          <p class="lead">
            Команда закрывает весь стек — от концепта до серийной поддержки.
          </p>
        </div>
        <div class="cards-grid">
          <article class="service-card reveal" style="--delay: 0.05s">
            <h3>Системная архитектура</h3>
            <p>Разбиваем продукт на подсистемы, задаем интерфейсы и KPI.</p>
          </article>
          <article class="service-card reveal" style="--delay: 0.1s">
            <h3>Механика и компоновка</h3>
            <p>Проработка узлов, точностные расчеты, подбор материалов.</p>
          </article>
          <article class="service-card reveal" style="--delay: 0.15s">
            <h3>Промышленный дизайн</h3>
            <p>Визуальный код продукта, эргономика и премиальные материалы.</p>
          </article>
          <article class="service-card reveal" style="--delay: 0.2s">
            <h3>Электроника и ПО</h3>
            <p>Схемотехника, встроенные системы, интеллектуальные контуры.</p>
          </article>
          <article class="service-card reveal" style="--delay: 0.25s">
            <h3>Инженерные испытания</h3>
            <p>Стресс-тесты, виброанализ, тепловизия, сертификация.</p>
          </article>
          <article class="service-card reveal" style="--delay: 0.3s">
            <h3>Сопровождение серии</h3>
            <p>Оптимизация под производство и снабжение на старте продаж.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--process">
      <div class="section-inner">
        <div class="section-head">
          <p class="eyebrow">Процесс</p>
          <h2>Чёткий маршрут от запроса до запуска.</h2>
          <p class="lead">
            Каждому этапу соответствует понятный результат и критерии готовности.
          </p>
        </div>
        <div class="process-grid">
          <div class="process-step reveal" style="--delay: 0.05s">
            <span class="step-index">01</span>
            <h3>Диагностика</h3>
            <p>Аналитика рынка, бриф, технико-экономический расчёт.</p>
          </div>
          <div class="process-step reveal" style="--delay: 0.1s">
            <span class="step-index">02</span>
            <h3>Концепт</h3>
            <p>Архитектура изделия, 3D-схемы, визуальные прототипы.</p>
          </div>
          <div class="process-step reveal" style="--delay: 0.15s">
            <span class="step-index">03</span>
            <h3>Инженерия</h3>
            <p>Деталировка, CAE-расчёты, выбор материалов и компонентов.</p>
          </div>
          <div class="process-step reveal" style="--delay: 0.2s">
            <span class="step-index">04</span>
            <h3>Прототип</h3>
            <p>Сборка, испытания, итерации, финальная валидация.</p>
          </div>
          <div class="process-step reveal" style="--delay: 0.25s">
            <span class="step-index">05</span>
            <h3>Серия</h3>
            <p>Документация, запуск оснастки, переход в производство.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="projects" class="section section--projects">
      <div class="section-inner">
        <div class="section-head">
          <p class="eyebrow">Кейсы</p>
          <h2>Продукты, которые меняют отрасли.</h2>
          <p class="lead">
            Три последних проекта, где мы отвечали за полную инженерную вертикаль.
          </p>
        </div>
        <div class="projects-grid">
          <article class="project-card reveal" style="--delay: 0.05s">
            <p class="project-title">Автономная мобильная платформа</p>
            <p class="project-meta">Робототехника · 6 месяцев</p>
            <p>
              Компоновка батарей и тягового узла, интеграция лидара, дизайн корпуса
              для работы 24/7 в логистике.
            </p>
          </article>
          <article class="project-card reveal" style="--delay: 0.1s">
            <p class="project-title">Медицинский прибор точной дозировки</p>
            <p class="project-meta">MedTech · 4 месяца</p>
            <p>
              Ультраточная механика, стерильные материалы, новый форм-фактор для
              госпитального сегмента.
            </p>
          </article>
          <article class="project-card reveal" style="--delay: 0.15s">
            <p class="project-title">Энергетический модуль мониторинга</p>
            <p class="project-meta">Энергетика · 5 месяцев</p>
            <p>
              Разработка шасси, термоуправление, подготовка к испытаниям по ГОСТ.
            </p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--metrics">
      <div class="section-inner metrics-grid">
        <div class="metric-card reveal" style="--delay: 0.05s">
          <p class="metric-value">120+</p>
          <p class="metric-label">прототипов и пилотных образцов</p>
        </div>
        <div class="metric-card reveal" style="--delay: 0.1s">
          <p class="metric-value">15 отраслей</p>
          <p class="metric-label">робототехника, медтех, нефтегаз</p>
        </div>
        <div class="metric-card reveal" style="--delay: 0.15s">
          <p class="metric-value">48 часов</p>
          <p class="metric-label">до первого инженерного аудита</p>
        </div>
      </div>
    </section>

    <section id="contacts" class="section section--contacts">
      <div class="section-inner contact-card">
        <div>
          <p class="eyebrow">Контакты</p>
          <h2>Готовы обсудить новый продукт?</h2>
          <p class="lead">
            Проведём инженерную сессию и предложим маршрут разработки.
          </p>
        </div>
        <div class="contact-actions">
          <a class="btn btn-primary" href="mailto:hello@ikb.studio">
            hello@ikb.studio
          </a>
          <p class="contact-note">
            Москва · Берлин · Дубай
          </p>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
</script>

<style scoped>
.page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.section,
.hero {
  position: relative;
  padding: 160px 24px;
  z-index: 2;
}

.hero {
  padding-top: 200px;
}

.section-inner {
  max-width: 1180px;
  margin: 0 auto;
}

.hero-inner {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
  gap: 56px;
  align-items: start;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero-copy h1 {
  font-family: "Unbounded", sans-serif;
  font-size: clamp(40px, 5vw, 72px);
  line-height: 1.05;
  margin: 0;
  text-shadow: 0 10px 30px rgba(7, 8, 11, 0.3);
}

.eyebrow {
  margin: 0 0 12px;
  font-size: 11px;
  letter-spacing: 0.35em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.6);
}

h2 {
  font-family: "Unbounded", sans-serif;
  font-size: clamp(30px, 4vw, 52px);
  line-height: 1.1;
  margin: 0 0 20px;
  text-shadow: 0 8px 24px rgba(7, 8, 11, 0.25);
}

h3 {
  margin: 0 0 12px;
  font-size: 18px;
}

.lead {
  font-size: 17px;
  line-height: 1.8;
  margin: 0;
  max-width: 720px;
  color: var(--muted);
  text-shadow: 0 6px 18px rgba(7, 8, 11, 0.2);
}

.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border-radius: 999px;
  text-decoration: none;
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.btn-primary {
  background: linear-gradient(130deg, var(--accent), var(--accent-strong));
  color: #1a1208;
  box-shadow: 0 12px 36px rgba(210, 166, 109, 0.25);
}

.btn-ghost {
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: var(--text);
  background: transparent;
}

.btn:hover {
  transform: translateY(-2px);
}

.hero-metrics {
  display: grid;
  gap: 12px;
}

.metric {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 12px;
}

.metric-value {
  font-weight: 600;
}

.metric-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.2em;
}

.hero-panel {
  display: grid;
  gap: 18px;
}

.panel-card {
  padding: 28px;
  border-radius: 20px;
  background: var(--surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(10px);
}

.panel-card ul {
  margin: 0;
  padding-left: 18px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.72);
}

.panel-title {
  margin: 0 0 12px;
  font-size: 13px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.6);
}

.panel-text {
  margin: 0 0 16px;
  color: rgba(255, 255, 255, 0.78);
  line-height: 1.7;
}

.panel-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.panel-tags span {
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
}

.panel-card.highlight {
  background: var(--surface-strong);
  border-color: rgba(210, 166, 109, 0.3);
}

.grid-two {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 48px;
  align-items: start;
}

.feature-stack {
  display: grid;
  gap: 18px;
}

.feature-card,
.service-card,
.project-card,
.metric-card,
.process-step {
  padding: 24px;
  border-radius: 18px;
  background: var(--surface-soft);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
}

.feature-card p,
.service-card p,
.project-card p {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

.section-head {
  margin-bottom: 40px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 18px;
}

.step-index {
  font-size: 12px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--accent);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.project-title {
  margin: 0 0 8px;
  font-size: 18px;
}

.project-meta {
  margin: 0 0 14px;
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.55);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  text-align: center;
}

.metric-card .metric-value {
  font-family: "Unbounded", sans-serif;
  font-size: 32px;
  margin: 0 0 6px;
}

.metric-card .metric-label {
  margin: 0;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: rgba(255, 255, 255, 0.6);
}

.contact-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  padding: 48px;
  border-radius: 24px;
  background: var(--surface-strong);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 22px 50px rgba(0, 0, 0, 0.35);
}

.contact-actions {
  display: grid;
  gap: 12px;
  text-align: right;
}

.contact-note {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.55);
}

.reveal {
  opacity: 0;
  transform: translateY(12px);
  animation: reveal 0.8s ease forwards;
  animation-delay: var(--delay, 0s);
}

@keyframes reveal {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 980px) {
  .hero-inner,
  .grid-two {
    grid-template-columns: 1fr;
  }

  .cards-grid,
  .projects-grid,
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .contact-card {
    flex-direction: column;
    text-align: left;
  }

  .contact-actions {
    text-align: left;
  }
}

@media (max-width: 720px) {
  .section,
  .hero {
    padding: 120px 20px;
  }

  .hero {
    padding-top: 160px;
  }

  .metric {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
