export default defineNuxtRouteMiddleware(async (to) => {
  const publicPaths = ["/login", "/register"]  
  if (publicPaths.includes(to.path)) return

  const access = useState("access", () => (process.client ? localStorage.getItem("access") : null))
  const user = useState("user", () => null)

  if (!access.value) return navigateTo("/login")

  if (!user.value) {
    try {
      const config = useRuntimeConfig()
      const me = await $fetch(`${config.public.apiBase}/auth/me/`, {
        headers: { Authorization: `Bearer ${access.value}` },
      })
      user.value = me
    } catch (e) {
      access.value = null
      if (process.client) { localStorage.removeItem("access"); localStorage.removeItem("refresh") }
      return navigateTo("/login")
    }
  }
})
