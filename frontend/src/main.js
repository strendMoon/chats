import './assets/main.css'

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import { createApp } from 'vue'
import App from './App.vue'


const app = createApp(App)
app.mount('#app')

const userStore = useUserStore()


