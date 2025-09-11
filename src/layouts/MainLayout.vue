<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar style="background-image: linear-gradient(#25193e, #06083A)">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Quasar App
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Essential Links
        </q-item-label>

        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
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
    link: '/games'
  },
  {
    title: 'Discord',
    caption: 'Наш Діскорд',
    icon: 'chat',
    link: 'https://discord.gg/VBjW9NERQv',
    essential: true
  }
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
