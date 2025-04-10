<template>
    <div class="coin-page">
        <h1 class="text-h3">Cryptocurrency Overview</h1>
        <p class="description">Explore the latest trends and prices in the cryptocurrency market.</p>
    </div>

    <div class="q-pa-md">
        <q-table title="Cryptocurrency Market" :rows="coins" :columns="columns" row-key="symbol"
            :pagination="{ rowsPerPage: 10 }" @row-click="onRowClick" />

        <q-dialog v-model="showCoinDetails" maximized>
            <q-card class="full-width">
                <q-card-section class="row items-center q-pb-none">
                    <div class="text-h6">{{ selectedCoin?.symbol }}</div>
                    <q-space />
                    <q-btn icon="close" flat round dense v-close-popup />
                </q-card-section>

                <q-card-section v-if="selectedCoin">
                    <div class="row q-col-gutter-md">
                        <!-- Price Information -->
                        <div class="col-12">
                            <div class="text-h4">
                                {{ selectedCoin.lastPrice }}
                                <q-chip :color="getPriceChangeColor(selectedCoin.priceChangePercent)"
                                    text-color="white">
                                    {{ selectedCoin.priceChangePercent }}%
                                    <q-icon :name="getPriceChangeIcon(selectedCoin.priceChangePercent)"
                                        class="q-ml-sm" />
                                </q-chip>
                            </div>
                        </div>

                        <!-- Chart Section -->
                        <div class="col-12 chart-container">
                            <Line :options="chartOptions" :data="chartData" />
                        </div>

                        <!-- Price Stats -->
                        <div class="col-12 col-md-6">
                            <q-list>
                                <q-item>
                                    <q-item-section>
                                        <q-item-label caption>24h High</q-item-label>
                                        <q-item-label>{{ selectedCoin.highPrice }}</q-item-label>
                                    </q-item-section>
                                </q-item>
                                <q-item>
                                    <q-item-section>
                                        <q-item-label caption>24h Low</q-item-label>
                                        <q-item-label>{{ selectedCoin.lowPrice }}</q-item-label>
                                    </q-item-section>
                                </q-item>
                            </q-list>
                        </div>

                        <!-- Volume Stats -->
                        <div class="col-12 col-md-6">
                            <q-list>
                                <q-item>
                                    <q-item-section>
                                        <q-item-label caption>Volume</q-item-label>
                                        <q-item-label>{{ selectedCoin.volume }}</q-item-label>
                                    </q-item-section>
                                </q-item>
                                <q-item>
                                    <q-item-section>
                                        <q-item-label caption>Quote Volume</q-item-label>
                                        <q-item-label>{{ selectedCoin.quoteVolume }}</q-item-label>
                                    </q-item-section>
                                </q-item>
                            </q-list>
                        </div>

                        <!-- Market Stats -->
                        <div class="col-12">
                            <q-list bordered class="rounded-borders">
                                <q-item>
                                    <q-item-section>
                                        <q-item-label caption>Bid Price</q-item-label>
                                        <q-item-label>{{ selectedCoin.bidPrice }} ({{ selectedCoin.bidQty
                                            }})</q-item-label>
                                    </q-item-section>
                                </q-item>
                                <q-item>
                                    <q-item-section>
                                        <q-item-label caption>Ask Price</q-item-label>
                                        <q-item-label>{{ selectedCoin.askPrice }} ({{ selectedCoin.askQty
                                            }})</q-item-label>
                                    </q-item-section>
                                </q-item>
                            </q-list>
                        </div>
                    </div>
                </q-card-section>
            </q-card>
        </q-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCoinStore } from 'src/stores/coin'
import { Line } from 'vue-chartjs'

const coinStore = useCoinStore()
const { coins } = storeToRefs(coinStore)
const { fetchKlines } = useCoinStore()
const showCoinDetails = ref(false)
const selectedCoin = ref(null)

import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Price History'
        }
    },
    scales: {
        y: {
            beginAtZero: false,
            grid: {
                display: true,
                color: 'rgba(0, 0, 0, 0.1)'
            }
        },
        x: {
            grid: {
                display: false
            }
        }
    }
}
const chartData = ref({
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
        {
            label: 'Price History',
            backgroundColor: '#f87979',
            data: [65, 59, 80, 81, 56, 55, 40],
            borderColor: '#f87979',
            tension: 0.1
        }
    ]
})

const columns = [
    {
        name: 'symbol',
        label: 'Symbol',
        align: 'left',
        field: 'symbol',
        sortable: true
    },
    {
        name: 'lastPrice',
        label: 'Price',
        align: 'right',
        field: 'lastPrice',
        sortable: true
    },
    {
        name: 'priceChangePercent',
        label: 'Change 24h',
        align: 'right',
        field: 'priceChangePercent',
        sortable: true,
        format: (val) => `${val}%`,
        style: (val) => ({ color: val.priceChangePercent >= 0 ? 'green' : 'red' })
    },
    {
        name: 'volume',
        label: 'Volume',
        align: 'right',
        field: 'volume',
        sortable: true
    },
    {
        name: 'highPrice',
        label: '24h High',
        align: 'right',
        field: 'highPrice',
        sortable: true
    },
    {
        name: 'lowPrice',
        label: '24h Low',
        align: 'right',
        field: 'lowPrice',
        sortable: true
    }
]

const klines = ref([])

function onRowClick(evt, row) {
    selectedCoin.value = row
    fetchKlines(row.symbol, '1m').then(data => {
        klines.value = data
        console.log('klines', klines.value)
        updateChartData(klines.value)
    })
    showCoinDetails.value = true
}

function updateChartData(klines) {
    const labels = klines.map(kline => new Date(kline[0]).toLocaleTimeString())
    const data = klines.map(kline => parseFloat(kline[4]))

    chartData.value = {
        labels: labels,
        datasets: [
            {
                label: 'Price History',
                backgroundColor: '#f87979',
                data: data,
                borderColor: '#f87979',
                tension: 0.1
            }
        ]
    }
}

function getPriceChangeColor(change) {
    return parseFloat(change) >= 0 ? 'positive' : 'negative'
}

function getPriceChangeIcon(change) {
    return parseFloat(change) >= 0 ? 'arrow_upward' : 'arrow_downward'
}


import { useAuthStore } from 'src/stores/auth'
const authStore = useAuthStore()

onMounted(async () => {
    if (!authStore.isAuthenticated) {
        authStore.logout()
        $q.notify({
            color: 'negative',
            message: 'Please login to continue.',
        })
        router.push('/login')
        return
    }
    await coinStore.fetchCoins()
})
</script>

<style scoped>
.positive {
    background-color: #21ba45 !important;
    color: white;
    padding: 5px;
    border-radius: 5px;
}

.negative {
    background-color: #c10015 !important;
    color: white;
    padding: 5px;
    border-radius: 5px;
}

.coin-page {
    text-align: center;
    margin-bottom: 20px;
}

.text-h3 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 10px;
}

.description {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 20px;
}

.q-table {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}

.q-table th {
    background-color: #f5f5f5;
    font-weight: bold;
    text-align: left;
}

.q-table td {
    padding: 10px;
    border-bottom: 1px solid #eee;
}

.q-table tr:hover {
    background-color: #f9f9f9;
}

.chart-container {
    position: relative;
    height: 400px;
    width: 100%;
    margin: 20px 0;
}

.full-width {
    width: 90vw;
    max-width: 1200px;
}

@media (max-width: 768px) {
    .text-h3 {
        font-size: 2rem;
    }

    .description {
        font-size: 1rem;
    }

    .q-table th,
    .q-table td {
        padding: 8px;
    }
}
</style>
