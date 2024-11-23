// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import MainScreen from '@/components/MainScreen.vue';
import ReportPage from '@/components/ReportPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainScreen,
  },
  {
    path: '/report',
    name: 'Report',
    component: ReportPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
