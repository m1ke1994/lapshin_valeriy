<template>
  <section id="contacts" class="section">
    <div class="section-inner contact-grid reveal">
      <!-- Левый блок оставляем как был -->
      <div class="glass-card contact-card">
        <p class="eyebrow section-title">Контакты</p>
        <h2>Соберём задачу в чёткий план в течение 48 часов.</h2>
        <p class="lead">
          Встреча онлайн или офлайн, подписание NDA, первичный разбор рисков и дорожная карта. Мы берём на себя
          подготовку артефактов, чтобы вы сразу видели ход проекта.
        </p>
      </div>

      <!-- Правый блок: форма -->
      <div class="glass-card contact-card">
        <h3 class="section-title">Запросить звонок</h3>

        <form class="contact-form" @submit.prevent="submit">
          <label class="field">
            <span class="field-label">Имя</span>
            <input
              v-model.trim="form.name"
              class="field-input"
              type="text"
              name="name"
              autocomplete="name"
              placeholder="Как к вам обращаться"
              required
            />
          </label>

          <label class="field">
            <span class="field-label">Телефон</span>
            <input
              v-model.trim="form.phone"
              class="field-input"
              type="tel"
              name="phone"
              autocomplete="tel"
              inputmode="tel"
              placeholder="+7 (___) ___-__-__"
              required
            />
          </label>

          <div class="row-2">
            <label class="field">
              <span class="field-label">Дата</span>
              <input v-model="form.date" class="field-input" type="date" name="date" required />
            </label>

            <label class="field">
              <span class="field-label">Время</span>
              <input v-model="form.time" class="field-input" type="time" name="time" required />
            </label>
          </div>

          <p class="contact-note">
            Свяжемся в выбранные дату и время (или предложим ближайший свободный слот).
          </p>

          <button class="btn btn-primary" type="submit" :disabled="isDisabled">
            Отправить заявку
          </button>

          <!-- если хочешь оставить почту/телефон текстом — можно компактно снизу -->
          <p class="contact-alt">
            или напишите: <a href="mailto:hello@ikb.studio">hello@ikb.studio</a>
          </p>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, computed } from "vue";

const form = reactive({
  name: "",
  phone: "",
  date: "",
  time: "",
});

const isDisabled = computed(() => {
  return !form.name || !form.phone || !form.date || !form.time;
});

// По умолчанию отправляем в почту (без бэкенда).
// Если у тебя есть API — скажи, я переделаю на fetch.
function submit() {
  const subject = encodeURIComponent("Запрос на звонок — IKB");
  const body = encodeURIComponent(
    [
      `Имя: ${form.name}`,
      `Телефон: ${form.phone}`,
      `Дата: ${form.date}`,
      `Время: ${form.time}`,
    ].join("\n")
  );

  window.location.href = `mailto:hello@ikb.studio?subject=${subject}&body=${body}`;
}
</script>

<style scoped>
   .section-title {
  color: rgb(214, 193, 142);
}

  .contact-form {
  display: grid;
  gap: 12px;
  margin-top: 10px;
}

/* Вся зона поля кликабельная */
.field {
  display: grid;
  gap: 6px;
  cursor: pointer;
}

.field-label {
  font-size: 12px;
  opacity: 0.75;
  letter-spacing: 0.02em;
  cursor: pointer;
}

/* Инпуты кликабельные и с подсветкой */
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

/* Чтобы на текстовых полях был I-beam, но на date/time всё равно pointer */
.field-input[type="text"],
.field-input[type="tel"],
.field-input[type="email"],
.field-input[type="search"],
.field-input[type="password"],
.field-input[type="url"],
.field-input[type="number"] {
  cursor: text;
}

/* Активное/фокус/клик — цвет #CFAD66 */
.field-input:focus,
.field-input:focus-visible,
.field-input:active {
  border-color: rgba(207, 173, 102, 0.75);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 3px rgba(207, 173, 102, 0.18);
}

/* Подсветка при наведении */
.field:hover .field-input {
  border-color: rgba(207, 173, 102, 0.35);
}

/* Для date/time иконки календаря/часов тоже кликабельные */
.field-input::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.85;
}

/* Кнопка и ссылки — pointer */
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
  opacity: 0.72;
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
/* Минимальный “обвес”, чтобы инпуты выглядели в стиле glass-card и не ломали палитру */
.contact-form {
  display: grid;
  gap: 12px;
  margin-top: 10px;
}

.field {
  display: grid;
  gap: 6px;
}

.field-label {
  font-size: 12px;
  opacity: 0.75;
  letter-spacing: 0.02em;
}

.field-input {
  width: 100%;
  padding: 12px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.06);
  color: inherit;
  outline: none;
  transition: border-color 160ms ease, background 160ms ease, transform 160ms ease;
}

.field-input:focus {
  border-color: rgba(255, 255, 255, 0.28);
  background: rgba(255, 255, 255, 0.08);
}

.row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.contact-note {
  margin: 2px 0 0;
  font-size: 13px;
  opacity: 0.72;
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
