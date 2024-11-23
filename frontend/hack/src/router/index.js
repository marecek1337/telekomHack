// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import MainScreen from '@/components/MainScreen.vue';
import ReportPage from '@/components/ReportPage.vue';
import LoadingPage from "@/components/LoadingPage";

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
  {
    path: "/loading",
    name: "LoadingPage",
    component: LoadingPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;