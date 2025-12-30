import { useRuntimeConfig, useFetch } from '#imports'

export const useApiBase = () => {
  const config = useRuntimeConfig()
  return (config.public?.apiBaseUrl as string) || ''
}

export const useApiFetch = async <T>(path: string, options: Parameters<typeof useFetch<T>>[1] = {}) => {
  const baseUrl = useApiBase()
  const url = path.startsWith('http') ? path : `${baseUrl}${path}`

  if (!url) {
    throw new Error('API base URL is not configured. Set NUXT_PUBLIC_API_BASE_URL.')
  }

  const { data, error } = await useFetch<T>(url, { watch: false, ...options })
  if (error.value) {
    throw error.value
  }

  return data.value as T
}
