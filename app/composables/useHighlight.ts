import { computed } from 'vue'
import { useLocale } from './useLocale'

const escapeRegex = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

export const useHighlight = () => {
  const { locale } = useLocale()

  const keywords = computed(() =>
    locale.value === 'ru'
      ? [
          'NDA',
          'R&D',
          'инжен',
          'продукт',
          'система',
          'серия',
          'качество',
          'конфиден',
          'безопас',
          'консультац',
          'проект',
        ]
      : ['NDA', 'R&D', 'engineering', 'product', 'system', 'prototype', 'series', 'quality', 'confidential', 'safety', 'consultation', 'project']
  )

  const regex = computed(() => {
    const words = keywords.value.filter(Boolean).map(escapeRegex)
    if (!words.length) return null
    return new RegExp(`(${words.join('|')})`, 'gi')
  })

  const highlight = (text: string) => {
    if (!text || typeof text !== 'string') return text
    const re = regex.value
    if (!re) return text
    return text.replace(re, '<span class="ikb-highlight">$1</span>')
  }

  return { highlight }
}
