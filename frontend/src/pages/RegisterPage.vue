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

                    <div class="row items-center q-mb-md">
                        <div style="max-width: 500px;">
                            <q-btn-toggle v-model="photoInputType" size="md" toggle-color="primary" :options="[
                                { value: 'file', slot: 'file' },
                                { value: 'url', slot: 'url' }
                            ]" class="q-mr-md" style="flex: 1;">
                                <template v-slot:file>
                                    <div class="row items-center no-wrap">
                                        <div class="text-center">
                                            File
                                        </div>
                                        <q-icon right name="upload" size="18px" />
                                    </div>
                                </template>

                                <template v-slot:url>
                                    <div class="row items-center no-wrap">
                                        <div class="text-center">
                                            URL
                                        </div>
                                        <q-icon right name="link" size="18px" />
                                    </div>
                                </template>
                            </q-btn-toggle>
                        </div>

                        <div style="flex: 2;">
                            <q-input v-if="photoInputType === 'url'" v-model="photoUrl" label="Photo URL" outlined dense
                                style="width: 100%;" />
                            <q-file v-else v-model="photoFile" label="Upload Photo" outlined dense
                                accept=".jpg,.jpeg,.png" @update:model-value="handleFileUpload" style="width: 100%;">
                                <template v-slot:prepend>
                                    <q-icon name="attach_file" size="18px" />
                                </template>
                            </q-file>
                        </div>
                    </div>

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
import { useAuthStore } from 'src/stores/auth'

export default {
    name: 'RegisterPage',
    setup() {
        const $q = useQuasar()
        const router = useRouter()
        const authStore = useAuthStore()
        const email = ref('')
        const username = ref('')
        const password = ref('')
        const fullName = ref('')
        const bio = ref('')
        const phone = ref('')
        const photoUrl = ref('')
        const photoFile = ref(null)
        const photoInputType = ref('url')
        const isPwd = ref(true)
        const loading = ref(false)

        const handleFileUpload = async (file) => {
            if (!file) return

            try {
                const formData = new FormData()
                formData.append('photo', file)

                const reader = new FileReader()
                reader.onload = (e) => {
                    photoUrl.value = e.target.result
                }
                reader.readAsDataURL(file)
            } catch (error) {
                $q.notify({
                    color: 'negative',
                    message: 'Failed to process image file' + error,
                })
            }
        }

        const onSubmit = async () => {
            try {
                loading.value = true
                await authStore.register({
                    email: email.value,
                    username: username.value,
                    password: password.value,
                    full_name: fullName.value,
                    bio: bio.value,
                    phone: phone.value,
                    photo_url: photoUrl.value,
                })

                $q.notify({
                    color: 'positive',
                    message: 'Registration successful! Please login.',
                })
                router.push('/login')
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
            photoFile,
            photoInputType,
            isPwd,
            loading,
            onSubmit,
            handleFileUpload,
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