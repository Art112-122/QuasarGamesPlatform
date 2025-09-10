<script setup>

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
          <h2 class="text-center oswald-bold">Назва</h2>
        </q-timeline-entry>

        <q-timeline-entry class="oswald-bold" title="Опис" subtitle="February 22, 1986">
          <div style="font-size: 1.1rem; font-family: sans-serif; min-height: 400px">
            Небольшое описание
          </div>
        </q-timeline-entry>
        <q-timeline-entry />
      </q-timeline>
    </div>
    <div class="col" style="margin-right: 5rem">
      <q-card dark bordered class="bg-grey-9 my-card">
        <q-card-section>
          <div class="text-h6">
            <q-avatar color="primary" size="40px">
              {{ author[0].toUpperCase() }}
            </q-avatar>
            {{author}}
          </div>
        </q-card-section>

        <q-separator dark inset />

        <q-card-section>
          <template>
            <div class="q-pa-md row justify-center">
              <div style="min-height: 400px">
                <q-chat-message
                  name="me"
                  avatar="https://cdn.quasar.dev/img/avatar1.jpg"
                  :text="['hey, how are you?']"
                  stamp="7 minutes ago"
                  sent
                  bg-color="amber-7"
                />
                <q-chat-message
                  name="Jane"
                  avatar="https://cdn.quasar.dev/img/avatar5.jpg"
                  :text="['doing fine, how r you?']"
                  stamp="4 minutes ago"
                  text-color="white"
                  bg-color="primary"
                />
              </div>
            </div>
          </template>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<style scoped></style>
