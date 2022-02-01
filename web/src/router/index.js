import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Form from '../views/Form.vue'
import PuntosYRecorridos from '../views/PuntosYRecorridos.vue'
import Zonas from '../views/Zonas.vue'
import ZonaEspecifica from '../views/ZonaEspecifica.vue'
import Reports from '../views/Reports.vue'
import ReportsMap from '../views/ReportsMap.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/formulario',
    name: 'Form',
    component: Form
  },
  {
    path: '/reports',
    name: 'Denuncias',
    component: Reports
  },
  {
    path: '/reportsMap',
    name: 'DenunciasMapa',
    component: ReportsMap
  },
  {
    path: '/recorridos_y_puntos',
    name: 'recorridosYPuntos',
    component: PuntosYRecorridos
  },
  {
    path: '/zonas',
    name: 'zonas',
    component: Zonas
  },
  {
    path: '/zonaEspecifica/:id',
    name: 'zonaEspecifica',
    component: ZonaEspecifica
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
