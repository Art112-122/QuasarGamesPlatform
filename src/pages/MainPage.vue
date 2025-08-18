<script setup>
import jsonObject from "../../config.json"
const json = jsonObject[0]

</script>

<template>
<h1 class="page-header text-center">
  Вітаю, <b>{{username}}!</b>
</h1>
  <q-page class="q-pa-md row">
    <q-card
      class="col-lg-2 col-md-2 col-sm-3 col-5"
      style="margin-left: 1rem; margin-right: 1rem; margin-bottom: 2rem"
      v-for="[name, page] in json"
      :key="name"
    >
      <q-img :src="`/cardimages/${page['imagePath']}`">
        <div class="absolute-bottom">
          <router-link :to="`/${page['pathname']}`" class="text-h6 link">{{ name }}</router-link>
        </div>
      </q-img>

      <q-card-actions class="q-gutter-md">
        <q-btn
          v-for="([category, link], idx) in Object.entries(page['categories'])"
          :key="idx"
          :to="`/${link}`"
          flat
          color="primary"
          size="md"
          class="text-capitalize"
        >
          {{ category }}
        </q-btn>
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap');

h1 {
  font-family: 'Roboto Mono', monospace;
}
</style>
