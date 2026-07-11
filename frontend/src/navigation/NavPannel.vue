
<template>
  <div class="nav-panel">
    <nav class="page-nav">
      <router-link
        v-for="page in pages"
        :key="page.id"
        :to="page.router_link"
        class="page-btn"
        :class="{ active: currentPage === page.id }"
        @click="selectPage(page.id)"
        :title="page.label"
      >
        <span class="page-icon">{{ page.icon }}</span>
        <span v-if="!sidebarCollapsed" class="page-label">{{ page.label }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { useAppStore } from '../stores/index.js';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const store = useAppStore();
const { buttons, sidebarCollapsed } = storeToRefs(store);

const currentPage = computed(() => buttons.value.currentPage);

const pages = [
  { id: 'chats', label: 'Чаты', icon: '💬', router_link: '/chats' },
  { id: 'alerts', label: 'Оповещения', icon: '🔔', router_link: '/alerts' },
  { id: 'stats', label: 'Статистика', icon: '📊', router_link: '/statistics' },
  { id: 'home', label: 'Workspace', icon: '🏠', router_link: '/' },
];

const selectPage = (pageId) => {
  store.setCurrentPage(pageId);
};

</script>
<style scoped src="../assets/app-dashboard.css"></style>