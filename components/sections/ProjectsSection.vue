<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useLocale } from '~/composables/useLocale'

type Project = {
  id: string
  title: string
  description: string
  category: string
  stage: string
  tags?: string[]
  image: string
}

const { t, locale } = useLocale()
const copy = computed(() => t.value.projects)
const placeholder = '/projects/nophoto.png'

const projects = computed<Project[]>(() => {
  const image = placeholder
  return [
    {
      id: 'udot-v1',
      title: '«УДОТ» v.1',
      description:
        'Свободно программируемое устройство: обработка входных цифровых и аналоговых сигналов, управление силовой нагрузкой, периферийный модуль связи (RS-485, DALI), питание 9–230 В.',
      category: 'Устройства управления',
      stage: 'Прототип',
      tags: ['RS-485', 'DALI'],
      image,
    },
    {
      id: 'udot-v2',
      title: '«УДОТ» v.2',
      description:
        'Управление электромагнитными клапанами гидравлических распределителей спецтехники. Входы: цифровые и аналоговые, связь RS-485, питание 9–40 В.',
      category: 'Устройства управления',
      stage: 'Прототип',
      tags: ['RS-485', 'Гидравлика'],
      image,
    },
    {
      id: 'mobius',
      title: '«МЁБИУС»',
      description:
        'Ёмкостное бесконтактное управление освещением или другой нагрузкой, возможна скрытая установка за отделкой. Патент RU68221.',
      category: 'Свет',
      stage: 'MVP',
      image,
    },
    {
      id: 'avis',
      title: '«АВИС»',
      description: 'Блок управления приводом ячейки КРУ(Э).',
      category: 'Инфраструктура',
      stage: 'Макет',
      image,
    },
    {
      id: 'disconnector',
      title: 'Блок управления разъединителем',
      description:
        'Автономный блок для отключения/включения нагрузки в бестоковую паузу (АПВ) с дистанционным управлением.',
      category: 'Устройства управления',
      stage: 'Концепт',
      image,
    },
    {
      id: 'typec',
      title: '«Конвертор Type-C»',
      description: 'Преобразователь USB Type-C в интерфейсы RS-485, RS-232 и др.',
      category: 'Инфраструктура',
      stage: 'Концепт',
      tags: ['USB-C', 'RS-485', 'RS-232'],
      image,
    },
    {
      id: 'mobile-electricity',
      title: '«Мобильное электричество»',
      description:
        'Прицеп с комплектом оборудования для длительной генерации электроэнергии в полевых условиях.',
      category: 'Автономность',
      stage: 'MVP',
      image,
    },
    {
      id: 'autonomous-village',
      title: '«Автономный посёлок»',
      description:
        'Оборудование для коттеджей с объединением в локальную сеть; эффективно от 50 домов.',
      category: 'Автономность',
      stage: 'Концепт',
      image,
    },
    {
      id: 'interos',
      title: '«ИнтеРОС»',
      description:
        'Децентрализованная модульная система для умного дома с адаптацией под привычки пользователя.',
      category: 'Инфраструктура',
      stage: 'MVP',
      image,
    },
    {
      id: 'no-switches',
      title: '«Свет без выключателей»',
      description:
        'Полная автоматика освещения и вентиляции с интеллектуальной подстройкой под объект.',
      category: 'Свет',
      stage: 'Прототип',
      image,
    },
    {
      id: 'light-wave',
      title: '«Световая волна»',
      description: 'Освещение протяжённых участков с управляемыми сценариями.',
      category: 'Свет',
      stage: 'MVP',
      image,
    },
    {
      id: 'house-no-electricity',
      title: '«Дом без электричества»',
      description:
        'Автономная солнечная установка; успешно работает с 2012 года в средней полосе России.',
      category: 'Автономность',
      stage: 'MVP',
      tags: ['Солнечная генерация'],
      image,
    },
    {
      id: 'underwater-pager',
      title: '«Подводный пейджер»',
      description:
        'Носимое устройство для быстрого поиска подводников в аварийной ситуации или обмена сообщениями под водой.',
      category: 'Инфраструктура',
      stage: 'Макет',
      image,
    },
    {
      id: 'sinus',
      title: '«СИНУС»',
      description:
        'Диммируемая LED-лампа/светильник для стандартного патрона или самостоятельного монтажа.',
      category: 'Свет',
      stage: 'Прототип',
      image,
    },
    {
      id: 'divo',
      title: '«ДиВО»',
      description: 'Дистанционное управление подсветкой рекламных конструкций.',
      category: 'Свет',
      stage: 'Прототип',
      image,
    },
    {
      id: 'emotional-light',
      title: '«Эмоциональное освещение»',
      description:
        'Управление режимами освещения и температуры по эмоциям (негативные/нейтральные/позитивные) без ИИ.',
      category: 'Свет',
      stage: 'Концепт',
      image,
    },
    {
      id: 'mobile-office',
      title: '«Мобильный офис»',
      description: 'Вагон-прицеп для длительного автономного проживания или работы.',
      category: 'Автономность',
      stage: 'Концепт',
      image,
    },
    {
      id: 'starwire',
      title: '«StarWire»',
      description:
        'Безопасный удлинитель: контроль температуры контактов, типа нагрузки, отключение забытого прибора.',
      category: 'Инфраструктура',
      stage: 'Прототип',
      image,
    },
    {
      id: 'birch-lamp',
      title: '«Birch-Lamp»',
      description:
        'Декоративный светильник с сенсорным управлением, имитацией пламени и возможностью «задуть».',
      category: 'Свет',
      stage: 'MVP',
      image,
    },
    {
      id: 'million-lamp',
      title: '«Million Lamp»',
      description:
        'Подвесной светильник из 1400 светодиодов с управлением любым ИК-пультом.',
      category: 'Свет',
      stage: 'MVP',
      image,
    },
    {
      id: 'tumbler',
      title: '«ТУМБЛЕР»',
      description: 'Открытая АСУ ТП.',
      category: 'Устройства управления',
      stage: 'Концепт',
      image,
    },
  ]
})

