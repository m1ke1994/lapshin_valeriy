<template>
  <section id="contacts" class="section">
    <div class="section-inner contact-grid reveal">
      <div class="glass-card contact-card">
        <p class="eyebrow section-title">{{ copy.eyebrow }}</p>
        <h2>{{ copy.title }}</h2>
        <p class="lead">
          {{ copy.lead }}
        </p>
      </div>

      <div class="glass-card contact-card">
        <h3 class="section-title">{{ copy.formTitle }}</h3>

        <form class="contact-form" @submit.prevent="submit">
          <label class="field">
            <span class="field-label">{{ copy.fields.name.label }}</span>
            <input
              v-model.trim="form.name"
              class="field-input"
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
              class="field-input"
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
                class="field-input"
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
                class="field-input"
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
        </form>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useLocale } from '~/composables/useLocale'

const { t } = useLocale()
const copy = computed(() => t.value.contacts)

const form = reactive({
  name: '',
  phone: '',
  date: '',
  time: '',
})

const isDisabled = computed(() => {
  return !form.name || !form.phone || !form.date || !form.time
})

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
  opacity: 0.8;
  letter-spacing: 0.02em;
  cursor: pointer;
}

.field-input {
  width: 100%;
  padding: 12px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.06);
  color: inherit;
  outline: none;
  cursor: pointer;
  transition: border-color 160ms ease, background 160ms ease, box-shadow 160ms ease;
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

.field-input:focus,
.field-input:focus-visible,
.field-input:active {
  border-color: rgba(var(--accent-rgb), 0.75);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.18);
}

.field:hover .field-input {
  border-color: rgba(var(--accent-rgb), 0.35);
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

@media (max-width: 720px) {
  .row-2 {
    grid-template-columns: 1fr;
  }
}
</style>
