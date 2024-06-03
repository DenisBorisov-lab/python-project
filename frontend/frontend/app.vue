<template>
  <div class="top-0 z-10 fixed h-16 w-screen bg-white/80 backdrop-blur-lg border-b flex space-x-12 items-center shadow-sm">
    <h1 class="ml-20 font-bold text-2xl">Фильмобукинг</h1>
    <router-link to="books" class="header-link" :class="booksActive && 'header-link-active'">Книжки</router-link>
    <router-link to="films" class="header-link" :class="filmsActive && 'header-link-active'">Фильмы</router-link>
    <router-link to="recommendations" class="header-link" :class="recommendationsActive && 'header-link-active'">Рекомендации</router-link>
  </div>
  <div class="mt-24 flex justify-center">
    <div class="container min-h-screen">
      <NuxtPage />
    </div>
  </div>
</template>

<script lang="ts" setup>
const route = useRoute();

const booksActive = computed(() => route.path.includes("books"))
const filmsActive = computed(() => route.path.includes("films"))
const recommendationsActive = computed(() => route.path.includes("recommendations"))
</script>

<style scoped lang="postcss">
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