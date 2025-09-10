<script setup>
const createdAt = '26.08.2025'
const title = 'Название'
const description = 'БОЛЬШОЕ ОПИСАНИЕ'
const author = 'Oniqq'
</script>

<template>
  <div class="q-pa-md row">
    <div
      class="col-2"
      style="
        margin-right: 5rem;
        background-image: linear-gradient(270deg, #8c52ff, #c572ed);
        border-radius: 1%;
      "
    ></div>
    <div class="col-5">
      <q-timeline color="primary">
        <q-timeline-entry heading>
          <h2 class="text-center oswald-bold">{{title}}</h2>
        </q-timeline-entry>

        <q-timeline-entry class="oswald-bold" title="Опис" :subtitle="createdAt">
          <div style="font-size: 1.1rem; font-family: sans-serif; min-height: 400px">
            {{description}}
          </div>
        </q-timeline-entry>
        <q-timeline-entry />
      </q-timeline>
    </div>
    <div class="col" style="margin-right: 5rem">
          <div class="text-h6" style="margin-top: 4rem;">
            <q-avatar color="primary" size="40px">
              {{ author[0].toUpperCase() }}
            </q-avatar>
            {{author}}
          </div>
    </div>
  </div>
</template>

<style scoped></style>
