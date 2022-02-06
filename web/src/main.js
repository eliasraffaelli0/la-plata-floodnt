import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "leaflet/dist/leaflet.css";
import '../dist/css/style.css';

 createApp(App).use(router).mount('#app')
