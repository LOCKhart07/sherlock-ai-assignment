import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null
    }),

    getters: {
        isAuthenticated: (state) => !!state.token,
        getUser: (state) => state.user
    },

    actions: {
        async register(userData) {
            try {
                const response = await api.post('/register', userData)
                if (response.status === 200) {
                    this.setAuth(response.data)
                    return true
                } else {
                    console.log("response errorrrr", response.data)
                    throw new Error(response.data.detail || 'Registration failed')
                }
            }
            catch (error) {
                console.log("response terrorrrr", error.response.data)
                throw new Error(error.response.data.detail || 'Registration failed')
            }

        },

        async login(username, password) {
            try {
                const formData = new FormData()
                formData.append('username', username)
                formData.append('password', password)

                const response = await api.post('/token', formData)
                this.setAuth(response.data)
                return true
            } catch (error) {
                console.error('Login error:', error)
                return false
            }
        },

        async getUserProfile() {
            console.log("getUserProfile", this.token)
            const response = await api.get('/users/me', {
                headers: {
                    Authorization: `Bearer ${this.token}`
                }
            })
            return response.data
        },

        async updateUserProfile(userData) {
            try {
                const response = await api.put('/users/me', userData, {
                    headers: {
                        Authorization: `Bearer ${this.token}`
                    }
                })
                return response.data
            } catch (error) {
                console.error('Update profile error:', error)
                throw error
            }
        },

        async googleSignIn(credential) {
            console.log("googleSignIn", credential)
            try {
                const response = await api.post('/google', { token: credential })
                this.setAuth(response.data)
                return true
            } catch (error) {
                console.error('Google sign-in error:', error)
                return false
            }
        },

        setAuth(data) {
            this.token = data.access_token
            localStorage.setItem('token', data.access_token)

            // Set the token in axios defaults
            api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
        },

        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            delete api.defaults.headers.common['Authorization']
        }
    }
}) 