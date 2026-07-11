<script setup>
import { useAppStore } from '@/stores/index.js';
import { storeToRefs } from 'pinia';

const store = useAppStore();
const { theme } = storeToRefs(store);
const { setTheme } = store;
</script>

<template>
  <header class="topbar">
    <div>
      <p class="eyebrow">Multi-chat workspace</p>
      <h1>{{ store.currentPageLabel }}</h1>
    </div>
    <div class="topbar-actions">
      <div class="theme-switch" role="group" aria-label="Выбор темы">
        <button class="switch-btn" :class="{ active: theme === 'light' }" @click="setTheme('light')">
          Светлая
        </button>
        <button class="switch-btn" :class="{ active: theme === 'dark' }" @click="setTheme('dark')">
          Темная
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped src="../assets/app-dashboard.css"></style>