import { computed, onMounted } from 'vue'
import { translations, type Locale } from '~/content/translations'

const STORAGE_KEY = 'ikb-locale'

const isLocale = (value: string | null): value is Locale => value === 'ru' || value === 'en'

export const useLocaleState = () => useState<Locale>('locale', () => 'ru')

export const useLocale = () => {
  const locale = useLocaleState()
  const initialized = useState<boolean>('locale-initialized', () => false)

  const setLocale = (value: Locale) => {
    locale.value = value
    if (process.client) {
      localStorage.setItem(STORAGE_KEY, value)
    }
  }

  onMounted(() => {
    if (initialized.value) return
    initialized.value = true

    if (!process.client) return
    const saved = localStorage.getItem(STORAGE_KEY)
    if (isLocale(saved)) {
      locale.value = saved
    }
  })

  const t = computed(() => translations[locale.value])

  return { locale, setLocale, t }
}
