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
          class="text-capitalize sergey-5cm-penis"
        >
          {{ category }}
        </q-btn>
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import configuration from '../../config.json'
import {api} from 'boot/axios.js'

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


onMounted(() => {
  api.get('/test')
  .then(response => {console.log(response.data)})
  api.post('/test', {test: "test_string"}).then(response => {console.log(response.data)})
})

</script>

<style scoped>
.link {
  font-size: 1.00rem;
  text-decoration: none;
  color: white;
}

.sergey-5cm-penis {
  font-size: 1.00rem;
  border: 2px solid #272525;
  box-shadow: 2px 2px 3px #272525;
  border-radius: 10px;
}

.soso-pikmi-misha:hover {
  box-shadow: #1D1D1D 2px 2px 2px;
  transform: scale(1.07);
  transition: 0.3s;
}

</style>
