// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
  css: ['~/assets/css/tailwind.css'],
  nitro: {
    routeRules: {
      '/bg/**': {
        headers: {
          'cache-control': 'public,max-age=31536000,immutable',
        },
      },
    },
  },
})
