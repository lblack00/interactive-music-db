import 'bootstrap/dist/css/bootstrap.css'
import './assets/main.css'
// Should be imported through main.css but I was unable to access it so I reimported it here - MS
import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')
