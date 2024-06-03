<script lang="ts" setup>
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
    <div v-if="!pending" class="grid grid-cols-2 gap-8">
      <Card v-for="film in films" :id="film.name" :author="film.release_date"
            :description="truncate(film.description.replace(' Read all', ''))" :field-value="film.release_date"
            :genres="normalizeGenres(film.genres)" :img-route="'/movies/image?name=' + encodeURI(film.name)" :rating="film.rating"
            :rating-max="10" :title="film.name" field-name="Дата премьеры"/>
    </div>
    <div v-else>
      <p class="text-center">Загрузка фильмов...</p>
    </div>
  </div>
  <div class="fixed left-0 bottom-20 flex justify-center w-full">
    <div class="flex space-x-16 w-full justify-center">
      <div :class="canDecrease ? 'cursor-pointer' : 'cursor-not-allowed'"
           class="bg-white/80 backdrop-blur-lg border py-2 px-4 rounded-lg shadow-sm" @click="decreasePage"><
      </div>
      <div class="bg-white/80 backdrop-blur-lg border py-2 px-4 rounded-lg shadow-sm cursor-pointer"
           @click="increasePage">>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>