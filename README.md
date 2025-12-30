# Nuxt Minimal Starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

## Backend (Django)

Backend живёт в `backend/` и поднимает API/CMS для контента, проектов и сертификатов.

- Шаги запуска: `cd backend`, создать venv, `pip install -r requirements.txt`, скопировать `.env.example`, `python manage.py migrate`, `python manage.py createsuperuser`, `python manage.py runserver`.
- Swagger: `http://localhost:8000/api/docs/`, публичный payload: `/api/public/home/`, проекты: `/api/projects/`, сертификаты: `/api/certificates/`.
- Настройки CORS/DB/SECRET_KEY смотрите в `backend/.env.example`.

Фронтенд может брать API-базу из `NUXT_PUBLIC_API_BASE_URL` (см. `.env.example` в корне).
