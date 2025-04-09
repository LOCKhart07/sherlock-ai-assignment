<template>
  <q-page class="q-pa-md">
    <div class="text-center q-mb-lg">
      <h1 class="text-h3 q-mb-sm">Welcome to SherlockAI Assignment</h1>
      <p class="text-subtitle1 text-grey-8">Your one-stop platform for cryptocurrency and weather information. Just
        kidding, it's just a assignment.</p>
    </div>

    <div class="row q-col-gutter-md justify-center">
      <!-- Cryptocurrency Box -->
      <div class="col-12 col-sm-6 col-md-4">
        <q-card class="feature-card cursor-pointer" @click="navigateTo('/coin')">
          <q-card-section class="text-center">
            <q-icon name="currency_bitcoin" size="4em" color="primary" />
            <div class="text-h5 q-mt-md">Cryptocurrency</div>
            <div class="text-subtitle2 text-grey-8 q-mt-sm">
              Track real-time cryptocurrency prices, trends, and market data
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Weather Box -->
      <div class="col-12 col-sm-6 col-md-4">
        <q-card class="feature-card cursor-pointer" @click="navigateTo('/weather')">
          <q-card-section class="text-center">
            <q-icon name="wb_sunny" size="4em" color="warning" />
            <div class="text-h5 q-mt-md">Weather</div>
            <div class="text-subtitle2 text-grey-8 q-mt-sm">
              View real-time weather data and forecasts across different locations
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Profile Box -->
      <div class="col-12 col-sm-6 col-md-4">
        <q-card class="feature-card cursor-pointer" @click="navigateTo('/profile')">
          <q-card-section class="text-center">
            <q-icon name="person" size="4em" color="secondary" />
            <div class="text-h5 q-mt-md">Profile</div>
            <div class="text-subtitle2 text-grey-8 q-mt-sm">
              Manage your account settings and personal information
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (route) => {
  router.push(route)
}
</script>

<style scoped>
.feature-card {
  height: 100%;
  transition: transform 0.3s ease-in-out;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.cursor-pointer {
  cursor: pointer;
}
</style>
