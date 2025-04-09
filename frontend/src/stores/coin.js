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
        },


        async fetchKlines(symbol, interval) {
            try {
                const response = await coinApi.get(`uiKlines?symbol=${symbol}&interval=${interval}`);
                return response.data;
            } catch (error) {
                console.error('Error fetching klines:', error);
                throw error; // Rethrow the error for further handling if needed
            }
        }
    },
})