const defaultCategory = 'Устройства управления'
const query = ref('')
const activeCategory = ref<string>(defaultCategory)
const activeStage = ref<string>('all')

const categories = computed(() => ['all', ...new Set(projects.value.map((p) => p.category))])
const stages = computed(() => ['all', ...new Set(projects.value.map((p) => p.stage))])

const labels = computed(() => {
  const ru = locale.value === 'ru'
  return {
    domain: ru ? 'Отрасль' : 'Domain',
    stage: ru ? 'Статус' : 'Stage',
    searchLabel: ru ? 'Поиск' : 'Search',
    search: ru ? 'Поиск по описанию, тегам и названию' : 'Search title, description, tags',
    reset: ru ? 'Сбросить' : 'Reset',
    empty: ru ? 'Нет проектов под выбранные фильтры' : 'No projects for the selected filters',
    results: ru ? 'Найдено' : 'Found',
  }
})

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return projects.value.filter((p) => {
    const byCategory = activeCategory.value === 'all' || p.category === activeCategory.value
    const byStage = activeStage.value === 'all' || p.stage === activeStage.value
    const byQuery =
      !q ||
      p.title.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      (p.tags ?? []).some((tag) => tag.toLowerCase().includes(q))
    return byCategory && byStage && byQuery
  })
})

const resetFilters = () => {
  query.value = ''
  activeCategory.value = defaultCategory
  activeStage.value = 'all'
}

const fallbackImg = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = placeholder
}

watch(locale, () => resetFilters())
</script>

