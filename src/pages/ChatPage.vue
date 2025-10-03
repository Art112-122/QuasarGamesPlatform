<script setup>
import { useQuasar } from 'quasar'
import { ref } from 'vue'

const $q = useQuasar()

const user = ref({
  name: 'Alex Johnson',
  email: 'alex@example.com',
  avatar: 'https://cdn.quasar.dev/img/avatar2.jpg',
  status: 'online',
})
</script>

<template>
  <div class="q-pa-md row justify-center chat-bg">
    <!-- чат -->
    <div class="col" :style="`height: ${$q.screen.height}px`" style="width: 100%; max-width: 400px">
      <q-chat-message name="me" :text="['hey, how are you?']" sent />
      <q-chat-message name="user" :text="['doing fine, how r you?']" />
      <q-chat-message name="me" :text="['all good, thanks!']" sent />
    </div>

    <div style="margin-top: 3rem" class="col-3 fixed-right user-panel q-pa-md">
      <q-card class="q-pa-md flex flex-center column">
        <q-avatar color="primary" text-color="white" size="80px" class="q-mb-md">
          {{ user.name ? user.name[0].toUpperCase() : '' }}
        </q-avatar>
        <div class="text-h6">{{ user.name }}</div>
        <div class="text-subtitle2 text-grey">{{ user.email }}</div>
        <q-badge
          style="border-radius: 30px"
          :color="user.status === 'online' ? 'green' : 'grey'"
          class="q-mt-md"
        >
          {{ user.status }}
        </q-badge>
      </q-card>
    </div>
  </div>
</template>

<style lang="sass" scoped>


// чат
.q-message-container
  background: transparent !important

:deep(.q-message-text--sent)
  background: linear-gradient(90deg, rgba(29, 29, 29, 0.21), rgba(29, 29, 29, 0.32)) !important
  backdrop-filter: blur(50px)
  color: white !important

:deep(.q-message-text--received)
  background: linear-gradient(90deg, rgba(29, 29, 29, 0.32), rgba(29, 29, 29, 0.21)) !important
  backdrop-filter: blur(50px)
  color: white !important

:deep(.q-message-text:before),
:deep(.q-message-text:after)
  display: none !important

:deep(.q-message-sent .q-message-name),
:deep(.q-message-received .q-message-name)
  color: black !important

// фон
.chat-bg
  width: 100%
  background: linear-gradient(180deg, #8c52ff, #c572ed)

:deep(.q-card)
  background: transparent
  border: none
  box-shadow: none !important

.user-panel
  background-image: linear-gradient(90deg, rgba(29, 29, 29, 0.24), rgba(29, 29, 29, 0.73))

</style>
