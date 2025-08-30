<template>
  <div class="container" style="max-width:440px">
    <div class="card">
      <div class="h1" style="margin-bottom:12px">Вход</div>
      <form class="form" @submit.prevent="submit">
        <fieldset>
          <label class="label">Логин</label>
          <input v-model="username" class="input" required />
        </fieldset>
        <fieldset>
          <label class="label">Пароль</label>
          <input v-model="password" type="password" class="input" required />
        </fieldset>
        <div class="actions-row">
          <button class="btn" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Войти</span>
          </button>
          <NuxtLink to="/register" class="btn ghost">Создать аккаунт</NuxtLink>
        </div>
        <p v-if="error" class="helper" style="color:var(--danger)">Неверный логин или пароль</p>
      </form>
    </div>
  </div>
</template>

<script setup>
const { login } = useAuth()
const router = useRouter()
const username = ref("")
const password = ref("")
const loading = ref(false)
const error = ref(false)

const submit = async () => {
  loading.value = true; error.value = false
  try { await login(username.value, password.value); router.push("/") }
  catch { error.value = true }
  finally { loading.value = false }
}
</script>
