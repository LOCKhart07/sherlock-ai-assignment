<template>
    <div class="q-pa-md">
        <div class="row items-center q-mb-md">
            <h1 class="q-ma-none">Weather Stations</h1>
            <q-space />
            <div class="row items-center q-gutter-md">
                <!-- <div class="q-pa-md" style="max-width: 300px">
                    <q-input filled v-model="selectedDate" mask="date" :rules="['date']">
                        <template v-slot:append>
                            <q-icon name="event" class="cursor-pointer">
                                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                    <q-date v-model="selectedDate">
                                        <div class="row items-center justify-end">
                                            <q-btn v-close-popup label="Close" color="primary" flat />
                                        </div>
                                    </q-date>
                                </q-popup-proxy>
                            </q-icon>
                        </template>
</q-input>
</div> -->
                <q-btn-toggle v-model="viewMode" :options="[
                    { label: 'Map View', icon: 'map', value: 0 },
                    { label: 'Table View', icon: 'table_chart', value: 1 }
                ]" />
            </div>
        </div>

        <div v-if="stations.length === 0" class="q-pa-md">
            <q-spinner color="primary" />
        </div>
        <div v-else>
            <!-- Weather Map -->
            <div v-show="viewMode === 0" class="map-container q-mb-md">
                <div id="weather-map" ref="mapRef"></div>
            </div>

            <!-- Weather Table -->
            <q-table v-show="viewMode" title="Weather Station Readings" :rows="tableData" :columns="columns"
                row-key="id" :pagination="{ rowsPerPage: 10 }">
                <template v-slot:body-cell-temperature="props">
                    <q-td :props="props">
                        {{ props.value }}°C
                    </q-td>
                </template>
            </q-table>
        </div>
    </div>
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

// Watch for date changes
watch(selectedDate, async (newDate) => {
    await fetchWeather(newDate)
    initializeMap()
})

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
                <strong>${station.name}</strong><br>
                Temperature: ${station.temperature}°C<br>
                ID: ${station.id}
            `)
        marker.addTo(map)
        console.log("marker", marker)
        bounds.extend([latitude, longitude])
    })

    map.fitBounds(bounds, {
        padding: [50, 50], // Add padding around the bounds
        maxZoom: 10 // Prevent zooming in too close
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

// watch(viewMode, () => {
//     if (viewMode.value === 0) {
//         initializeMap()
//     }
// })


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
    await fetchWeather()
    tableData.value = stations.value
    if (viewMode.value === 0) {
        initializeMap()
    }
})
</script>

<style scoped>
.q-pa-md {
    padding: 16px;
}

.map-container {
    position: relative;
    height: 500px;
    width: 100%;
    margin: 20px 0;
}

#weather-map {
    height: 100%;
    width: 100%;
    border-radius: 8px;
    border: 1px solid #ddd;
}
</style>
