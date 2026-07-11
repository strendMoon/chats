import { createRouter, createWebHistory } from 'vue-router';
import Chats from '../pages/Chats.vue';
import Alerts from '../pages/Alerts.vue';
import Statistics from '../pages/Statistics.vue';
import Home from '../pages/Home.vue';


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/chats',
    name: 'Chats',
    component: Chats
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;