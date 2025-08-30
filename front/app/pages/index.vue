<template>
  <div class="grid" style="gap:16px">
    <!-- Фильтр -->
    <div class="card">
      <div class="row" style="gap:12px; align-items:flex-end">
        <fieldset style="flex:1">
          <label class="label">Поиск по названию</label>
          <input v-model="q" class="input" placeholder="Напр. 'Банк'" />
        </fieldset>
        <button class="btn ghost" @click="apply">Найти</button>
        <button class="btn ghost" @click="reset">Сброс</button>
      </div>
    </div>

    <!-- Форма добавления (только админ) -->
    <div v-if="isAdmin" class="card">
      <div class="h2">Добавить организацию</div>
      <form class="form" @submit.prevent="createOrg">
        <fieldset>
          <label class="label">Название</label>
          <input v-model="form.name" class="input" required />
        </fieldset>
        <fieldset>
          <label class="label">BIN (12 цифр)</label>
          <input v-model="form.bin" class="input" required />
        </fieldset>
        <fieldset>
          <label class="label">Лицензии</label>
          <div class="row" style="flex-wrap:wrap">
            <label v-for="lic in licenses" :key="lic.id" class="row" style="gap:6px">
              <input class="checkbox" type="checkbox" :value="lic.id" v-model="form.license_ids">
              <span class="helper">{{ lic.code }}</span>
            </label>
          </div>
        </fieldset>
        <fieldset>
          <label class="label">Логотип (опционально)</label>
          <input class="file" type="file" accept="image/*" @change="onFile" />
          <div v-if="preview" style="margin-top:8px">
            <img :src="preview" class="logo" />
          </div>
        </fieldset>
        <div class="actions-row">
          <button class="btn" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Создать</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Список -->
    <div v-if="items.length" class="grid cards">
      <OrgCard v-for="o in items" :key="o.id" :org="o">
        <NuxtLink v-if="isAdmin" :to="`/org/${o.id}`" class="btn ghost">Редактировать</NuxtLink>
      </OrgCard>
    </div>
    <div v-else class="card empty">Нет организаций</div>
  </div>
</template>

<script setup>
import OrgCard from "~/components/OrgCard.vue"
const config = useRuntimeConfig()
const { isAdmin, access } = useAuth()

const q = ref("")
const items = ref([])
const licenses = ref([])
const loading = ref(false)
const form = reactive({ name:"", bin:"", license_ids:[], logo:null })
const preview = ref(null)

const load = async () => {
  const qs = q.value ? `?name=${encodeURIComponent(q.value)}` : ""
  const res = await $fetch(`${config.public.apiBase}/orgs/${qs}`, { headers:{ Authorization:`Bearer ${access.value}` }})
  items.value = res.results ?? res
}
const loadLicenses = async () => {
  const res = await $fetch(`${config.public.apiBase}/licenses/?limit=1000`, { headers:{ Authorization:`Bearer ${access.value}` }})
  licenses.value = res.results ?? res
}
const apply = () => load()
const reset = () => { q.value=""; load() }
const onFile = (e) => { const f=e.target.files?.[0]; form.logo=f||null; preview.value=f?URL.createObjectURL(f):null }
const createOrg = async () => {
  loading.value = true
  try {
    let body
    if (form.logo){
      const fd=new FormData()
      fd.append("name", form.name); fd.append("bin", form.bin)
      form.license_ids.forEach(id=>fd.append("license_ids", String(id)))
      fd.append("logo", form.logo); body=fd
    } else {
      body = { name:form.name, bin:form.bin, license_ids:form.license_ids }
    }
    await $fetch(`${config.public.apiBase}/orgs/`, { method:"POST", body, headers:{ Authorization:`Bearer ${access.value}` }})
    form.name=""; form.bin=""; form.license_ids=[]; form.logo=null; preview.value=null
    await load()
  } finally { loading.value = false }
}
onMounted(()=>{ load(); loadLicenses() })
</script>
