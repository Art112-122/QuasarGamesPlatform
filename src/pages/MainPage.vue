<script setup>
import jsonObject from '../../config.json'
import { getCookie, getToken } from '../api/cookies.js'
import { api } from 'boot/axios.js'
import { ref } from 'vue'

const json = jsonObject[0]?.pages ?? {}

const username = ref('')

async function loadAccountInfo() {
  api
    .get('/me', { headers: { Authorization: `Bearer ${getToken()}` } })
    .then((data) => {
      username.value = data.data.username
    })
    .catch((error) => {
      if (error) {
        username.value = ''
      }
    })
}

loadAccountInfo()

const games = JSON.parse(getCookie("games") ?? "[]")

const filtered = Object.entries(json)
  .filter(([name]) => games.includes(name))
  .map(([name, page]) => ({ name, ...page }))

</script>

<template>

  <h1 class="subtitle text-center">
    Вітаю, <b v-if="username">{{ username }}!</b><b v-else>Геймеру!</b>
  </h1>
  <h4 class="text-center subtitle" v-if="games.length">Ваші Ігри</h4>
  <q-page class="q-pa-md row">
    <q-card
      v-for="(game, idx) in filtered"
      :key="game.name || idx"
      class="col-lg-2 col-md-2 col-sm-3 col-5"
      style="margin-left: 1rem; margin-right: 1rem; margin-bottom: 2rem; max-height: 12rem"
    >
      <q-img :src="`/cardimages/${game.imagePath}`">
        <div class="absolute-bottom">
          <router-link :to="`/games/${game.pathName}`" class="text-h6 link">
            {{ game.name || 'Помилка' }}
          </router-link>
        </div>
      </q-img>

      <q-card-actions class="q-gutter-md">
        <q-btn
          v-for="([category, link], idx2) in Object.entries(game.categories || {})"
          :key="idx2"
          :to="`/games/${game.pathName}/${link}`"
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

h1 {
  font-family: 'Roboto Mono', monospace;
}
</style>
