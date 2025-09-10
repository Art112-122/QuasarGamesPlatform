<template>
  <q-input v-model="search" debounce="300" placeholder="Поиск..." filled clearable class="">
    <template v-slot:append>
      <q-icon name="search" />
    </template>
  </q-input>
  <q-page class="q-pa-md row">
    <q-card
      class="col-lg-2 col-md-2 col-sm-3 col-5 soso-pikmi-misha"
      style="margin-left: 1rem; margin-right: 1rem; margin-bottom: 2rem"
      v-for="[name, page] in filteredPages"
      :key="name"
    >
      <q-img :src="`/cardimages/${page['imagePath']}`">
        <div class="absolute-bottom">
          <router-link v-on:click="setGames(name)" :to="`/games/${page.pathName}`" class="text-h6 link">{{ name }}</router-link>
        </div>
      </q-img>

      <q-card-actions class="q-gutter-md">
        <q-btn
          v-for="([category, link], idx) in Object.entries(page['categories'])"
          :key="idx"
          :to="`/games/${page.pathName}/${link}`"
          flat
          v-on:click="setGames(name)"
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

<script setup>
import { ref, computed } from 'vue'
import configuration from '../../config.json'
import {getCookie, setCookie} from 'src/api/cookies.js'

function setGames(game) {
  let games = JSON.parse(getCookie("games") ?? "[]")
  games.push(game)
  setCookie("games", JSON.stringify(games))
}

const json = configuration[0]
const search = ref('')

const filteredPages = computed(() => {
  const pages = json.pages || {}
  return Object.entries(pages).filter(([item, value]) => {
    const searchText = search.value.toLowerCase()
    return (
      item.toLowerCase().includes(searchText) ||
      (value.pathname && value.pathname.toLowerCase().includes(searchText))
    )
  })
})
</script>

<style scoped>
.link {
  font-size: 1.00rem;
  text-decoration: none;
  color: white;
}

.soso-pikmi-misha:hover {
  transform: scale(1.07);
  transition-duration: 0.3s;
}


</style>
