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

definePageMeta({
  auth: {
    unauthenticatedOnly: true,
    navigateAuthenticatedTo: '/books',
  }
})

const username = ref()
const password = ref()

async function login() {
  try {
    await signIn({username: username.value, password: password.value}, {external: true})
  } catch {
    if (process.client) {
      alert('Ошибка!')
    }
  }
}
</script>

<template>
  <div class="flex justify-center items-center w-full">
    <div class="p-4 shadow bg-white rounded-lg border flex flex-col">
      <h2 class="font-bold">Авторизация | <span class="text-gray-400 cursor-pointer"
                                                @click="navigateTo('/auth/register')">Регистрация</span></h2>
      <label class="mt-2" for="username">Юзернейм</label>
      <input id="username" v-model="username" name="username" type="text">
      <label class="mt-2" for="password">Пароль</label>
      <input id="password" v-model="password" name="password" type="password">
      <button class="mt-4 rounded-full hover:bg-purple-100 transition p-1 border" @click="login">Войти</button>
    </div>
  </div>
</template>

<style lang="postcss" scoped>
input {
  @apply rounded-lg border;
}
</style>