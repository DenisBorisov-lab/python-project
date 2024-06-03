<script lang="ts" setup>
import type {Book} from "~/models";

const page = ref(1);

const {data: books, pending} = useFetch<Book[]>(() => `http://localhost:8000/books?skip=${page.value}`)

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
      <Card v-for="book in books" :id="book.Name" :description="truncate(book.Description)" :field-value="book.Author"
            :genres="normalizeGenres(book.Genres)" :img-route="'/books/image?name=' + encodeURI(book.Name)" :rating="book.Rating" :rating-max="5"
            :title="book.Name" field-name="Автор"/>
    </div>
    <div v-else>
      <p class="text-center">Загрузка книг...</p>
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