<template>
    <q-page class="flex flex-center">
        <q-card class="register-card q-pa-lg">
            <q-card-section>
                <div class="text-h5 text-center q-mb-md">Register</div>
                <q-form @submit="onSubmit" class="q-gutter-md">
                    <q-input v-model="email" label="Email" type="email" :rules="[
                        val => !!val || 'Email is required',
                        val => /^[^@]+@[^@]+\.[^@]+$/.test(val) || 'Invalid email format'
                    ]" outlined />

                    <q-input v-model="username" label="Username" :rules="[val => !!val || 'Username is required']"
                        outlined />

                    <q-input v-model="password" label="Password" :type="isPwd ? 'password' : 'text'"
                        :rules="[val => !!val || 'Password is required']" outlined>
                        <template v-slot:append>
                            <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                                @click="isPwd = !isPwd" />
                        </template>
                    </q-input>

                    <q-input v-model="fullName" label="Full Name" :rules="[val => !!val || 'Full name is required']"
                        outlined />

                    <q-input v-model="bio" label="Bio" type="textarea" outlined />

                    <q-input v-model="phone" label="Phone" outlined />

                    <q-input v-model="photoUrl" label="Photo URL" outlined />

                    <div>
                        <q-btn label="Register" type="submit" color="primary" class="full-width" :loading="loading" />
                    </div>

                    <div class="text-center q-mt-sm">
                        <router-link to="/login" class="text-primary">Already have an account? Login here</router-link>
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
    name: 'RegisterPage',
    setup() {
        const $q = useQuasar()
        const router = useRouter()
        const email = ref('')
        const username = ref('')
        const password = ref('')
        const fullName = ref('')
        const bio = ref('')
        const phone = ref('')
        const photoUrl = ref('')
        const isPwd = ref(true)
        const loading = ref(false)

        const onSubmit = async () => {
            try {
                loading.value = true
                const response = await fetch('http://localhost:8000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email.value,
                        username: username.value,
                        password: password.value,
                        full_name: fullName.value,
                        bio: bio.value,
                        phone: phone.value,
                        photo_url: photoUrl.value,
                    }),
                })

                if (response.ok) {
                    $q.notify({
                        color: 'positive',
                        message: 'Registration successful! Please login.',
                    })
                    router.push('/login')
                } else {
                    const error = await response.json()
                    throw new Error(error.detail || 'Registration failed')
                }
            } catch (error) {
                $q.notify({
                    color: 'negative',
                    message: error.message || 'Registration failed',
                })
            } finally {
                loading.value = false
            }
        }

        return {
            email,
            username,
            password,
            fullName,
            bio,
            phone,
            photoUrl,
            isPwd,
            loading,
            onSubmit,
        }
    },
}
</script>

<style scoped>
.register-card {
    width: 100%;
    max-width: 400px;
}
</style>