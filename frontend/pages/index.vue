<script lang="ts" setup>
const {
  status,
  data,
  token,
  lastRefreshedAt,
  getSession,
  signUp,
  signIn,
  signOut,
} = useAuth()

onMounted(async () => {
  if (status.value == "unauthenticated") {
    await navigateTo('/auth/login')
  }
})
</script>

<template>
  <p>Выберите интересующий Вас раздел.</p>
</template>

<style scoped>

</style>