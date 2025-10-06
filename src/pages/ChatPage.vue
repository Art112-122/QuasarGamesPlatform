<script setup>
import { useQuasar } from 'quasar'
import { ref, nextTick } from 'vue'

const $q = useQuasar()

const showInput = ref(false)
const message = ref('')
const inputRef = ref(null)
const showAvatar = ref(true)

function openInput() {
  showAvatar.value = false
  showInput.value = true
  nextTick(() => {
    inputRef.value?.focus()
  })
}

function closeInput() {
  showInput.value = false
  message.value = ''
  setTimeout(() => {
    showAvatar.value = true
  }, 400)
}

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
      <div
        class="fixed-bottom chat-input-box flex justify-center items-center"
        style="margin-bottom: 1rem"
      >
        <div class="chat-input" :class="{ expanded: showInput }">
          <transition name="fade">
            <q-input
              v-show="showInput"
              v-model="message"
              ref="inputRef"
              autofocus
              borderless
              placeholder="Напиши повідомлення..."
              @blur="closeInput"
            />
          </transition>
            <q-avatar
              v-show="showAvatar"
              icon="chat"
              text-color="white"
              size="50px"
              class="cursor-pointer"
              @click="openInput"
            />
        </div>
      </div>
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
          :color="user.status === 'online' ? 'teal' : 'grey'"
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
.chat-input

  transition-property: opacity, width
  transition-duration: 0.4s, 0.40s
  border-radius: 5rem
  padding: 0.5rem
  background: linear-gradient(45deg, rgba(29, 29, 29, 0.21), rgba(29, 29, 29, 0.32)) !important
  width: 60px
  opacity: 1



.chat-input.expanded
  width: 100%
  opacity: 1


.chat-input-box
  left: 50%
  transform: translateX(-50%)
  bottom: 20px
  position: fixed
  display: flex
  justify-content: center
  align-items: center
  width: auto
  height: auto
  background: transparent


.chat-input-box
  bottom: 20px


.chat-input-box .q-avatar
  cursor: pointer
  transition: transform 0.2s


.q-avatar:hover
  transform: scale(1.1)


.fade-enter-active, .fade-leave-active
  transition: opacity 0.4s ease

.fade-enter-from, .fade-leave-to
  opacity: 0





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
