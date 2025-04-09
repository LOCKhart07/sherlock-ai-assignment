<template>
    <q-page class="flex flex-center">
        <q-card class="login-card q-pa-lg">
            <q-card-section>
                <div class="text-h5 text-center q-mb-md">Login</div>
                <q-form @submit="onSubmit" class="q-gutter-md">
                    <q-input v-model="username" label="Username" :rules="[val => !!val || 'Username is required']"
                        outlined />

                    <q-input v-model="password" label="Password" :type="isPwd ? 'password' : 'text'"
                        :rules="[val => !!val || 'Password is required']" outlined>
                        <template v-slot:append>
                            <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                                @click="isPwd = !isPwd" />
                        </template>
                    </q-input>

                    <div>
                        <q-btn label="Login" type="submit" color="primary" class="full-width" :loading="loading" />
                    </div>

                    <div class="text-center q-mt-sm">
                        <router-link to="/register" class="text-primary">Register here</router-link>
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

export default {
    name: 'LoginPage',
    setup() {
        const $q = useQuasar()
        const router = useRouter()
        const username = ref('')
        const password = ref('')
        const isPwd = ref(true)
        const loading = ref(false)

        const onSubmit = async () => {
            try {
                loading.value = true
                const response = await fetch('http://localhost:8000/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        username: username.value,
                        password: password.value,
                    }),
                })

                if (response.ok) {
                    const data = await response.json()
                    localStorage.setItem('token', data.access_token)
                    $q.notify({
                        color: 'positive',
                        message: 'Login successful!',
                    })
                    router.push('/profile')
                } else {
                    const error = await response.json()
                    throw new Error(error.detail || 'Login failed')
                }
            } catch (error) {
                $q.notify({
                    color: 'negative',
                    message: error.message || 'Login failed',
                })
            } finally {
                loading.value = false
            }
        }

        return {
            username,
            password,
            isPwd,
            loading,
            onSubmit,
        }
    },
}
</script>

<style scoped>
.login-card {
    width: 100%;
    max-width: 400px;
}
</style>