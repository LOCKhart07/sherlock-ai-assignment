<template>
    <q-page class="q-pa-md">
        <div class="row q-col-gutter-md">
            <!-- Header Section -->
            <div class="col-12">
                <div class="row items-center justify-between q-mb-md">
                    <div class="text-h5 q-ma-none">Weather Stations</div>
                    <div class="row items-center q-gutter-md">
                        <q-btn-toggle v-model="viewMode" :options="[
                            { label: 'Map View', icon: 'map', value: 0 },
                            { label: 'Table View', icon: 'table_chart', value: 1 }
                        ]" />
                    </div>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="stations.length === 0" class="col-12 flex flex-center" style="min-height: 400px">
                <q-spinner color="primary" size="3em" />
            </div>

            <!-- Content Section -->
            <div v-else class="col-12">
                <!-- Weather Map -->
                <div v-show="viewMode === 0" class="map-container q-mb-md">
                    <div id="weather-map" ref="mapRef"></div>
                </div>

                <!-- Weather Table -->
                <q-card v-show="viewMode" class="q-mb-md">
                    <q-card-section>
                        <div class="text-h6">Station Readings</div>
                    </q-card-section>
                    <q-card-section>
                        <q-table :rows="tableData" :columns="columns" row-key="id" :pagination="{ rowsPerPage: 10 }"
                            flat bordered>
                            <template v-slot:body-cell-temperature="props">
                                <q-td :props="props">
                                    <q-chip :color="getTemperatureColor(props.value)" text-color="white" dense>
                                        {{ props.value }}°C
                                    </q-chip>
                                </q-td>
                            </template>
                        </q-table>
                    </q-card-section>
                </q-card>
            </div>
        </div>
    </q-page>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useWeatherStore } from 'src/stores/weather'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const { fetchWeather } = useWeatherStore()
const weatherStore = useWeatherStore()
const { stations } = storeToRefs(weatherStore)
const tableData = ref([])
const mapRef = ref(null)
const viewMode = ref(0) // 0 for map view, 1 for table view
let map = null

// Date handling
const yesterday = new Date()
yesterday.setDate(yesterday.getDate() - 1)
const selectedDate = ref(yesterday.toISOString().split('T')[0].replace(/-/g, '/'))

// Temperature color function
const getTemperatureColor = (temp) => {
    if (temp <= 0) return 'blue'
    if (temp <= 10) return 'cyan'
    if (temp <= 20) return 'green'
    if (temp <= 30) return 'orange'
    return 'red'
}

// Create custom icon for weather stations
const weatherIcon = L.icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
})

// Initialize map and add markers
const initializeMap = () => {
    if (!mapRef.value) return

    // Initialize map if not already done
    if (!map) {
        map = L.map(mapRef.value).setView([0, 0], 2)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map)
    }

    // Clear existing markers
    map.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer)
        }
    })

    // Create a bounds object to store all marker positions
    const bounds = L.latLngBounds([])

    // Add markers for each station
    stations.value.forEach(station => {
        const { latitude, longitude } = station.location
        const marker = L.marker([latitude, longitude], { icon: weatherIcon })
            .bindPopup(`
                <div class="station-popup">
                    <strong>${station.name}</strong><br>
                    Temperature: <span style="color: ${getTemperatureColor(station.temperature)}">${station.temperature}°C</span><br>
                    ID: ${station.id}
                </div>
            `)
        marker.addTo(map)
        bounds.extend([latitude, longitude])
    })

    map.fitBounds(bounds, {
        padding: [50, 50],
        maxZoom: 10
    })

    // Force a map refresh
    map.invalidateSize()
}

// Watch for changes in stations data
watch(stations, () => {
    if (viewMode.value === 0) {
        initializeMap()
    }
}, { deep: true })

// Watch for date changes
watch(selectedDate, async (newDate) => {
    await fetchWeather(newDate)
    initializeMap()
})

const columns = [
    {
        name: 'id',
        required: true,
        label: 'Station ID',
        align: 'left',
        field: row => row.id,
        sortable: true
    },
    {
        name: 'name',
        required: true,
        label: 'Station Name',
        align: 'left',
        field: row => row.name,
        sortable: true
    },
    {
        name: 'latitude',
        required: true,
        label: 'Latitude',
        align: 'left',
        field: row => row.location.latitude,
        sortable: true
    },
    {
        name: 'longitude',
        required: true,
        label: 'Longitude',
        align: 'left',
        field: row => row.location.longitude,
        sortable: true
    },
    {
        name: 'temperature',
        required: true,
        label: 'Temperature',
        align: 'left',
        field: row => row.temperature,
        sortable: true
    }
]

onMounted(async () => {
    await fetchWeather(null)
    tableData.value = stations.value
    if (viewMode.value === 0) {
        initializeMap()
    }
})
</script>

<style scoped>
.map-container {
    position: relative;
    height: 600px;
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#weather-map {
    height: 100%;
    width: 100%;
}

.station-popup {
    padding: 5px;
    min-width: 150px;
}

:deep(.leaflet-popup-content-wrapper) {
    border-radius: 8px;
}

:deep(.leaflet-popup-content) {
    margin: 10px;
}
</style>
