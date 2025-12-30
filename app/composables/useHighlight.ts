import { computed } from 'vue'
import { useLocale } from './useLocale'

const escapeRegex = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

export const useHighlight = () => {
  const { locale } = useLocale()

  const keywords = computed(() => {
    const ru = [
      'NDA',
      'R&D',
      'инженерия',
      'инженерный',
      'инженерные',
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
    const en = [
      'NDA',
      'R&D',
      'engineering',
      'engineered',
      'engineer',
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
    const base = locale.value === 'ru' ? ru : en
    return Array.from(new Set(base)).sort((a, b) => b.length - a.length)
  })

  const regex = computed(() => {
    const words = keywords.value.filter(Boolean).map(escapeRegex)
    if (!words.length) return null
    return new RegExp(`(?<![\\p{L}\\p{N}])(${words.join('|')})(?![\\p{L}\\p{N}])`, 'giu')
  })

  const highlight = (text: string) => {
    if (!text || typeof text !== 'string') return text
    const re = regex.value
    if (!re) return text
    return text.replace(re, '<span class="ikb-highlight">$1</span>')
  }

  return { highlight }
}
