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
          <p v-if="status === 'success'" class="contact-status success">
            {{ copy.submitSuccess }}
          </p>
          <p v-else-if="status === 'error'" class="contact-status error">
            {{ errorText }}
          </p>
        </form>
      </div>
    </div>

    <div v-if="showModal" class="modal-backdrop" @click="showModal = false">
      <div class="modal" @click.stop>
        <div class="modal-icon" :class="modalType">
          <span v-if="modalType === 'success'">✓</span>
          <span v-else>!</span>
        </div>
        <p class="modal-title">
          {{ modalType === 'success' ? copy.submitSuccess : copy.submitError }}
        </p>
        <p class="modal-body">{{ modalBody }}</p>
        <button class="btn btn-primary" type="button" @click="showModal = false">{{ copy.modalOk }}</button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, computed, ref } from 'vue'
import { useContent } from '~/composables/useContent'
import { useApiFetch } from '~/composables/useApi'

type ContactsCopy = (typeof import('~/content/translations').translations)['ru']['contacts']

const { copy: content, t } = useContent()
const copy = computed<ContactsCopy>(() => (content.value.contacts || t('contacts')) as ContactsCopy)

const form = reactive({
  name: '',
  phone: '',
  date: '',
  time: '',
})

const status = ref<'idle' | 'loading' | 'success' | 'error'>('idle')
const errorMsg = ref('')
const showModal = ref(false)
const modalType = ref<'success' | 'error'>('success')
const errorText = computed(() => {
  const details = errorMsg.value?.trim()
  if (details) return `${copy.value.submitError} ${details}`
  return copy.value.submitErrorFallback || copy.value.submitError
})
const modalBody = computed(() => {
  if (modalType.value === 'success') return copy.value.submitSuccess
  return errorText.value
})

const isDisabled = computed(() => {
  return status.value === 'loading' || !form.name || !form.phone || !form.date || !form.time
})

async function submit() {
  status.value = 'loading'
  errorMsg.value = ''
  try {
    await useApiFetch('/api/applications/', {
      method: 'POST',
      body: {
        name: form.name,
        phone: form.phone,
        preferred_date: form.date || null,
        preferred_time: form.time || null,
        message: '',
      },
    })
    status.value = 'success'
    modalType.value = 'success'
    showModal.value = true
    form.name = ''
    form.phone = ''
    form.date = ''
    form.time = ''
  } catch (error: any) {
    status.value = 'error'
    modalType.value = 'error'
    errorMsg.value = error?.message || ''
    showModal.value = true
  }
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

.contact-status {
  margin: 8px 0 0;
  font-size: 13px;
}

.contact-status.success {
  color: #6ad597;
}

.contact-status.error {
  color: #ff7b7b;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(12, 16, 26, 0.38);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: grid;
  place-items: center;
  z-index: 20;
  padding: 16px;
}

.modal {
  width: min(480px, 100%);
  background: radial-gradient(circle at 18% 18%, rgba(var(--accent-rgb), 0.14), transparent 48%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.82));
  border: 1px solid rgba(var(--accent-rgb), 0.26);
  border-radius: 18px;
  padding: 22px 22px 20px;
  box-shadow: 0 18px 52px rgba(0, 0, 0, 0.28);
  display: grid;
  gap: 12px;
  position: relative;
  overflow: hidden;
  text-align: center;
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.modal-body {
  font-size: 14px;
  opacity: 0.85;
  margin: 0;
}

.modal-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  font-size: 22px;
  font-weight: 700;
  color: #0b0f1a;
  margin: 0 auto;
}

.modal-icon.success {
  background: rgba(var(--accent-rgb), 0.25);
}

.modal-icon.error {
  background: #ffadad;
}

@media (max-width: 720px) {
  .row-2 {
    grid-template-columns: 1fr;
  }
}
</style>
