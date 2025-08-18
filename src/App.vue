<template>
  <router-view />
</template>

<script setup>
import { useQuasar } from 'quasar'
let $q = useQuasar()

$q.dark.set(true)
</script>
