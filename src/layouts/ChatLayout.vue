<script setup>
import { ref } from 'vue'
import router from 'src/router/index.js'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const isOpen = ref(true)

const data = ref([
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
  { name: 'TestName1', email: 'test@gmail.com' },
  { name: 'TestEmail1', email: 'test@gmail.com' },
])
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar style="background-image: linear-gradient(#25193e, #06083a)">
        <q-btn flat dense round icon="arrow_back" aria-label="Menu" @click="router.push('/')">
          <q-tooltip>Повернутися на головну сторінку</q-tooltip>
        </q-btn>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="isOpen = !isOpen" />

        <q-toolbar-title>LootMarket</q-toolbar-title>

        <q-drawer
          :width="$q.screen.width >= 800 ? 300 : null"
          v-model="isOpen"
          side="left"
          bordered
        >
          <div class="bg-dark">
            <q-avatar
              icon="settings"
              class="settings"
              size="60px"

            ></q-avatar>
          </div>
          <q-virtual-scroll :items="data" virtual-scroll-item-size="56">
            <template v-slot="{ item, index }">
              <q-item clickable v-ripple :key="index" @click="router.push(`/chat/${item.email}`)">
                <q-item-section avatar>
                  <q-avatar color="primary" text-color="white">
                    {{ item.name ? item.name[0].toUpperCase() : '' }}
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ item.name }}</q-item-label>
                  <q-item-label caption>{{ item.email }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-virtual-scroll>
        </q-drawer>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style lang="sass" scoped>
.contact-item
  height: 56px

.settings
  cursor: pointer
  transition-duration: 0.2s

.settings:hover
  background-color: rgba(255, 255, 255, 0.07);

</style>
