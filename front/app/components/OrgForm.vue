<template>
  <form @submit.prevent="onSubmit" class="form">
    <fieldset>
      <label class="label">Название</label>
      <input v-model.trim="form.name" class="input" required />
    </fieldset>

    <fieldset>
      <label class="label">BIN (12 цифр)</label>
      <input
        v-model="form.bin"
        class="input"
        inputmode="numeric"
        maxlength="12"
        @input="digitsOnly"
        required
      />
      <div v-if="binError" class="helper" style="color:var(--danger)">{{ binError }}</div>
    </fieldset>

    <fieldset>
      <label class="label">Лицензии</label>
      <div class="row" style="flex-wrap:wrap; gap:8px">
        <label v-for="lic in licenses" :key="lic.id" class="row" style="gap:6px">
          <input class="checkbox" type="checkbox" :value="lic.id" v-model="form.license_ids" />
          <span class="helper">{{ lic.code }}</span>
        </label>
      </div>
    </fieldset>

    <fieldset>
      <label class="label">Логотип (png/jpg)</label>
      <input class="file" type="file" accept="image/*" @change="onFile" ref="fileEl" />
      <div v-if="preview" style="margin-top:8px">
        <img :src="preview" class="logo" />
      </div>
    </fieldset>

    <div class="actions">
      <button class="btn" :disabled="loading">
        <span v-if="loading" class="spinner"></span>
        <span v-else>{{ submitText || (isEdit ? 'Сохранить' : 'Создать') }}</span>
      </button>
      <button v-if="canReset" type="button" class="btn ghost" @click="$emit('cancel')">Отмена</button>
    </div>

    <p v-if="error" class="helper" style="color:var(--danger)">{{ error }}</p>
  </form>
</template>

<script setup>
const props = defineProps({
  initial: { type: Object, default: null },  // { id, name, bin, licenses:[{id,code}], logo? }
  submitText: { type: String, default: "" },
  canReset: { type: Boolean, default: false },
})
const emit = defineEmits(["submitted", "cancel"])

const config = useRuntimeConfig()
const { access } = useAuth()

const isEdit = computed(() => !!props.initial?.id)
const licenses = ref([])
const loading = ref(false)
const error = ref("")
const binError = ref("")
const fileEl = ref(null)

const form = reactive({
  name: props.initial?.name || "",
  bin: props.initial?.bin || "",
  license_ids: props.initial?.licenses?.map(l => l.id) || [],
  logo: null, // File | null
})

const preview = ref(null)

onMounted(async () => {
  // Подтянуть список лицензий
  const resLic = await $fetch(`${config.public.apiBase}/licenses/?limit=1000`, {
    headers: { Authorization: `Bearer ${access.value}` },
  })
  licenses.value = resLic.results ?? resLic

  // Если редактирование — не показываем текущий логотип как превью (его уже видно в карточке)
  preview.value = null
})

function digitsOnly(e) {
  const v = e.target.value.replace(/\D+/g, "").slice(0, 12)
  form.bin = v
  binError.value = v.length === 0 ? "" : (v.length !== 12 ? "BIN должен состоять из 12 цифр" : "")
}

function onFile(e) {
  const file = e.target.files?.[0]
  form.logo = file || null
  preview.value = file ? URL.createObjectURL(file) : null
}

async function onSubmit() {
  error.value = ""

  // простая валидация BIN
  if (!/^\d{12}$/.test(form.bin)) {
    binError.value = "BIN должен состоять из 12 цифр"
    return
  }

  loading.value = true
  try {
    let body
    if (form.logo) {
      const fd = new FormData()
      fd.append("name", form.name)
      fd.append("bin", form.bin)
      form.license_ids.forEach(id => fd.append("license_ids", String(id)))
      fd.append("logo", form.logo)
      body = fd
    } else {
      body = { name: form.name, bin: form.bin, license_ids: form.license_ids }
    }

    const url = isEdit.value
      ? `${config.public.apiBase}/orgs/${props.initial.id}/`
      : `${config.public.apiBase}/orgs/`

    const method = isEdit.value ? "PATCH" : "POST"

    const org = await $fetch(url, {
      method,
      body,
      headers: { Authorization: `Bearer ${access.value}` },
    })

    // очистка локального состояния (если это форма создания)
    if (!isEdit.value) {
      form.name = ""
      form.bin = ""
      form.license_ids = []
      form.logo = null
      preview.value = null
      if (fileEl.value) fileEl.value.value = "" // сброс input[type=file]
    }

    emit("submitted", org)
  } catch (e) {
    // покажем сообщение сервера, если есть
    error.value = (e?.data && (typeof e.data === "string" ? e.data : JSON.stringify(e.data))) || "Ошибка сохранения"
  } finally {
    loading.value = false
  }
}
</script>


