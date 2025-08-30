<template>
  <div class="card">
    <div class="card-row">
      <img v-if="org.logo" :src="org.logo" class="logo" alt="logo" />
      <div class="content">
        <div class="h2">{{ org.name }}</div>
        <div class="kv"><span class="k">BIN</span><span class="v">{{ org.bin }}</span></div>
        <div>
          <span v-for="lic in org.licenses" :key="lic.id" class="badge">{{ lic.code }}</span>
        </div>
      </div>

      <!-- ВНИМАНИЕ: слот теперь в .actions, чтобы кнопка не ломала ряд -->
      <div class="actions">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ org: { type: Object, required: true } })
</script>
