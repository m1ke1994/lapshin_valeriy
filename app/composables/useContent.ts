import { computed } from 'vue'
import { useFetch } from '#app'
import { translations, type Locale } from '~/content/translations'
import { useLocale } from './useLocale'

type ApiSectionItem = {
  item_type: string
  title_ru?: string
  title_en?: string
  text_ru?: string
  text_en?: string
  value_ru?: string
  value_en?: string
  is_enabled?: boolean
}

type ApiSection = {
  type: string
  title_ru?: string
  title_en?: string
  subtitle_ru?: string
  subtitle_en?: string
  body_ru?: string
  body_en?: string
  button_text_ru?: string
  button_text_en?: string
  button_link?: string
  is_enabled?: boolean
  items?: ApiSectionItem[]
}

type ApiProject = {
  title_ru?: string
  title_en?: string
  description_ru?: string
  description_en?: string
  category_ru?: string
  category_en?: string
  stage_ru?: string
  stage_en?: string
  tags_ru?: string
  tags_en?: string
  link?: string
  image_url?: string | null
  is_published?: boolean
}

type ApiCertificate = {
  title_ru?: string
  title_en?: string
  issuer_ru?: string
  issuer_en?: string
  year?: number | null
  description_ru?: string
  description_en?: string
  image_url?: string | null
  is_published?: boolean
}

type ApiSite = {
  settings?: {
    site_name_ru?: string
    site_name_en?: string
    header_cta_text_ru?: string
    header_cta_text_en?: string
    header_cta_link?: string
    email?: string
    phone?: string
    address?: string
  }
  sections: ApiSection[]
  projects: ApiProject[]
  certificates: ApiCertificate[]
}

const defaultContent = translations

const clone = <T>(value: T): T => JSON.parse(JSON.stringify(value))

const pickLocale = (obj: Record<string, any> | undefined, locale: Locale, base?: any) =>
  (locale === 'en' ? obj?.en : obj?.ru) ?? base ?? ''

const getLocaleValue = (section: ApiSection | undefined, field: 'title' | 'subtitle' | 'body' | 'button_text', locale: Locale) => {
  const map = {
    title: locale === 'en' ? section?.title_en : section?.title_ru,
    subtitle: locale === 'en' ? section?.subtitle_en : section?.subtitle_ru,
    body: locale === 'en' ? section?.body_en : section?.body_ru,
    button_text: locale === 'en' ? section?.button_text_en : section?.button_text_ru,
  }
  return map[field] || ''
}

const splitTags = (value?: string | null) =>
  (value || '')
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean)

