export default defineNuxtConfig({
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api",
    },
  },
  app: {
    head: {
      title: "Fin Catalog",
      meta: [{ name: "viewport", content: "width=device-width, initial-scale=1" }],
    },
  },
})


