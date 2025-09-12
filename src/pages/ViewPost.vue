<script setup>
import { useRoute } from 'vue-router'
import { api } from 'boot/axios.js'
import { useQuasar } from 'quasar'
import { onMounted, ref } from 'vue'
import router from 'src/router/index.js'
import { getToken } from 'src/api/cookies.js'

const $q = useQuasar()
const route = useRoute()

const createdAt = ref('')
const title = ref('')
const description = ref('')
const author = ref('')
const is_author = ref(false)

async function loadData() {
  try {
    const response = await api.get('/games/id', {
      params: { id: route.params.id },
      headers: { Authorization: `Bearer ${getToken()}` },
    })
    const data = response.data
    createdAt.value = data.created_at
    title.value = data.name
    description.value = data.description
    author.value = data.author
    is_author.value = data.is_author
    descriptionToChange.value = data.description

  } catch {
    $q.notify({
      color: 'red-5',
      textColor: 'white',
      icon: 'warning',
      message: 'Не вдалося завантажити дані. Ви будете повернені назад...',
    })
    setTimeout(() => {
      router.back()
    }, 3000)
  }
}

onMounted(loadData)


const descriptionToChange = ref(description.value)
const changing = ref(false)
const changingData = () => {
  if (is_author.value) {
    changing.value = !changing.value
    if (!changing.value) {descriptionToChange.value = description.value}
  }
}

const deleteModal = ref(false)

const deletePost = () => {
  api
    .delete('/games', {
      params: { id: route.params.id },
      headers: { Authorization: `Bearer ${getToken()}` },
    })
    .then(() => {
      deleteModal.value = false
      $q.notify({
        color: 'green-5',
        textColor: 'white',
        icon: 'info',
        message: 'Публікація видалена. Ви будете повернені назад...',
      })
      setTimeout(() => {
        router.back()
      }, 3000)
    })
    .catch((error) => {
      if (error.status < 500) {
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Не вдалося завантажити дані. Ви будете повернені назад...',
        })
      } else {
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Критична помилка, спробуйте пізніше',
        })
      }
    })
}

// -- update --

const updatePost = () => {
  api
    .put(
      '/games',
      {
        id: route.params.id,
        description: descriptionToChange.value,
      },
      { headers: { Authorization: `Bearer ${getToken()}` } },
    )
    .then(() => {
      changing.value = false
      $q.notify({
        color: 'green-5',
        textColor: 'white',
        icon: 'info',
        message: 'Публікація змінена, сторінка буде оновлена...',
      })
      setTimeout(() => {
        window.location.reload()
      }, 3000)
    })
    .catch((error) => {
      if (error.status < 500) {
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Не вдалося оновити, спробуйте пізніше',
        })
      } else {
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Критична помилка, спробуйте пізніше',
        })
        console.log(error)
      }
    })
}
</script>

<template>
  <div class="q-pa-md row">
    <div
      v-if="$q.screen.width > 800"
      class="col-2"
      style="
        margin-right: 5rem;
        background-image: linear-gradient(270deg, #8c52ff, #c572ed);
        border-radius: 1%;
      "
    ></div>
    <div class="col-7 col-md-7 col-sm-7 col-lg-5">
      <q-avatar icon="arrow_back" size="60px" v-on:click="router.back()"></q-avatar>
      <q-timeline color="primary">
        <q-timeline-entry heading>
          <h2 class="oswald-bold word-wrap">{{ title }}</h2>
        </q-timeline-entry>

        <q-timeline-entry class="oswald-bold" title="Опис" :subtitle="createdAt">
          <div
            v-if="!changing"
            class="word-wrap"
            style="font-size: 1.1rem; font-family: sans-serif; min-height: 400px"
          >
            {{ description }}
          </div>
          <div v-else>
            <q-btn label="Змінити" v-on:click="updatePost" style="margin: 0.5rem" color="green"></q-btn>
            <q-btn label="Відмінити зміни" v-on:click="changingData" style="margin: 0.5rem" color="red"></q-btn>
            <q-input
              v-model="descriptionToChange"
              style="min-height: 400px"
              autofocus
              autogrow
              label="Тепер можете редагувати"
            />
          </div>
        </q-timeline-entry>
        <q-timeline-entry />
      </q-timeline>
    </div>
    <div class="col" style="margin-right: 5rem">
      <div v-if="$q.screen.width <= 600">
        <q-avatar color="primary" size="40px">
          {{ author ? author[0].toUpperCase() : '' }}
        </q-avatar>
        {{ author }}
      </div>
      <q-btn
        style="margin: 0.5rem"
        v-if="is_author"
        :label="changing ? 'Зупинити змінювання' : 'Змінити'"
        v-on:click="changingData"
        color="green"
      />
      <q-btn
        style="margin: 0.5rem"
        v-on:click="deleteModal = true"
        v-if="is_author"
        label="Видалити"
        color="red"
      />
      <q-card
        v-if="$q.screen.width > 600"
        style="margin-top: 4rem; padding: 1rem; min-height: 400px"
      >
        <div class="text-h6">
          <q-avatar color="primary" size="40px">
            {{ author ? author[0].toUpperCase() : '' }}
          </q-avatar>
          {{ author }}
        </div>
        <q-separator style="margin-top: 1rem; margin-bottom: 1rem" />
        <div class="q-pa-md row justify-center">
          <div style="width: 100%; max-width: 400px">
            <q-chat-message name="Я" :text="[`Привіт, я з привіду ${title}`]" sent />
          </div>
        </div>
        <q-btn
          flat
          label="Написати"
          class="absolute-bottom"
          v-on:click="
            $q.notify({
              color: 'blue',
              textColor: 'white',
              icon: 'warning',
              message: 'Ця функція в розробці...',
            })
          "
          style="padding-bottom: 0.5rem; padding-top: 0.5rem"
        />
      </q-card>
    </div>
  </div>

  <!-- dialog -->

  <q-dialog v-model="deleteModal" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="delete_forever" color="red" text-color="white" />
        <span class="q-ml-sm">Ви впевнені що хочете видалити публікацію?</span>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Скасувати" color="white" v-close-popup />
        <q-btn flat label="Видалити" color="red" v-on:click="deletePost" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped></style>
