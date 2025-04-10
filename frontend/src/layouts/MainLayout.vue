<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          SherlockAI Assignment - Jenslee Dsouza
        </q-toolbar-title>

        <q-btn flat dense round icon="code" aria-label="GitHub" @click="openGitHubRepo" />

      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" bordered overlay>
      <q-list>
        <!-- <q-item-label header>Navigation</q-item-label> -->
        <q-item clickable v-ripple :to="{ name: 'home' }" exact active-class="q-item--active">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>Home</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/coin" exact active-class="q-item--active">
          <q-item-section avatar>
            <q-icon name="monetization_on" />
          </q-item-section>
          <q-item-section>Coins</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/weather" exact active-class="q-item--active">
          <q-item-section avatar>
            <q-icon name="cloud" />
          </q-item-section>
          <q-item-section>Weather Stations</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/profile" exact active-class="q-item--active">
          <q-item-section avatar>
            <q-icon name="person" />
          </q-item-section>
          <q-item-section>Profile</q-item-section>
        </q-item>

        <q-separator />

        <q-item clickable v-ripple @click="logout">
          <q-item-section avatar>
            <q-icon name="logout" />
          </q-item-section>
          <q-item-section>Logout</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'src/stores/auth'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const router = useRouter()
const authStore = useAuthStore()
const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function logout() {
  authStore.logout()
  $q.notify({
    color: 'positive',
    message: 'Logged out successfully'
  })
  router.push('/login')
}

function openGitHubRepo() {
  window.open('https://github.com/LOCKhart07/sherlock-ai-assignment', '_blank')
}
</script>

<style scoped>
.q-toolbar {
  min-height: 64px;
}

.q-drawer {
  background: #f5f5f5;
}
</style>
