<template>
  <div class="container" style="max-width:480px">
    <div class="card">
      <div class="h1" style="margin-bottom:12px">Регистрация</div>
      <form class="form" @submit.prevent="submit">
        <fieldset>
          <label class="label">Логин (username)</label>
          <input v-model.trim="username" class="input" required />
        </fieldset>
        <fieldset>
          <label class="label">Email (необязательно)</label>
          <input v-model.trim="email" class="input" type="email" placeholder="you@example.com" />
        </fieldset>
        <fieldset>
          <label class="label">Пароль</label>
          <input v-model="password" class="input" type="password" required minlength="8" />
          <div class="helper">Минимум 8 символов</div>
        </fieldset>
        <fieldset>
          <label class="label">Повторите пароль</label>
          <input v-model="password2" class="input" type="password" required />
          <div v-if="mismatch" class="helper" style="color:var(--danger)">Пароли не совпадают</div>
        </fieldset>

        <div class="actions">
          <button class="btn" :disabled="loading || mismatch">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Создать аккаунт</span>
          </button>
          <NuxtLink to="/login" class="btn ghost">У меня уже есть аккаунт</NuxtLink>
        </div>

        <p v-if="error" class="helper" style="color:var(--danger)">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
const { register } = useAuth()
const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")
const password2 = ref("")
const loading = ref(false)
const error = ref("")

const mismatch = computed(() => password.value && password2.value && password.value !== password2.value)

const submit = async () => {
  if (mismatch.value) return
  loading.value = true; error.value = ""
  try {
    await register({ username: username.value, email: email.value || undefined, password: password.value })
    router.push("/") // автологин → сразу на главную
  } catch (e) {
    // покажем сообщение от бэка, если есть
    const msg = (e?.data && JSON.stringify(e.data)) || "Ошибка регистрации"
    error.value = msg
  } finally {
    loading.value = false
  }
}
</script>
