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
          'инженерия',
          'инженерные',
          'инженерный',
          'продукт',
          'продукты',
          'продукта',
          'система',
          'системы',
          'системный',
          'серия',
          'серийный',
          'серийные',
          'прототип',
          'прототипы',
          'качество',
          'качественный',
          'конфиденциальность',
          'конфиденциальный',
          'безопасность',
          'безопасный',
          'консультация',
          'консультации',
          'проект',
          'проекты',
        ]
      : [
          'NDA',
          'R&D',
          'engineering',
          'engineered',
          'engineers',
          'product',
          'products',
          'system',
          'systems',
          'prototype',
          'prototypes',
          'series',
          'serial',
          'quality',
          'confidential',
          'confidentiality',
          'safety',
          'secure',
          'consultation',
          'consult',
          'project',
          'projects',
        ]
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
