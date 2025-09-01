<template>
  <div class="card">
    <div class="card-row">
      <img v-if="org.logo" :src="org.logo" class="logo" alt="logo" />

      <div class="content">
        <!-- Заголовок кликабелен -->
        <NuxtLink :to="`/org/${org.id}`" class="h2 title-link">
          {{ org.name }}
        </NuxtLink>

        <div class="kv">
          <span class="k">BIN</span>
          <span class="v">{{ org.bin }}</span>
        </div>

        <div>
          <span v-for="lic in org.licenses" :key="lic.id" class="badge">{{ lic.code }}</span>
        </div>
      </div>

      <!-- Справа: по умолчанию "Подробнее". Если родитель передал слот (например, "Редактировать"), он перекрывает фолбэк -->
      <div class="actions">
        <slot>
          <NuxtLink :to="`/org/${org.id}`" class="btn ghost">Подробнее</NuxtLink>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ org: { type: Object, required: true } })
</script>
