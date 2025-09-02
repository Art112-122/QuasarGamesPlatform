<template>
  <div class="q-pa-md row fullscreen">
    <div
      ref="image"
      class="q-pa-md col-1"
      v-if="$q.screen.width < 800"
      style="margin-right: 3rem; background-image: linear-gradient(270deg, #ba52ff, #72baed)"
    ></div>
    <q-form
      @submit="onSubmit"
      :class="$q.screen.width >= 800 ? 'col-10 col-lg-3 col-md-5 col-sm-6' : 'col-8'"
      class="content-center"
    >
      <h3 :style="$q.screen.width >= 500 ? '' : 'font-size: 2rem'">Підтверження Ел. Адреси</h3>

      <q-input
        filled
        v-model="formattedCode"
        label="Код"
        @update:model-value="formatCode"
        maxlength="7"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Заповніть це поле будь ласка',
          (val) => (val.length===7) || 'Невірний код',
        ]"
      />



      <q-btn label="Надіслати" type="submit" color="primary" style="margin-top: 1rem" />

    </q-form>
    <div
      ref="image"
      v-if="$q.screen.width >= 800"
      class="q-pa-md col"
      style="margin-left: 5rem; background-image: linear-gradient(270deg, #ba52ff, #72baed)"
    ></div>
  </div>
</template>

<script setup>
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { api } from 'boot/axios.js'
import {getToken} from 'src/api/cookies.js'
import Router from 'src/router/index.js'

const $q = useQuasar()

let code = ref('')
let formattedCode = ref('')

function formatCode(val) {
  const digits = val.replace(/\s/g, '')

  formattedCode.value = digits.replace(/(\d{3})(?=\d)/g, '$1 ').trim()
  code.value = digits
}


const onSubmit = () => {
  api
    .post('/email', { code: code.value, headers: { 'token': getToken() } })
    .then(() => {
      Router.push('/games')
    })
    .catch((error) => {
      if (error.status < 500) {
        if (error.response) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: error.response.data,
          })
        } else if (error.request) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'cloud-off',
            message: '',
          })
        } else if (error.status === 422) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'cloud-off',
            message: 'Невалідна інформація, будь-ласка перевірте введені поля на правильність',
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
