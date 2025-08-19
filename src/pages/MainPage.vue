<script setup>
import jsonObject from '../../config.json'
import { getCookie } from '../api/cookies.js'

const json = jsonObject[0]?.pages ?? {}

const username = "TestName1"

const games = getCookie('games') ?? []

const filtered = Object.entries(json)
  .filter(([name]) => games.includes(name))
</script>

<template>

  <h1 class="subtitle text-center">
    Вітаю, <b v-if="username">{{ username }}!</b><b v-else>Мандрівнику!</b>
  </h1>
  <h4 class="text-center subtitle" v-if="games.length">Ваші Ігри</h4>
  <q-page class="q-pa-md row">
    <q-card
      v-for="([name, page], idx) in Object.entries(filtered)"
      :key="name || idx"
      class="col-lg-2 col-md-2 col-sm-3 col-5"
      style="margin-left: 1rem; margin-right: 1rem; margin-bottom: 2rem"
    >


      <q-img :src="`/cardimages/${page['imagePath']}`">
      <div class="absolute-bottom">
        <router-link :to="`/${page.pathName}`" class="text-h6 link">
          {{ name || 'Помилка' }}
        </router-link>
      </div>
      </q-img>

      <q-card-actions class="q-gutter-md">
        <q-btn
          v-for="([category, link], idx2) in Object.entries(page.categories || {})"
          :key="idx2"
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

.link {
  font-size: 0.98rem;
  text-decoration: none;
  color: white;
}

.my-card {
  max-height: 30rem !important;
}

.image-back {
  align-items: center;
}

h1 {
  font-family: 'Roboto Mono', monospace;
}
</style>
