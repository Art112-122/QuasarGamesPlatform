<script setup>
import config from '../../config.json'
import { useRoute } from 'vue-router'
import { computed, ref, watch, onMounted } from 'vue'
import router from 'src/router/index.js'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios.js'
import { getToken } from 'src/api/cookies.js'

const $q = useQuasar()
const route = useRoute()
const pages = config[0]?.pages ?? {}

let foundGame = null

for (const [key, game] of Object.entries(pages)) {
  if (game.pathName === route.params.game) {
    foundGame = {
      key,
      ...game,
    }
    break
  }
}

if (foundGame === null || foundGame === undefined) {
  router.push({ name: 'notFound' })
}
const modal = ref(false)
const categories = ref([])

const rows = ref([])

const currentTab = ref(route.params.category ?? '')

if (foundGame) {
  categories.value = Object.entries(foundGame.categories).map(([label, value]) => ({
    label,
    value,
  }))

  if (categories.value.some(cat => cat.value === route.params.category)) {
    currentTab.value = route.params.category
  } else {
    currentTab.value = categories.value[0]?.value || null
  }
}

const columns = ref([
  { name: 'name', label: 'Обьявление', field: 'name' },
  { name: 'author', label: 'Автор', field: 'author' },
])

function truncate(text, length = 30) {
  if (!text) return ''
  return text.length > length ? text.slice(0, length) + '...' : text
}

function routerPushTo() {
  if (currentTab.value === 'all') {
    router.push(`/games/${route.params.game}`)
  } else {
    router.push(`/games/${route.params.game}/${currentTab.value}`)
  }
}


const dialogSize = computed(() => {
  let size = $q.screen.width
  if (size > 1000) {
    return 'width: 30vw'
  } else if (size > 800) {
    return 'width: 40vw'
  } else {
    return 'width: 70vw'
  }
})



async function loadData() {
  try {
    const { data } = await api.get(`/games`, {
      params: {
        game: route.params.game,
        category: route.params.category ?? null,
      },
    })
    rows.value = data
  } catch (err) {
    console.error("Ошибка загрузки:", err)
    $q.notify({
      color: 'red-5',
      textColor: 'white',
      icon: 'warning',
      message: 'Не вдалося завантажити дані',
    })
  }
}

onMounted(loadData)

watch(
  () => [route.params.game, route.params.category],
  () => {
    currentTab.value = route.params.category ?? 'all'
    loadData()
  }
)







// -- Form --

const name = ref('')
const description = ref('')
const game = ref(route.params.game)
const selectedCategory = ref('')

const options = computed(() => {
  let option = []
  categories.value.forEach((value) => option.push(value))
  return option
})

const sendForm = () => {

  api
    .post(
      '/games/add',
      {
        name: name.value,
        description: description.value,
        game: game.value,
        category: selectedCategory.value?.value,
      },
      { headers: { Authorization: `Bearer ${getToken()}`, 'Content-Type': 'application/json' } },
    )
    .then(() => {
      modal.value = false
      $q.notify({
        color: 'green-3',
        textColor: 'white',
        icon: 'check',
        message: 'Ваш пост успішно створений!',
      })
    })
    .catch((error) => {
      if (error.status < 500) {
        if (error.status === 422) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: 'Невалідна інформація, будь-ласка перевірте введені поля на правильність',
          })
          console.log(error.response.data)
        } else if (error.response) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: error.response.data.error,
          })
        } else if (error.request) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: 'Невідома помилка, спробуйте пізніше',
          })
        } else {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'error',
            message: 'Невідома помилка, спробуйте пізніше',
          })
        }
      } else {
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'error',
          message: 'Невідома помилка, спробуйте пізніше',
        })
      }
    })
}
</script>

<template>
  <q-tabs
    v-model="currentTab"
    class="text-primary"
    align="center"
    @update:model-value="routerPushTo"
  >
    <q-tab label="Усі" name="all"/>
    <q-tab v-for="cat in categories" :key="cat.value" :name="cat.value" :label="cat.label" />
  </q-tabs>

  <q-separator />

  <div class="text-h3 text-white text-center text-bold">
    {{ foundGame.key }}
  </div>

  <div class="game-image">
    <img :src="`/cardimages/${foundGame.imagePath}`" alt="game image" />
  </div>

  <div :class="$q.screen.width < 750 ? 'margin-sm' : 'margin-md'">
    <q-btn label="Створити" color="primary" @click="modal = true" />
    <q-table
      style="margin-top: 2rem"
      flat
      bordered
      :rows="rows"
      :columns="columns"
      class="table-games"
      no-data-label="Ничего не найдено:("
      row-key="name"
    >
      <template v-slot:body="props">
        <q-tr :props="props" v-on:click="router.push(`/post/view/${props.row.id}`)">
          <q-td auto-width key="name" :props="props">
            {{ truncate(props.row.name, 30) }}
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
  </div>

  <!-- Dialog -->
  <q-dialog v-model="modal">
    <q-card>
      <q-card-section>
        <div class="text-h6">Створити</div>
      </q-card-section>

      <q-separator />

      <q-card-section style="max-height: 50vh" class="scroll">
        <q-input
          :style="dialogSize"
          filled
          v-model="name"
          label="Короткий опис \ Назва"
          lazy-rules
          maxlength="20"
          :rules="[(val) => (val && val.length > 0) || 'Заповніть це поле будь ласка']"
        />

        <q-form>
          <q-input
            autogrow
            filled
            type="textarea"
            v-model="description"
            label="Повний опис"
            lazy-rules
            :rules="[(val) => (val && val.length > 0) || 'Заповніть це поле будь ласка']"
          />
          <q-input disable filled v-model="game" />
          <q-select
            label="Категорія"
            transition-show="scale"
            transition-hide="scale"
            filled
            v-model="selectedCategory"
            :options="options"
            :rules="[(val) => !!val || 'Оберіть категорію']"
            style="width: 250px; margin-top: 1rem"
          />
        </q-form>
      </q-card-section>

      <q-separator />

      <q-card-actions align="right">
        <q-btn flat label="Закрити" color="primary" v-close-popup />
        <q-btn flat label="Створити" v-on:click="sendForm" color="primary" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>
.margin-sm {
  margin: 2rem 3rem 3rem;
}

.margin-md {
  margin: 2rem 5rem 5rem;
}

.game-image img {
  border-radius: 10%;
  max-width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
  margin: 0 auto;
}
</style>
