# Ключи контента и примеры JSON для поля `extra`

Ключ передаётся в `ContentBlock.key`, локаль — `ru` или `en`.

- `header`: `extra` пример  
```json
{
  "logoTagline": "Engineering bureau",
  "nav": ["Philosophy", "Method", "Capabilities", "Trust", "Projects", "Contacts"],
  "cta": "Book a call",
  "menuTitle": "Navigation",
  "menuClose": "Close menu",
  "menuOpenLabel": "Open menu",
  "languageLabel": "Change language",
  "languageShort": { "ru": "RU", "en": "EN" }
}
```

- `hero`: `title` — заголовок, `body` — lead, `extra` пример  
```json
{
  "eyebrow": "IKB — contract engineering & R&D",
  "ctas": { "primary": "Schedule a call", "secondary": "View projects" },
  "metrics": [{ "value": "18+ years", "label": "of engineering practice" }],
  "notes": [{ "title": "Complex systems", "body": "..." }]
}
```

- `values`: `title` — заголовок секции, `extra.cards` — список  
```json
{ "eyebrow": "Philosophy", "cards": [{ "title": "Systems approach", "body": "..." }] }
```

- `approach`: `body` — lead, `extra.steps` — список шагов  
```json
{ "eyebrow": "Method", "steps": [{ "title": "NDA & kickoff", "body": "..." }] }
```

- `competencies`: `extra.cards` — список навыков  
```json
{ "eyebrow": "Capabilities", "cards": [{ "title": "Mechatronics", "body": "..." }] }
```

- `trust`: `body` — lead, `extra.cards` — карточки доверия  
```json
{ "eyebrow": "Trust", "cards": [{ "title": "Quality system", "body": "..." }] }
```

- `projects`: `title/body` — заголовок/лид; сами проекты заводятся отдельно в `ProjectItem`.  
`extra.labels` можно задать тексты для фильтров (domain/stage/search/reset/empty/results).

- `contacts`: поля формы и копирайты  
```json
{
  "eyebrow": "Contacts",
  "formTitle": "Book a consultation",
  "fields": {
    "name": { "label": "Name", "placeholder": "How should we address you?" },
    "phone": { "label": "Phone", "placeholder": "+1..." },
    "date": { "label": "Date", "placeholder": "" },
    "time": { "label": "Time", "placeholder": "" }
  },
  "note": "We keep your data safe",
  "button": "Send",
  "alt": "Or email:",
  "mailSubject": "Consultation request — IKB",
  "mailLabels": { "name": "Name", "phone": "Phone", "date": "Date", "time": "Time" }
}
```

- `certificates`: `title/body` — заголовок/лид; карточки создаются в `CertificateItem`.  
`extra.type_labels` задаёт подписи для бейджей; `extra.actions` — кнопки просмотра.