<template>
  <section id="projects" class="section projects-section">
    <div class="section-inner reveal">
      <div class="section-head section-head--split">
        <div>
          <p class="eyebrow">{{ copy.eyebrow }}</p>
          <h2>{{ copy.title }}</h2>
          <p class="lead">{{ copy.lead }}</p>
        </div>
      
      </div>

      <div class="controls-grid">
        <div class="projects-controls glass-card control-card">
          <div class="filter-block">
            <span class="filter-label">{{ labels.domain }}</span>
            <div class="chip-group">
              <button
                v-for="category in categories"
                :key="category"
                type="button"
                class="chip"
                :class="{ 'is-active': activeCategory === category }"
                @click="activeCategory = category"
              >
                {{ category === 'all' ? (locale === 'ru' ? 'Все' : 'All') : category }}
              </button>
            </div>
          </div>
        </div>

        <div class="projects-controls glass-card control-card">
          <div class="filter-block">
            <span class="filter-label">{{ labels.stage }}</span>
            <div class="chip-group">
              <button
                v-for="stage in stages"
                :key="stage"
                type="button"
                class="chip"
                :class="{ 'is-active': activeStage === stage }"
                @click="activeStage = stage"
              >
                {{ stage === 'all' ? (locale === 'ru' ? 'Все' : 'All') : stage }}
              </button>
            </div>
          </div>
        </div>

        <div class="projects-controls glass-card control-card search-card">
          <div class="filter-block search-block">
            <span class="filter-label">{{ labels.searchLabel }}</span>
            <div class="search-shell">
              <input
                v-model="query"
                type="text"
                :placeholder="labels.search"
                class="search-input"
              />
              <button type="button" class="chip ghost" @click="resetFilters">{{ labels.reset }}</button>
            </div>
            <span class="meta">{{ labels.results }}: {{ filtered.length }}</span>
          </div>
        </div>
      </div>

      <div v-if="filtered.length" class="projects-grid">
        <article
          v-for="(project, index) in filtered"
          :key="project.id"
          class="project-card glass-card"
        >
          <div class="project-visual">
            <img :src="project.image" :alt="project.title" loading="lazy" @error="fallbackImg" />
            <div class="badge-row">
              <span class="badge">{{ project.category }}</span>
              <span class="badge badge-soft">{{ project.stage }}</span>
            </div>
            <span class="card-index">{{ String(index + 1).padStart(2, '0') }}</span>
          </div>
          <div class="project-body">
            <h3>{{ project.title }}</h3>
            <p class="project-description">{{ project.description }}</p>
            <div v-if="project.tags?.length" class="project-tags">
              <span v-for="tag in project.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </article>
      </div>

      <div v-else class="empty-state glass-card">
        <p>{{ labels.empty }}</p>
        <button type="button" class="chip ghost" @click="resetFilters">{{ labels.reset }}</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.projects-section {
  position: relative;
}

.projects-section::after {
  content: '';
  position: absolute;
  inset: 40px 0 auto;
  height: 420px;
  background: radial-gradient(60% 45% at 50% 18%, rgba(var(--accent-rgb), 0.16), transparent),
    radial-gradient(40% 35% at 20% 5%, rgba(255, 255, 255, 0.32), transparent);
  filter: blur(50px);
  opacity: 0.75;
  pointer-events: none;
  z-index: 0;
}

.controls-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  margin-bottom: 20px;
}

.projects-controls {
  position: relative;
  overflow: hidden;
  padding: 16px;
}

.projects-controls::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(115deg, rgba(var(--accent-rgb), 0.12), transparent 45%, rgba(255, 255, 255, 0.32));
  opacity: 0.8;
  pointer-events: none;
}

.control-card {
  border: 1px solid rgba(var(--text-rgb), 0.08);
}

.search-card {
  display: flex;
  align-items: center;
}

.filter-block {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-label {
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(var(--text-rgb), 0.65);
}

.chip-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  border: 1px solid rgba(var(--text-rgb), 0.08);
  background: rgba(255, 255, 255, 0.8);
  color: var(--text);
  padding: 9px 12px;
  border-radius: 999px;
  font-size: 13px;
  letter-spacing: 0.02em;
  transition: all 0.18s ease;
  box-shadow: 0 8px 18px rgba(15, 18, 26, 0.08);
}

.chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(15, 18, 26, 0.14);
}

