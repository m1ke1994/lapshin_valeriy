import { computed } from 'vue'
import { translations } from '~/content/translations'
import { useLocale } from './useLocale'

export const useContent = () => {
  const { locale, setLocale, t, dictionary } = useLocale()

  const copy = computed(() => dictionary.value ?? translations.ru)

  return {
    locale,
    setLocale,
    copy,
    t,
  }
}
