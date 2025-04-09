<template>
    <q-page class="q-pa-md">
        <div class="row justify-center">
            <div class="col-12 col-md-8 col-lg-6">
                <q-card class="profile-card">
                    <q-card-section class="text-center">
                        <q-avatar size="100px" class="q-mb-md">
                            <img :src="user.photo_url || 'https://cdn.quasar.dev/img/avatar.png'" />
                        </q-avatar>
                        <div class="text-h5">{{ user.full_name }}</div>
                        <div class="text-subtitle1">@{{ user.username }}</div>
                    </q-card-section>

                    <q-card-section>
                        <q-list>
                            <q-item>
                                <q-item-section>
                                    <q-item-label caption>Email</q-item-label>
                                    <q-item-label>{{ user.email }}</q-item-label>
                                </q-item-section>
                            </q-item>

                            <q-item v-if="user.phone">
                                <q-item-section>
                                    <q-item-label caption>Phone</q-item-label>
                                    <q-item-label>{{ user.phone }}</q-item-label>
                                </q-item-section>
                            </q-item>

                            <q-item v-if="user.bio">
                                <q-item-section>
                                    <q-item-label caption>Bio</q-item-label>
                                    <q-item-label>{{ user.bio }}</q-item-label>
                                </q-item-section>
                            </q-item>
                        </q-list>
                    </q-card-section>

                    <q-card-actions align="right">
                        <q-btn color="negative" label="Logout" @click="logout" />
                    </q-card-actions>
                </q-card>
            </div>
        </div>
    </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

export default {
    name: 'UserProfilePage',
    setup() {
        const $q = useQuasar()
        const router = useRouter()
        const user = ref({})

        const fetchUserProfile = async () => {
            try {
                const token = localStorage.getItem('token')
                if (!token) {
                    router.push('/login')
                    return
                }

                const response = await fetch('http://localhost:8000/users/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })

                if (response.ok) {
                    user.value = await response.json()
                } else {
                    throw new Error('Failed to fetch user profile')
                }
            } catch (error) {
                $q.notify({
                    color: 'negative',
                    message: error.message || 'Failed to fetch user profile',
                })
                router.push('/login')
            }
        }

        const logout = () => {
            localStorage.removeItem('token')
            router.push('/login')
        }

        onMounted(() => {
            fetchUserProfile()
        })

        return {
            user,
            logout,
        }
    },
}
</script>

<style scoped>
.profile-card {
    margin-top: 2rem;
}
</style>