.chip.is-active {
  border-color: rgba(var(--accent-rgb), 0.5);
  background: linear-gradient(120deg, rgba(var(--accent-rgb), 0.16), rgba(255, 255, 255, 0.9));
  color: #6b4b14;
  box-shadow: 0 12px 28px rgba(15, 18, 26, 0.12);
}

.chip.ghost {
  background: rgba(255, 255, 255, 0.6);
  border: 1px dashed rgba(var(--text-rgb), 0.2);
  box-shadow: none;
}

.search-block {
  position: relative;
}

.search-shell {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-input {
  flex: 1;
  border: 1px solid rgba(var(--text-rgb), 0.08);
  background: rgba(255, 255, 255, 0.9);
  padding: 12px 14px;
  border-radius: 14px;
  font-size: 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: rgba(var(--accent-rgb), 0.5);
  box-shadow: 0 0 0 6px rgba(var(--accent-rgb), 0.12);
}

.meta {
  font-size: 12px;
  color: rgba(var(--text-rgb), 0.55);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
  position: relative;
}

.project-card {
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 12px;
  padding: 0;
  overflow: hidden;
  background: linear-gradient(150deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.78));
  border: 1px solid rgba(var(--text-rgb), 0.05);
  box-shadow: 0 14px 32px rgba(15, 18, 26, 0.12);
  position: relative;
}

.project-visual {
  position: relative;
  overflow: hidden;
  aspect-ratio: 4 / 3;
}

.project-visual img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.85);
  transform: scale(1.01);
  transition: transform 0.35s ease;
}

.project-card:hover .project-visual img {
  transform: scale(1.04);
}

.project-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(var(--accent-rgb), 0.08), transparent 38%, rgba(0, 0, 0, 0.05));
  mix-blend-mode: multiply;
  pointer-events: none;
}

.badge-row {
  position: absolute;
  bottom: 14px;
  left: 14px;
  display: flex;
  gap: 8px;
}

.card-index {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 7px 9px;
  border-radius: 11px;
  background: rgba(0, 0, 0, 0.38);
  color: #f9f9f9;
  font-size: 12px;
  letter-spacing: 0.08em;
}

.badge {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(var(--accent-rgb), 0.15);
  color: #6b4b14;
  font-size: 12px;
  letter-spacing: 0.04em;
  border: 1px solid rgba(var(--accent-rgb), 0.4);
  backdrop-filter: blur(8px);
}

.badge-soft {
  background: rgba(15, 18, 26, 0.65);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.35);
}

.project-body {
  padding: 0 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.project-body h3 {
  margin: 0;
  font-size: 18px;
  letter-spacing: -0.01em;
  color: var(--text);
}

.project-description {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
  font-size: 14px;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 6px;
}

.tag {
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(var(--text-rgb), 0.05);
  border: 1px solid rgba(var(--text-rgb), 0.08);
  font-size: 11.5px;
  color: rgba(var(--text-rgb), 0.68);
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px dashed rgba(var(--text-rgb), 0.14);
  padding: 14px 16px;
}

.empty-state p {
  margin: 0;
  color: var(--muted);
}

.section-head--split {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
  gap: 18px;
  align-items: center;
}

.legend {
  display: grid;
  gap: 10px;
  padding: 18px;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  border: 1px solid rgba(var(--accent-rgb), 0.24);
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.dot-accent {
  background: rgba(var(--accent-rgb), 0.8);
}

.dot-dark {
  background: rgba(0, 0, 0, 0.65);
}

.legend-title {
  margin: 0;
  font-weight: 600;
  color: var(--text);
}

.legend-meta {
  margin: 2px 0 0;
  font-size: 13px;
  color: var(--muted);
}

@media (max-width: 720px) {
  .projects-controls {
    grid-template-columns: 1fr;
  }

  .badge-row {
    flex-wrap: wrap;
  }

  .empty-state {
    flex-direction: column;
    align-items: flex-start;
  }

  .section-head--split {
    grid-template-columns: 1fr;
  }
}
</style>
