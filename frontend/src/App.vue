<script setup>
import { computed, ref } from 'vue'
import { useAppStore } from '@/stores/appStore'

import { YoutubeChat, TwitchChat, VkliveChat} from './widgets/chats/chats_import.js'

const theme = ref('dark')
const sidebarCollapsed = ref(false)
const selectedPage = ref('chats')
const store = useAppStore()

const pages = [
  { id: 'chats', label: 'Чаты', icon: '💬', hint: 'Мульти-чат' },
  { id: 'alerts', label: 'Оповещения', icon: '🔔', hint: 'Уведомления' },
  { id: 'stats', label: 'Статистика', icon: '📊', hint: 'Аналитика' }
]
console.log(YoutubeChat)
const removedWidgets = ref([])
const currentPage = computed(() => pages.find((page) => page.id === selectedPage.value))


const toggleTheme = () => {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
}

const setTheme = (value) => {
  theme.value = value
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const selectPage = (pageId) => {
  selectedPage.value = pageId
}

const toggleMerge = () => {
  mergedView.value = !mergedView.value
}
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

      <nav class="page-nav">
        <button
          v-for="page in pages"
          :key="page.id"
          class="page-btn"
          :class="{ active: selectedPage === page.id }"
          @click="selectPage(page.id)"
          :title="page.label"
        >
          <span class="page-icon">{{ page.icon }}</span>
          <span v-if="!sidebarCollapsed" class="page-label">{{ page.label }}</span>
        </button>
      </nav>

      <div class="sidebar-foot">
        <button class="icon-btn" aria-label="Настройки">⚙️</button>
      </div>
    </aside>

    <main class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">Multi-chat workspace</p>
          <h1>{{ currentPage?.label || 'Чаты' }}</h1>
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

      <section class="content-grid">
        <div class="chat-area">
          <div class="chat-grid">
            <YoutubeChat />
          </div>
        </div>

        <aside class="restore-panel">
          <h3>Удалённые окна</h3>
          <p class="restore-help">Возвращайте любое окно обратно в список чатов.</p>

          <div v-if="removedWidgets.length" class="restore-list">
            <div v-for="widget in removedWidgets" :key="widget.id" class="restore-item">
              <div>
                <strong>{{ widget.title }}</strong>
                <span>{{ widget.service }}</span>
              </div>
              <button class="restore-btn" @click="restoreWidget(widget.id)">Вернуть</button>
            </div>
          </div>

          <div v-else class="restore-empty">
            Список пуст. Удалите окно, чтобы оно появилось здесь.
          </div>
        </aside>
      </section>
    </main>
  </div>
</template>

<style scoped src="./assets/app-dashboard.css"></style>