const mapApiToContent = (api: ApiSite | null | undefined) => {
  if (!api) return null
  const sectionsMap = new Map<string, ApiSection>()
  for (const section of api.sections || []) {
    if (section.is_enabled === false) continue
    sectionsMap.set(section.type, section)
  }

  const buildLocale = (locale: Locale) => {
    const fallback = clone(defaultContent[locale] ?? defaultContent.ru)

    // header from settings
    if (api.settings) {
      const header = fallback.header
      if (locale === 'en') {
        header.logoTagline = api.settings.site_name_en || header.logoTagline
        header.cta = api.settings.header_cta_text_en || header.cta
      } else {
        header.logoTagline = api.settings.site_name_ru || header.logoTagline
        header.cta = api.settings.header_cta_text_ru || header.cta
      }
    }

    const applyTextSection = (type: string, targetKey: keyof typeof fallback) => {
      const apiSection = sectionsMap.get(type)
      if (!apiSection) return
      const section = (fallback as any)[targetKey] || {}
      section.eyebrow = getLocaleValue(apiSection, 'subtitle', locale) || section.eyebrow
      section.title = getLocaleValue(apiSection, 'title', locale) || section.title
      const body = getLocaleValue(apiSection, 'body', locale)
      if (body) {
        if ('lead' in section) section.lead = body
        else section.body = body
      }
      const btn = getLocaleValue(apiSection, 'button_text', locale)
      if (btn && section.ctas) section.ctas.primary = btn
    }

    applyTextSection('hero', 'hero')
    applyTextSection('values', 'values')
    applyTextSection('approach', 'approach')
    applyTextSection('competencies', 'competencies')
    applyTextSection('trust', 'trust')
    applyTextSection('projects', 'projects')
    applyTextSection('contacts', 'contacts')
    applyTextSection('certificates', 'certificates')

    // Hero items
    const heroApi = sectionsMap.get('hero')
    if (heroApi?.items?.length) {
      const metrics = heroApi.items
        .filter((i) => i.item_type === 'metric' && i.is_enabled !== false)
        .map((i) => ({
          value: locale === 'en' ? i.title_en || i.value_en || '' : i.title_ru || i.value_ru || '',
          label: locale === 'en' ? i.text_en || '' : i.text_ru || '',
        }))
      if (metrics.length) fallback.hero.metrics = metrics

      const notes = heroApi.items
        .filter((i) => i.item_type === 'note' && i.is_enabled !== false)
        .map((i) => ({
          title: locale === 'en' ? i.title_en || '' : i.title_ru || '',
          body: locale === 'en' ? i.text_en || '' : i.text_ru || '',
        }))
      if (notes.length) fallback.hero.notes = notes
    }

    const mapCards = (type: string, targetKey: keyof typeof fallback, itemType: 'cards' | 'steps' = 'cards') => {
      const apiSection = sectionsMap.get(type)
      if (!apiSection?.items?.length) return
      const cards = apiSection.items
        .filter((i) => i.is_enabled !== false)
        .map((i) => ({
          title: locale === 'en' ? i.title_en || '' : i.title_ru || '',
          body: locale === 'en' ? i.text_en || '' : i.text_ru || '',
        }))
      if (cards.length) {
        const target = (fallback as any)[targetKey]
        target[itemType] = cards
      }
    }

    mapCards('values', 'values')
    mapCards('approach', 'approach', 'steps')
    mapCards('competencies', 'competencies')
    mapCards('trust', 'trust')

    // Projects
    const projects = (api.projects || []).filter((p) => p.is_published !== false)
    if (projects.length) {
      (fallback as any).projects.cards = projects.map((p) => {
        const title = locale === 'en' ? p.title_en || p.title_ru || '' : p.title_ru || p.title_en || ''
        const description =
          locale === 'en' ? p.description_en || p.description_ru || '' : p.description_ru || p.description_en || ''
        const category = locale === 'en' ? p.category_en || p.category_ru || '' : p.category_ru || p.category_en || ''
        const stage = locale === 'en' ? p.stage_en || p.stage_ru || '' : p.stage_ru || p.stage_en || ''
        const tags = locale === 'en' ? splitTags(p.tags_en) : splitTags(p.tags_ru)
        const metaParts = [category, stage].filter(Boolean)
        return {
          title,
          body: description,
          meta: metaParts.join(' / ') || '',
          category,
          stage,
          tags,
          image_url: p.image_url || null,
          image: p.image_url || null,
        }
      })
    }

    // Certificates
    const certs = (api.certificates || []).filter((c) => c.is_published !== false)
    if (certs.length) {
      (fallback as any).certificates.items = certs.map((c, idx) => ({
        id: `cert-${idx}`,
        src: c.image_url || c.image || '',
        title: locale === 'en' ? c.title_en || c.title_ru || '' : c.title_ru || c.title_en || '',
        subtitle: locale === 'en' ? c.issuer_en || c.issuer_ru || '' : c.issuer_ru || c.issuer_en || '',
        type: 'certificate',
      }))
    }

    return fallback
  }

  return {
    ru: buildLocale('ru'),
    en: buildLocale('en'),
  }
}

export const useContent = () => {
  const { locale, setLocale, t, dictionary } = useLocale()

  const remoteContent = useState<Record<Locale, any> | null>('remote-content', () => null)
  const isLoading = useState<boolean>('content-loading', () => false)
  const loadError = useState<any>('content-error', () => null)
  const initialized = useState<boolean>('content-init', () => false)

  const loadSiteContent = async (force = false) => {
    if (isLoading.value) return
    if (initialized.value && !force) return
    isLoading.value = true
    try {
      const { data, error } = await useFetch<ApiSite>('/api/site/', { watch: false })
      if (error.value) throw error.value
      const mapped = mapApiToContent(data.value || null)
      if (mapped) remoteContent.value = mapped as Record<Locale, any>
      loadError.value = null
    } catch (err) {
      loadError.value = err
      if (process.dev) {
        console.warn('[content] fallback to defaults', err)
      }
    } finally {
      isLoading.value = false
      initialized.value = true
    }
  }

  if (!initialized.value && process.client) {
    loadSiteContent()
  }

  const copy = computed(() => {
    return remoteContent.value?.[locale.value] ?? dictionary.value ?? defaultContent.ru
  })

  return {
    locale,
    setLocale,
    copy,
    t,
    isLoading,
    loadError,
    refresh: (force = true) => loadSiteContent(force),
  }
}
