<script setup>
import config from "../../config.json"
import { useRoute } from "vue-router"
import { ref } from "vue"
import router from 'src/router/index.js'

const route = useRoute()
const pages = config[0]?.pages ?? {}

let foundGame = null

for (const [key, game] of Object.entries(pages)) {
  if (game.pathName === route.params.game) {
    foundGame = { key, ...game }
    break
  }
}

if (foundGame === null) {
  router.push({ name: 'profile'})
}
const columns = ref([
  { name: "name", label: "Обьявление", field: "name" },
  { name: "author", label: "Автор", field: "author" }
])

const rows = ref([
  { name: "testname1", author: "authorname1" }
])
</script>

<template>
  <q-tabs
    style="margin-top: 3rem"
    v-model="tab"
    class="text-teal"
  >
    <q-tab name="mails" icon="mail" label="Mails" />
    <q-tab name="alarms" icon="alarm" label="Alarms" />
    <q-tab name="movies" icon="movie" label="Movies" />
  </q-tabs>

  <q-table
    flat bordered
    :style="$q.screen.width < 750 ? 'margin: 3rem;': 'margin: 5rem;'"
    :rows="rows"
    :columns="columns"
    no-data-label="Ничего не найдено:("
    row-key="name"
  >
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td auto-width key="name" :props="props">
          {{ props.row.name }}
        </q-td>
        <q-td auto-width key="author" :props="props">
          {{ props.row.author }}
          <q-avatar color="primary" size="24px">
            {{ props.row.author[0].toUpperCase() }}
          </q-avatar>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<style scoped>
</style>
