<script lang="ts" setup>
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
      <div v-if="!booksPending" class="grid grid-cols-2 gap-8">
        <Card v-for="book in books" :id="book.Name" :description="truncate(book.Description)" :field-value="book.Author"
              :genres="normalizeGenres(book.Genres)" :img-route="'/books/image?name=' + encodeURI(book.Name)" :rating="book.Rating" :rating-max="5"
              :title="book.Name" field-name="Автор"/>
      </div>
      <div v-else>
        <p class="text-center">Загрузка...</p>
      </div>
    </div>
    <h1 class="font-bold text-xl">Фильмы (ТОП 10)</h1>
    <div>
      <div v-if="!filmsPending" class="grid grid-cols-2 gap-8">
        <Card v-for="film in films" :id="film.name" :author="film.release_date"
              :description="truncate(film.description.replace(' Read all', ''))" :field-value="film.release_date"
              :genres="normalizeGenres(film.genres)" :img-route="'/movies/image?name=' + encodeURI(film.name)" :rating="film.rating"
              :rating-max="10" :title="film.name" field-name="Дата премьеры"/>
      </div>
      <div v-else>
        <p class="text-center">Загрузка...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>