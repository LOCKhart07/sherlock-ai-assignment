<template>
    <div>
        <h1>Coin Page</h1>
    </div>
    <div class="q-pa-md">
        <q-table title="Coins" :rows="coins" row-key="name" :pagination="{ rowsPerPage: 10 }" />
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCoinStore } from 'src/stores/coin'

const coinStore = useCoinStore()

const { coins } = storeToRefs(coinStore)
// const columns = [
//     { name: 'symbol', label: 'Symbol', align: 'left', field: 'symbol' },
//     { name: 'priceChange', label: 'Price Change', align: 'right', field: 'priceChange' },
//     { name: 'lastPrice', label: 'Last Price', align: 'right', field: 'lastPrice' },
//     { name: 'highPrice', label: 'High Price', align: 'right', field: 'highPrice' },
//     { name: 'lowPrice', label: 'Low Price', align: 'right', field: 'lowPrice' },
//     { name: 'volume', label: 'Volume', align: 'right', field: 'volume' }
// ]


onMounted(async () => {
    await coinStore.fetchCoins()
})
</script>
