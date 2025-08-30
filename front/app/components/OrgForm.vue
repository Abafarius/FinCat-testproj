<!-- frontend/app/components/OrgForm.vue -->
<template>
  <form @submit.prevent="onSubmit" class="space-y-3">
    <div>
      <label class="block text-sm">Название</label>
      <input v-model="form.name" class="border rounded px-3 py-2 w-full" required />
    </div>
    <div>
      <label class="block text-sm">BIN (12 цифр)</label>
      <input v-model="form.bin" class="border rounded px-3 py-2 w-full" required />
    </div>

    <div>
      <label class="block text-sm">Лицензии</label>
      <div class="flex flex-wrap gap-2">
        <label v-for="lic in licenses" :key="lic.id" class="inline-flex items-center gap-1">
          <input type="checkbox" :value="lic.id" v-model="form.license_ids">
          <span class="text-sm">{{ lic.code }}</span>
        </label>
      </div>
    </div>

    <div>
      <label class="block text-sm">Логотип (png/jpg)</label>
      <input type="file" accept="image/*" @change="onFile" />
      <div v-if="preview" class="mt-2">
        <img :src="preview" class="h-16 object-contain border rounded" />
      </div>
    </div>

    <div class="flex gap-2">
      <button class="bg-black text-white px-4 py-2 rounded" :disabled="loading">
        {{ submitText }}
      </button>
      <button v-if="canReset" type="button" @click="$emit('cancel')" class="px-4 py-2 border rounded">Отмена</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useOrgs } from "~/composables/useOrgs"
import type { Org } from "~/composables/useOrgs"

const props = defineProps<{
  initial?: Org | null,
  submitText?: string,
  canReset?: boolean
}>()

const emit = defineEmits<{ (e:"submitted", org:Org):void; (e:"cancel"):void }>()
const { listLicenses, createOrg, updateOrg } = useOrgs()

const licenses = ref<any[]>([])
const loading = ref(false)
const form = reactive<{ name:string; bin:string; license_ids:number[]; logo?:File | null }>({
  name: props.initial?.name || "",
  bin: props.initial?.bin || "",
  license_ids: props.initial?.licenses?.map(l => l.id) || [],
  logo: null
})
const preview = ref<string | null>(null)

onMounted(async () => {
  const res = await listLicenses()
  licenses.value = res.results ?? res
})

function onFile(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  form.logo = file || null
  if (file) preview.value = URL.createObjectURL(file)
}

async function onSubmit() {
  loading.value = true
  try {
    // если есть файл — отправим multipart
    const hasFile = !!form.logo
    let payload: any = form
    if (hasFile) {
      const fd = new FormData()
      fd.append("name", form.name)
      fd.append("bin", form.bin)
      form.license_ids.forEach(id => fd.append("license_ids", String(id)))
      if (form.logo) fd.append("logo", form.logo)
      payload = fd
    } else {
      payload = { name: form.name, bin: form.bin, license_ids: form.license_ids }
    }

    const org = props.initial
      ? await updateOrg(props.initial.id, payload)
      : await createOrg(payload)

    emit("submitted", org)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
label { user-select: none; }
</style>
