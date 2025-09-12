<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar style="background-image: linear-gradient(#25193e, #06083a)">
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <div v-if="isAuth" class="flex items-center q-ml-auto">
          <q-avatar color="primary" size="40px" class="q-mr-sm">
            {{ username ? username[0].toUpperCase() : '' }}
          </q-avatar>
          <div>
            <div class="text-subtitle1">{{ username }}</div>
            <div class="text-caption text-grey">{{ email }}</div>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Essential Links</q-item-label>

        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { api } from 'boot/axios.js'
import { getToken } from 'src/api/cookies.js'

const linksList = [
  {
    title: 'Головна',
    caption: 'Вітальна сторінка',
    icon: 'home',
    link: '/',
  },
  {
    title: 'Игри',
    caption: 'Усі доступні ігри проекту',
    icon: 'apps',
    link: '/games',
  },
  {
    title: 'Discord',
    caption: 'Наш Діскорд',
    icon: 'chat',
    link: 'https://discord.gg/VBjW9NERQv',
    essential: true,
  },
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const isAuth = ref(false)
const username = ref('')
const email = ref('')

async function loadAccountInfo() {
  api
    .get('/me', { headers: { Authorization: `Bearer ${getToken()}` } })
    .then((data) => {
      console.log(data)
      isAuth.value = true
      username.value = data.data.username
      email.value = data.data.email
    })
    .catch((error) => {
      if (error.status < 500) {
        isAuth.value = false
      }
      else {
        isAuth.value = false
      }
    })
}

loadAccountInfo()
</script>
