<template>
  <div class="grid" style="gap:16px">
    <NuxtLink to="/" class="btn ghost">← Назад</NuxtLink>

    <div class="card" v-if="org">
      <div class="card-row">
        <img v-if="org.logo" :src="org.logo" class="logo" />
        <div class="grid" style="gap:6px">
          <div class="h1">{{ org.name }}</div>
          <div class="kv"><span class="k">BIN</span><span class="v">{{ org.bin }}</span></div>
          <div>
            <span v-for="lic in org.licenses" :key="lic.id" class="badge ok">{{ lic.code }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isAdmin" class="card">
      <div class="h2">Редактировать</div>
      <form class="form" @submit.prevent="save">
        <fieldset>
          <label class="label">Название</label>
          <input v-model="form.name" class="input" required />
        </fieldset>
        <fieldset>
          <label class="label">BIN</label>
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
          <label class="label">Сменить логотип</label>
          <input class="file" type="file" accept="image/*" @change="onFile" />
          <div v-if="preview" style="margin-top:8px">
            <img :src="preview" class="logo" />
          </div>
        </fieldset>
        <div class="actions">
          <button class="btn" :disabled="saving">
            <span v-if="saving" class="spinner"></span>
            <span v-else>Сохранить</span>
          </button>
          <button type="button" class="btn danger" @click="del">Удалить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const route = useRoute()
const { isAdmin, access } = useAuth()

const org = ref(null)
const licenses = ref([])
const form = reactive({ name:"", bin:"", license_ids:[], logo:null })
const preview = ref(null)
const saving = ref(false)

const load = async () => {
  const [o, lic] = await Promise.all([
    $fetch(`${config.public.apiBase}/orgs/${route.params.id}/`, { headers:{ Authorization:`Bearer ${access.value}` }}),
    $fetch(`${config.public.apiBase}/licenses/?limit=1000`, { headers:{ Authorization:`Bearer ${access.value}` }}),
  ])
  org.value = o
  licenses.value = lic.results ?? lic
  form.name = o.name; form.bin = o.bin; form.license_ids = o.licenses.map(l=>l.id); form.logo=null; preview.value=null
}
const onFile = (e)=>{ const f=e.target.files?.[0]; form.logo=f||null; preview.value=f?URL.createObjectURL(f):null }

const save = async () => {
  saving.value = true
  try {
    let body
    if (form.logo){
      const fd = new FormData()
      fd.append("name",form.name); fd.append("bin",form.bin)
      form.license_ids.forEach(id=>fd.append("license_ids",String(id)))
      fd.append("logo",form.logo); body=fd
    } else {
      body = { name:form.name, bin:form.bin, license_ids:form.license_ids }
    }
    await $fetch(`${config.public.apiBase}/orgs/${org.value.id}/`, { method:"PATCH", body,
      headers:{ Authorization:`Bearer ${access.value}` } })
    await load()
  } finally { saving.value = false }
}

const del = async () => {
  if(!confirm("Удалить организацию?")) return
  await $fetch(`${config.public.apiBase}/orgs/${org.value.id}/`, { method:"DELETE", headers:{ Authorization:`Bearer ${access.value}` }})
  navigateTo("/")
}

onMounted(load)
</script>
