<script setup>
import {computed } from 'vue';
import { useAppStore } from '@/stores/index.js';
import { storeToRefs } from 'pinia';

import { pageComponents } from './pages/index.js';
import NavPannel from './navigation/NavPannel.vue';
import TopBar from './navigation/TopBar.vue';

const store = useAppStore();
const { theme, sidebarCollapsed, buttons} = storeToRefs(store);
const { toggleSidebar, setTheme } = store;

const toggleTheme = () => {
  store.toggleTheme();
};
const currentPageId = computed(() => buttons.value.currentPage);
</script>

<template>
  <div class="app-shell" :class="theme === 'dark' ? 'theme-dark' : 'theme-light'">
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-head">
        <button class="icon-btn" @click="toggleSidebar" aria-label="Скрыть меню">
          ☰
        </button>
        <span v-if="!sidebarCollapsed" class="sidebar-title">Menu</span>
      </div>
      <NavPannel />
      <sideBar/>
    </aside>
    <main class="workspace">
      <TopBar />
      <section class="content-grid">
        <div v-if="!pageComponents[currentPageId]">Нет компонента для страницы {{ currentPageId }}</div>
        <component v-else :is="pageComponents[currentPageId]" />
        <!-- <aside class="restore-panel">
          <h3>Удалённые окна</h3>
          <p class="restore-help">Возвращайте любое окно обратно в список чатов.</p>
          <div class="restore-list">
            <div v-for="widget in removedWidgets" :key="widget.id" class="restore-item">
              <div>
                <strong>{{ widget.title }}</strong>
                <span>{{ widget.service }}</span>
              </div>
              <button class="restore-btn" @click="restoreWidget(widget.id)">Вернуть</button>
            </div>
          </div>
          <div class="restore-empty">
            Список пуст. Удалите окно, чтобы оно появилось здесь.
          </div>
        </aside> -->
      </section>
    </main>
  </div>
</template>

<style scoped src="./assets/app-dashboard.css"></style>