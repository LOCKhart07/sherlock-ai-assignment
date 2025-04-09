import { weatherApi } from 'src/boot/axios'
import { defineStore } from 'pinia'

export const useWeatherStore = defineStore('weather', {
    state: () => ({
        stations: []
    }),

    actions: {
        async fetchWeather(date) {
            this.stations = []
            const params = date ? { date: date.replace(/\//g, '-') } : {};
            return weatherApi.get('environment/air-temperature', { params }).then(response => {
                console.log("response", response);
                this.stations = response.data.metadata.stations.map(station => {
                    const reading = response.data.items[0].readings.find(r => r.station_id === station.id);
                    return {
                        ...station,
                        temperature: reading ? reading.value : null
                    };
                });
                console.log("this.stations", this.stations);
            });
        }
    },
})