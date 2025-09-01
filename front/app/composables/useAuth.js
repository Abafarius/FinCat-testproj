export const useAuth = () => {
  const config = useRuntimeConfig()
  const user = useState("user", () => null)
  const access = useState("access", () => (process.client ? localStorage.getItem("access") : null))
  const refresh = useState("refresh", () => (process.client ? localStorage.getItem("refresh") : null))

  const login = async (username, password) => {
    const data = await $fetch(`${config.public.apiBase}/auth/token/`, {
      method: "POST",
      body: { username, password },
    })
    access.value = data.access
    refresh.value = data.refresh
    if (process.client) {
      localStorage.setItem("access", data.access)
      localStorage.setItem("refresh", data.refresh)
    }
    const me = await $fetch(`${config.public.apiBase}/auth/me/`, {
      headers: { Authorization: `Bearer ${access.value}` },
    })
    user.value = me
  }

  // регистрация + автологин
  const register = async ({ username, email, password }) => {
    await $fetch(`${config.public.apiBase}/auth/register/`, {
      method: "POST",
      body: { username, email, password },
    })
    // сразу логиним
    await login(username, password)
  }

  const logout = () => {
    user.value = null
    access.value = null
    refresh.value = null
    if (process.client) { localStorage.removeItem("access"); localStorage.removeItem("refresh") }
  }

  const isAdmin = computed(() => !!user.value?.is_staff)
  return { user, access, refresh, login, register, logout, isAdmin }
}
