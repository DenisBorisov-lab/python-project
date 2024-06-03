<template>
  <div class="top-0 z-10 fixed h-16 w-screen bg-white/80 backdrop-blur-lg border-b flex items-center shadow-sm">
    <div class="flex justify-between px-20 w-full">
      <div class="flex space-x-12 items-center">
        <h1 class="font-bold text-2xl">Фильмобукинг</h1>
        <router-link :class="booksActive && 'header-link-active'" class="header-link" to="/books">Книжки</router-link>
        <router-link :class="filmsActive && 'header-link-active'" class="header-link" to="/films">Фильмы</router-link>
        <router-link :class="recommendationsActive && 'header-link-active'" class="header-link" to="/recommendations">
          Рекомендации
        </router-link>
      </div>
      <div class="flex items-center space-x-3">
        <p v-if="data?.username">{{ data?.username ?? "" }}</p>
        <p v-if="data?.username">|</p>
        <button v-if="data?.username" @click="unlogin">Выйти</button>
      </div>
    </div>
  </div>
  <div class="mt-24 flex justify-center">
    <div class="container min-h-screen">
      <NuxtPage/>
    </div>
  </div>
</template>

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

const route = useRoute();

const booksActive = computed(() => route.path.includes("books"))
const filmsActive = computed(() => route.path.includes("films"))
const recommendationsActive = computed(() => route.path.includes("recommendations"))

async function unlogin() {
  try {
    await signOut()
  } catch (e) {

  }
  await navigateTo('/auth/login')
}
</script>

<style lang="postcss" scoped>
.header-link {
  @apply text-xl transition;
}

.header-link:hover {
  @apply scale-110;
}

.header-link-active {
  @apply text-purple-600 scale-105;
}
</style>