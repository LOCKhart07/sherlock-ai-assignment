import { coinApi } from 'src/boot/axios'
import { defineStore } from 'pinia'

export const useCoinStore = defineStore('coin', {
    state: () => ({
        coins: []
    }),

    actions: {
        async fetchCoins() {
            coinApi.get('ticker/24hr').then(response => {
                this.coins = response.data
                console.log(this.coins)
            })
        }
    }
})