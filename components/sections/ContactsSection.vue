<template>
  <section id="contacts" class="section">
    <div class="section-inner contact-grid reveal">
      <div class="glass-card contact-card">
        <p class="eyebrow section-title">{{ copy.eyebrow }}</p>
        <h2 v-html="highlight(copy.title)"></h2>
        <p class="lead">
          <span v-html="highlight(copy.lead)"></span>
        </p>
      </div>

      <div class="glass-card contact-card">
        <h3 class="section-title" v-html="highlight(copy.formTitle)"></h3>

        <form class="contact-form" @submit.prevent="submit">
          <label class="field">
            <span class="field-label">{{ copy.fields.name.label }}</span>
            <input
              v-model.trim="form.name"
              class="field-input ikb-field"
              type="text"
              name="name"
              autocomplete="name"
              :placeholder="copy.fields.name.placeholder"
              required
            />
          </label>

          <label class="field">
            <span class="field-label">{{ copy.fields.phone.label }}</span>
            <input
              v-model.trim="form.phone"
              class="field-input ikb-field"
              type="tel"
              name="phone"
              autocomplete="tel"
              inputmode="tel"
              :placeholder="copy.fields.phone.placeholder"
              required
            />
          </label>

          <div class="row-2">
            <label class="field">
              <span class="field-label">{{ copy.fields.date.label }}</span>
              <input
                v-model="form.date"
                class="field-input ikb-field"
                type="date"
                name="date"
                :placeholder="copy.fields.date.placeholder"
                required
              />
            </label>

            <label class="field">
              <span class="field-label">{{ copy.fields.time.label }}</span>
              <input
                v-model="form.time"
                class="field-input ikb-field"
                type="time"
                name="time"
                :placeholder="copy.fields.time.placeholder"
                required
              />
            </label>
          </div>

          <p class="contact-note">
            {{ copy.note }}
          </p>

          <button class="btn btn-primary" type="submit" :disabled="isDisabled">
            {{ copy.button }}
          </button>

          <p class="contact-alt">
            {{ copy.alt }} <a href="mailto:hello@ikb.studio">hello@ikb.studio</a>
          </p>

          <div class="loyalty-widget">
            <div id="loyalty-entry" class="loyalty-entry-slot" aria-live="polite"></div>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, computed, onMounted } from 'vue'
import { useLocale } from '~/composables/useLocale'
import { useHighlight } from '~/composables/useHighlight'

const { t } = useLocale()
const copy = computed(() => t.value.contacts)
const { highlight } = useHighlight()

const form = reactive({
  name: '',
  phone: '',
  date: '',
  time: '',
})

const isDisabled = computed(() => {
  return !form.name || !form.phone || !form.date || !form.time
})

declare global {
  interface Window {
    LoyaltyEntryWidget?: {
      mount: (selector: string, options: { tenantSlug: string; pwaUrl: string }) => void
    }
  }
}

const widgetSelector = '#loyalty-entry'
const widgetOptions = {
  tenantSlug: 'demo',
  pwaUrl: 'http://localhost:8080/pwa?t=demo',
}

const mountWidget = () => {
  const mountFn = window.LoyaltyEntryWidget?.mount
  if (typeof mountFn !== 'function') return
  mountFn(widgetSelector, widgetOptions)
}

const onWidgetScriptLoad = () => {
  const scriptEl = document.querySelector<HTMLScriptElement>('script[data-loyalty-widget-entry]')
  if (scriptEl) {
    scriptEl.dataset.loaded = 'true'
  }
  mountWidget()
}

const ensureWidgetScript = () => {
  if (typeof window === 'undefined') return

  const existingScript = document.querySelector<HTMLScriptElement>('script[data-loyalty-widget-entry]')
  if (existingScript) {
    if (window.LoyaltyEntryWidget?.mount) {
      mountWidget()
    } else {
      existingScript.addEventListener('load', onWidgetScriptLoad, { once: true })
    }
    return
  }

  const script = document.createElement('script')
  script.src = 'http://localhost:8080/widget/entry-widget.js'
  script.async = true
  script.dataset.loyaltyWidgetEntry = 'true'
  script.addEventListener('load', onWidgetScriptLoad, { once: true })
  document.head.appendChild(script)
}

function submit() {
  const subject = encodeURIComponent(copy.value.mailSubject)
  const body = encodeURIComponent(
    [
      `${copy.value.mailLabels.name}: ${form.name}`,
      `${copy.value.mailLabels.phone}: ${form.phone}`,
      `${copy.value.mailLabels.date}: ${form.date}`,
      `${copy.value.mailLabels.time}: ${form.time}`,
    ].join('\n')
  )

  window.location.href = `mailto:hello@ikb.studio?subject=${subject}&body=${body}`
}

onMounted(() => {
  ensureWidgetScript()
})
</script>

<style scoped>
.section-title {
  color: var(--accent-strong);
}

.contact-form {
  display: grid;
  gap: 12px;
  margin-top: 10px;
}

.field {
  display: grid;
  gap: 6px;
  cursor: pointer;
}

.field-label {
  font-size: 12px;
  opacity: 0.92;
  letter-spacing: 0.02em;
  color: rgba(var(--text-rgb), 0.9);
  cursor: pointer;
}

.field-input {
  cursor: pointer;
  background: var(--field-bg);
  border: 1px solid var(--field-border);
  color: var(--text);
  box-shadow: 0 8px 22px rgba(15, 18, 26, 0.08);
  transition:
    border-color 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease;
}

.field-input[type='text'],
.field-input[type='tel'],
.field-input[type='email'],
.field-input[type='search'],
.field-input[type='password'],
.field-input[type='url'],
.field-input[type='number'] {
  cursor: text;
}

.field:hover .field-input {
  border-color: var(--field-border-strong);
  background: var(--field-bg-hover);
}

.field-input:focus,
.field-input:focus-visible {
  border-color: rgba(var(--accent-rgb), 0.8);
  background: #fff;
  box-shadow:
    0 10px 28px rgba(15, 18, 26, 0.12),
    0 0 0 3px rgba(var(--accent-rgb), 0.2);
}

.field-input::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.85;
}

.btn,
button,
a {
  cursor: pointer;
}

.row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.contact-note {
  margin: 2px 0 0;
  font-size: 13px;
  opacity: 0.78;
}

.contact-alt {
  margin: 6px 0 0;
  font-size: 13px;
  opacity: 0.75;
}

.loyalty-widget {
  position: fixed;
  right: 26px;
  top: 50%;
  transform: translateY(-50%);
  width: min(360px, 88vw);
  padding: 16px;
  border-radius: 18px;
  border: 1px solid rgba(var(--accent-rgb), 0.28);
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.9));
  box-shadow:
    0 18px 48px rgba(15, 18, 26, 0.24),
    0 6px 18px rgba(15, 18, 26, 0.12);
  z-index: 40;
}

.loyalty-entry-slot {
  min-height: 220px;
}

@media (max-width: 720px) {
  .row-2 {
    grid-template-columns: 1fr;
  }

  .loyalty-widget {
    right: 14px;
    top: auto;
    bottom: 14px;
    transform: none;
    width: min(420px, 94vw);
    padding: 14px;
  }
}
</style>
