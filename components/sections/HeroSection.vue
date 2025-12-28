<template>
  <section class="hero" id="top">
    <div :class="['section-inner hero-inner reveal hero-animate', { 'is-visible': isHeroVisible }]">
      <div class="hero-copy glass-card">
        <p class="eyebrow">ИКБ · контрактная разработка и ОКР</p>

        <h1>Проектируем и доводим инженерные продукты до рынка.</h1>

        <p class="lead">
          Берём на себя полный цикл: постановка задачи, проектирование, механика и электроника, embedded-ПО,
          испытания и подготовка к предсерии. Работаем с B2B-командами как единый инженерный контур —
          аккуратно, системно и с измеримыми результатами. NDA подписываем на старте и ведём проект в режиме
          «одного окна».
        </p>

        <div class="hero-actions">
          <a class="btn btn-primary" href="#contacts">Запланировать встречу</a>
          <a class="btn btn-ghost" href="#projects">Посмотреть проекты</a>
        </div>

        <div class="hero-metrics">
          <div class="metric">
            <span class="metric-value">18+ лет</span>
            <span class="metric-label">инженерной практики и производства</span>
          </div>
          <div class="metric">
            <span class="metric-value">100+ изделий</span>
            <span class="metric-label">прототипы, MVP и внедрения</span>
          </div>
          <div class="metric">
            <span class="metric-value">NDA</span>
            <span class="metric-label">конфиденциальность по умолчанию</span>
          </div>
        </div>
      </div>

      <div class="hero-aside">
        <div class="glass-card hero-note">
          <h3>Сложные системы под ключ</h3>
          <p>
            Прецизионная механика, силовая электроника, промышленная автоматика, коммуникации, FPGA/embedded,
            стенды и валидация. Собираем решение под бизнес-цель: надёжность, себестоимость, технологичность,
            сроки.
          </p>
        </div>

        <div class="glass-card hero-note">
          <h3>Процесс, который держит сроки</h3>
          <p>
            Выделенный PM, прозрачные артефакты (спеки, схемы, BOM, протоколы испытаний), контроль рисков на
            каждом цикле. Готовность к аудиту, аккуратная документация и понятные статусы без «магии».
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

const isHeroVisible = ref(false);

onMounted(() => {
  // Double RAF to ensure the hidden state paints before toggling visibility.
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      isHeroVisible.value = true;
    });
  });
});
</script>
