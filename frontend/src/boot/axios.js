import { defineBoot } from '#q-app/wrappers'
import axios from 'axios'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)

const api = axios.create({ baseURL: 'http://localhost:3000/api' })
const coinApi = axios.create({ baseURL: 'https://data-api.binance.vision/api/v3' })
const weatherApi = axios.create({ baseURL: 'https://api.data.gov.sg/v1/' })
export default defineBoot(({ app }) => {
  // for use inside Vue files (Composition API) through inject
  app.provide('axios', axios)
  app.provide('api', api)
  app.provide('coinApi', coinApi)
  app.provide('weatherApi', weatherApi)
})

export { api, coinApi, weatherApi }
