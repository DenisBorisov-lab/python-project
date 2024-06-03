<script setup lang="ts">
import type {Book, Film} from "~/models";

const {data: books, pending: booksPending} = useFetch<Book[]>(() => `http://localhost:8000/recommendations/books`)
const {data: films, pending: filmsPending} = useFetch<Film[]>(() => `http://localhost:8000/recommendations/movies`)

function truncate(s: string) {
  return s.length > 300 ? s.slice(0, 300) + "..." : s;
}

function normalizeGenres(s: string) {
  if (!s) {
    return 'Не указаны'
  }
  return s.split(",").map(x => x.trim()).map(x => x.at(0)!.toUpperCase() + x.substring(1));
}
</script>

<template>
  <div class="flex flex-col space-y-4">
    <h1 class="font-bold text-xl">Книги (ТОП 10)</h1>
    <div>
      <div class="grid grid-cols-2 gap-8" v-if="!booksPending">
        <Card v-for="book in books" :id="book.Name" :title="book.Name" :description="truncate(book.Description)" :genres="normalizeGenres(book.Genres)" field-name="Автор" :field-value="book.Author" :rating="book.Rating" :rating-max="5" :img-route="'/books/image?name=' + encodeURI(book.Name)" />
      </div>
      <div v-else>
        <p class="text-center">Загрузка...</p>
      </div>
    </div>
    <h1 class="font-bold text-xl">Фильмы (ТОП 10)</h1>
    <div>
      <div class="grid grid-cols-2 gap-8" v-if="!filmsPending">
        <Card v-for="film in films" :id="film.name" :title="film.name" :description="truncate(film.description.replace(' Read all', ''))" :genres="normalizeGenres(film.genres)" :author="film.release_date" field-name="Дата премьеры" :field-value="film.release_date":rating="film.rating" :rating-max="10" :img-route="'/movies/image?name=' + encodeURI(film.name)" />
      </div>
      <div v-else>
        <p class="text-center">Загрузка...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>