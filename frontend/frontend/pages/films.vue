<script setup lang="ts">
import type {Film} from "~/models";

const page = ref(1);

const {data: films, pending} = useFetch<Film[]>(() => `http://localhost:8000/movies?skip=${page.value}`)

const canDecrease = computed(() => page.value != 1)

function truncate(s: string) {
  return s.length > 300 ? s.slice(0, 300) + "..." : s;
}

function normalizeGenres(s: string) {
  if (!s) {
    return 'Не указаны'
  }
  return s.split(",").map(x => x.trim()).map(x => x.at(0)!.toUpperCase() + x.substring(1));
}

function increasePage() {
  page.value += 1
}

function decreasePage() {
  if (!canDecrease.value) {
    return
  }

  page.value -= 1
}
</script>

<template>
  <div>
    <div class="grid grid-cols-2 gap-8" v-if="!pending">
      <Card v-for="film in films" :id="film.name" :title="film.name" :description="truncate(film.description.replace(' Read all', ''))" :genres="normalizeGenres(film.genres)" :author="film.release_date" field-name="Дата премьеры" :field-value="film.release_date":rating="film.rating" :rating-max="10" :img-route="'/movies/image?name=' + encodeURI(film.name)" />
    </div>
    <div v-else>
      <p class="text-center">Загрузка фильмов...</p>
    </div>
  </div>
  <div class="fixed left-0 bottom-20 flex justify-center w-full">
    <div class="flex space-x-16 w-full justify-center">
      <div class="bg-white/80 backdrop-blur-lg border py-2 px-4 rounded-lg shadow-sm" :class="canDecrease ? 'cursor-pointer' : 'cursor-not-allowed'" @click="decreasePage"><</div>
      <div class="bg-white/80 backdrop-blur-lg border py-2 px-4 rounded-lg shadow-sm cursor-pointer" @click="increasePage">></div>
    </div>
  </div>
</template>

<style scoped>

</style>