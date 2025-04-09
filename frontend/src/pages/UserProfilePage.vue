<template>
    <q-page class="q-pa-md">
        <div class="row justify-center">
            <div class="col-12 col-md-8 col-lg-6">
                <q-card class="profile-card">
                    <q-card-section class="text-center">
                        <q-avatar size="100px" class="q-mb-md">
                            <img :src="user.photo_url || defaultAvatar" @error="handleImageError" />
                        </q-avatar>
                        <div class="text-h5">{{ user.full_name }}</div>
                        <div class="text-subtitle1">@{{ user.username }}</div>
                    </q-card-section>

                    <q-card-section>
                        <q-form @submit="onSubmit" class="q-gutter-md">
                            <q-input v-model="editForm.photo_url" label="Photo URL" outlined />

                            <q-input v-model="editForm.full_name" label="Full Name"
                                :rules="[val => !!val || 'Full name is required']" outlined />

                            <q-input v-model="editForm.email" label="Email" type="email" :rules="[
                                val => !!val || 'Email is required',
                                val => /^[^@]+@[^@]+\.[^@]+$/.test(val) || 'Invalid email format'
                            ]" outlined />

                            <q-input v-model="editForm.phone" label="Phone" outlined />

                            <q-input v-model="editForm.bio" label="Bio" type="textarea" outlined />
                            {{ editForm.password }}
                            <q-input v-model="editForm.password" label="New Password (leave blank to keep current)"
                                :type="isPwd ? 'password' : 'text'" outlined>
                                <template v-slot:append>
                                    <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                                        @click="isPwd = !isPwd" />
                                </template>
                            </q-input>

                            <div class="row q-gutter-sm justify-end">
                                <q-btn label="Cancel" color="grey" @click="cancelEdit" />
                                <q-btn label="Save Changes" type="submit" color="primary" :loading="loading" />
                            </div>
                        </q-form>
                    </q-card-section>

                    <q-card-actions align="right">
                        <q-btn color="negative" label="Logout" @click="logout" />
                    </q-card-actions>
                </q-card>
            </div>
        </div>
    </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import defaultAvatar from 'src/assets/default-avatar.png'

const $q = useQuasar()
const router = useRouter()
const user = ref({})
const editForm = ref({})
const isPwd = ref(true)
const loading = ref(false)
const { getUserProfile, updateUserProfile } = useAuthStore()

const fetchUserProfileLocal = async () => {
    try {
        const token = localStorage.getItem('token')
        if (!token) {
            router.push('/login')
            return
        }

        const response = await getUserProfile()
        user.value = response
        // Initialize edit form with current values
        editForm.value = {
            username: response.username,
            photo_url: response.photo_url || '',
            full_name: response.full_name,
            email: response.email,
            phone: response.phone || '',
            bio: response.bio || '',
            password: ''
        }

    } catch (error) {
        $q.notify({
            color: 'negative',
            message: error.message || 'Failed to fetch user profile',
        })
        console.log("error", error)
        router.push('/login')
    }
}

const onSubmit = async () => {
    try {
        loading.value = true
        console.log("editForm.value", editForm.value)
        // Remove empty password field
        if (!editForm.value.password) {
            delete editForm.value.password
        }

        const updatedUser = await updateUserProfile(editForm.value)
        if (editForm.value.password) {
            $q.notify({
                color: 'positive',
                message: 'Password updated successfully. Please login again.',
            })
            logout()

        }
        user.value = updatedUser

        $q.notify({
            color: 'positive',
            message: 'Profile updated successfully',
        })

        // Reset password field
        // editForm.value.password = ''

    } catch (error) {
        $q.notify({
            color: 'negative',
            message: error.message || 'Failed to update profile',
        })
    } finally {
        loading.value = false
    }
}

const cancelEdit = () => {
    // Reset form to current user values
    editForm.value = {
        photo_url: user.value.photo_url || '',
        full_name: user.value.full_name,
        email: user.value.email,
        phone: user.value.phone || '',
        bio: user.value.bio || '',
        password: ''
    }
}

const logout = () => {
    localStorage.removeItem('token')
    router.push('/login')
}

const handleImageError = (e) => {
    console.log("handleImageError", e)
    e.target.src = defaultAvatar
}

onMounted(() => {
    fetchUserProfileLocal()
})
</script>

<style scoped>
.profile-card {
    margin-top: 2rem;
}
</style>