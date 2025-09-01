<template>
  <div class="q-pa-md row fullscreen">
    <div
      ref="image"
      class="q-pa-md col-1"
      v-if="$q.screen.width < 800"
      style="margin-right: 3rem; background-image: linear-gradient(270deg, #8c52ff, #c572ed)"
    ></div>
    <q-form
      @submit="onSubmit"
      :class="$q.screen.width >= 800 ? 'col-10 col-lg-3 col-md-5 col-sm-6' : 'col-8'"
      class="content-center"
    >
      <h3 :style="$q.screen.width >= 500 ? '' : 'font-size: 2rem'">Регістрація</h3>
      <q-input
        filled
        v-model="name"
        label="Username"
        lazy-rules
        :rules="[(val) => (val && val.length > 0) || 'Заповніть це поле будь ласка']"
      />

      <q-input
        filled
        v-model="email"
        label="Email"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Заповніть це поле будь ласка',
          (val) => val.includes('@gmail.com') || 'Невірна електронна адреса',
        ]"
      />

      <q-input
        filled
        :type="showPassword ? 'text' : 'password'"
        v-model="password"
        label="Пароль"
        lazy-rules
        :rules="[
          (val) => (val !== null && val !== '') || 'Заповніть це поле будь ласка',
          (val) => val.length < 20 || 'Завеликий пароль',
        ]"
      />

      <q-toggle v-model="showPassword" label="Подивитися пароль" />

      <q-btn label="Надіслати" type="submit" color="primary" style="margin-left: 3rem" />
      <div class="text-center subtitle" style="margin-top: 2rem">
        Вже маєте аккаунт?
        <router-link class="text-primary" to="/login">Вхід</router-link>
      </div>
    </q-form>
    <div
      ref="image"
      v-if="$q.screen.width >= 800"
      class="q-pa-md col"
      style="margin-left: 5rem; background-image: linear-gradient(270deg, #8c52ff, #c572ed)"
    ></div>
  </div>
</template>

<script setup>
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { api } from 'boot/axios.js'
import { setCookie } from 'src/api/cookies.js'
import Router from 'src/router/index.js'

const $q = useQuasar()

let showPassword = ref(false)

let name = ref('')
let email = ref('')
let password = ref('')

const onSubmit = () => {
  api
    .post('/register', { name: name.value, email: email.value, password: password.value })
    .then((res) => {
      setCookie('token', res.data.access_token)
      Router.push('/emailCheck')
    })
    .catch((error) => {
      if (error.status < 500) {
        if (error.response) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: error.response.data.error,
          })
        } else if (error.status === 422) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'cloud-off',
            message: 'Невалідна інформація, будь-ласка перевірте введені поля на правильність',
          })
        } else if (error.request) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'cloud-off',
            message: '',
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
