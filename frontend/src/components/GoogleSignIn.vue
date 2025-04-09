<template>
    <div class="google-sign-in">
        <div id="g_id_onload" :data-client_id="clientId" data-context="signin" data-ux_mode="popup"
            data-auto_prompt="false"></div>
        <div class="g_id_signin" data-type="standard" data-shape="rectangular" data-theme="outline"
            data-text="signin_with" data-size="large" data-logo_alignment="left"></div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'src/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

onMounted(() => {
    // Wait for Google script to load
    const waitForGoogle = setInterval(() => {
        if (window.google) {
            clearInterval(waitForGoogle)
            // Initialize Google Sign-In
            window.google.accounts.id.initialize({
                client_id: clientId,
                callback: handleCredentialResponse,
                ux_mode: 'popup',
                auto_select: false,
                context: 'signin'
            })
            window.google.accounts.id.renderButton(
                document.querySelector('.g_id_signin'),
                {
                    theme: 'outline',
                    size: 'large',
                    type: 'standard',
                    text: 'signin_with',
                    shape: 'rectangular',
                    logo_alignment: 'left'
                }
            )
        }
    }, 100)
})

// Define the callback function outside onMounted to avoid recreation
async function handleCredentialResponse(response) {
    console.log("handleCredentialResponse")
    console.log(response.credential)
    try {
        await new Promise(resolve => setTimeout(resolve, 500));
        const result = await authStore.googleSignIn(response.credential)
        if (result) {
            router.push('/profile')
        }
    } catch (error) {
        console.error('Google sign-in error:', error)
    }
}
</script>

<style scoped>
.google-sign-in {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
}
</style>