<template>
  <div>
    <nav class="navbar">
      <div class="navbar-inner container">
        <div class="brand">
          <span class="brand-badge">₸</span>
          <span>Fin Catalog</span>
        </div>
        <div class="row">
          <span v-if="user" class="muted">👤 {{ user.username }} <span v-if="user.is_staff">(admin)</span></span>
          <button class="btn ghost" @click="goLogout">Выйти</button>
        </div>
      </div>
    </nav>
    <main class="container">
      <slot />
    </main>
  </div>
</template>

<script setup>
const { user, logout } = useAuth()
const router = useRouter()
const goLogout = () => { logout(); router.push("/login") }
</script>
