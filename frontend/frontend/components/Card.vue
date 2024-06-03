<script lang="ts" setup>
const props = defineProps<{
  title: string;
  description: string;
  genres: string[];
  fieldName: string;
  fieldValue: string;
  rating: number;
  ratingMax: number;
  imgRoute: string;
}>()
</script>

<template>
  <div class="bg-white shadow-md rounded-lg flex hover:scale-105 transition overflow-y-hidden">
    <div class="flex">
      <img
          :src="'http://localhost:8000' + props.imgRoute"
          alt=""
          class="rounded-l-lg w-[189px]">
      <div class="p-3">
        <h2 class="text-2xl font-bold mb-2">{{ props.title }}</h2>
        <p class="text-gray-700 text-base mb-4">{{ props.description }}</p>
        <div class="mb-4">
          <span class="text-gray-600 text-sm font-semibold">Жанры:</span>
          <ul class="list-disc list-inside ml-2">
            <li v-for="genre in props.genres" :key="genre" class="text-sm text-gray-600">{{ genre }}</li>
          </ul>
        </div>
        <p class="text-gray-700 text-sm"><span class="font-semibold">{{ props.fieldName }}:</span> {{
            props.fieldValue
          }}</p>
        <p class="text-gray-700 text-sm mt-1">
          <span class="font-semibold">Рейтинг:</span> {{ props.rating }}
          <span class="text-yellow-500">{{ '★'.repeat(Math.round(props.rating)) }}</span>
          <span class="text-gray-300">{{ '★'.repeat(ratingMax - Math.round(props.rating)) }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
