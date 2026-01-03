import { computed } from 'vue'
import { translations, type Locale } from '~/content/translations'

const STORAGE_KEY = 'locale'
const LEGACY_KEYS = ['ikb-locale']
const DEFAULT_LOCALE: Locale = 'ru'

const isLocale = (value: string | null | undefined): value is Locale => value === 'ru' || value === 'en'

const useLocaleState = () => useState<Locale>('locale', () => DEFAULT_LOCALE)
const useLocaleInitState = () => useState<boolean>('locale-initialized', () => false)

const readStoredLocale = (): Locale => {
  if (!process.client) return DEFAULT_LOCALE

  const legacy = LEGACY_KEYS.map((key) => localStorage.getItem(key)).find(isLocale)
  if (legacy) {
    localStorage.setItem(STORAGE_KEY, legacy)
    LEGACY_KEYS.forEach((key) => key !== STORAGE_KEY && localStorage.removeItem(key))
    return legacy
  }

  const stored = localStorage.getItem(STORAGE_KEY)
  if (isLocale(stored)) return stored

  localStorage.setItem(STORAGE_KEY, DEFAULT_LOCALE)
  LEGACY_KEYS.forEach((key) => key !== STORAGE_KEY && localStorage.removeItem(key))
  return DEFAULT_LOCALE
}

const persistLocale = (value: Locale) => {
  if (!process.client) return
  localStorage.setItem(STORAGE_KEY, value)
  LEGACY_KEYS.forEach((key) => key !== STORAGE_KEY && localStorage.removeItem(key))
}

const getByPath = (target: Record<string, any>, path: string) => {
  return path.split('.').reduce<any>((acc, part) => {
    if (acc === undefined || acc === null) return undefined
    if (typeof acc !== 'object') return undefined
    return acc[part]
  }, target)
}

export const useLocale = () => {
  const locale = useLocaleState()
  const initialized = useLocaleInitState()

  if (!initialized.value && process.client) {
    locale.value = readStoredLocale()
    initialized.value = true
  }

  const setLocale = (value: Locale) => {
    if (!isLocale(value)) return
    if (locale.value === value) return
    locale.value = value
    persistLocale(value)
  }

  const dictionary = computed(() => translations[locale.value] ?? translations[DEFAULT_LOCALE])

  const t = (path: string) => {
    const current = getByPath(dictionary.value, path)
    if (current !== undefined) return current

    const fallback = getByPath(translations[DEFAULT_LOCALE], path)
    if (fallback !== undefined) return fallback

    if (process.dev) {
      console.warn(`[i18n] missing translation key: ${path}`)
    }
    return path
  }

  return { locale, setLocale, t, dictionary }
}
