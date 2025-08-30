// frontend/app/composables/useApi.ts
import axios, { AxiosError } from "axios"

let isRefreshing = false
let subscribers: Array<(t: string)=>void> = []

function onRefreshed(token: string) { subscribers.forEach(cb => cb(token)); subscribers = [] }
function addSubscriber(cb: (t:string)=>void) { subscribers.push(cb) }

export const useApi = () => {
  const config = useRuntimeConfig()
  const access = useState<string | null>("access", () => process.client ? localStorage.getItem("access") : null)
  const refresh = useState<string | null>("refresh", () => process.client ? localStorage.getItem("refresh") : null)

  const instance = axios.create({ baseURL: config.public.apiBase })

  instance.interceptors.request.use((req) => {
    if (access.value) req.headers.Authorization = `Bearer ${access.value}`
    return req
  })

  instance.interceptors.response.use(r => r, async (error: AxiosError) => {
    const original: any = error.config
    if (error.response?.status === 401 && refresh.value && !original._retry) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          addSubscriber((token) => {
            original.headers.Authorization = `Bearer ${token}`
            resolve(instance(original))
          })
        })
      }
      original._retry = true
      isRefreshing = true
      try {
        const resp = await axios.post(`${config.public.apiBase}/auth/refresh/`, { refresh: refresh.value })
        const newAccess = (resp.data as any).access
        access.value = newAccess
        if (process.client) localStorage.setItem("access", newAccess)
        isRefreshing = false
        onRefreshed(newAccess)
        original.headers.Authorization = `Bearer ${newAccess}`
        return instance(original)
      } catch (e) {
        isRefreshing = false
        // токены умерли — выходим
        const router = useRouter()
        access.value = null; refresh.value = null
        if (process.client) { localStorage.removeItem("access"); localStorage.removeItem("refresh") }
        router.push("/login")
      }
    }
    throw error
  })

  return instance
}
