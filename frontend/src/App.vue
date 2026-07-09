<script setup>
import { computed, ref } from 'vue'
import { useAppStore } from '@/stores/appStore'
const theme = ref('dark')
const sidebarCollapsed = ref(false)
const selectedPage = ref('chats')
const mergedView = ref(false)
const store = useAppStore()

const pages = [
  { id: 'chats', label: 'Чаты', icon: '💬', hint: 'Мульти-чат' },
  { id: 'alerts', label: 'Оповещения', icon: '🔔', hint: 'Уведомления' },
  { id: 'stats', label: 'Статистика', icon: '📊', hint: 'Аналитика' }
]

const widgets = ref([
  {
    id: 1,
    title: 'VK Live',
    service: 'vk',
    accentClass: 'accent-vk',
    messages: [
      { id: 1, text: 'Пользователь задал вопрос о новом стриме.' },
      { id: 2, text: 'Новый комментарий пришёл из сообщества.' }
    ]
  },
  {
    id: 2,
    title: 'YouTube',
    service: 'youtube',
    accentClass: 'accent-youtube',
    messages: [
      { id: 3, text: 'Подписчик оставил благодарность за видео.' },
      { id: 4, text: 'Появился новый комментарий из прямой трансляции.' }
    ]
  },
  {
    id: 3,
    title: 'Twitch',
    service: 'twitch',
    accentClass: 'accent-twitch',
    messages: [
      { id: 5, text: 'Быстрый ответ в чат для активной аудитории.' },
      { id: 6, text: 'Пользователь отправил эмодзи и реакцию.' }
    ]
  }
])

const removedWidgets = ref([])

const activeWidgets = computed(() => widgets.value)
const currentPage = computed(() => pages.find((page) => page.id === selectedPage.value))

const mergedMessages = computed(() =>
  activeWidgets.value.flatMap((widget) =>
    widget.messages.map((message) => ({ ...message, source: widget.title }))
  )
)

const visibleWidgets = computed(() => {
  if (!mergedView.value) {
    return activeWidgets.value
  }

  return [
    {
      id: 'combined',
      title: 'Объединённое окно',
      service: 'combined',
      accentClass: 'accent-combined',
      messages: mergedMessages.value
    }
  ]
})

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

const removeWidget = (widgetId) => {
  const index = widgets.value.findIndex((widget) => widget.id === widgetId)

  if (index === -1) {
    return
  }

  const [removed] = widgets.value.splice(index, 1)
  removedWidgets.value.push(removed)
}

const restoreWidget = (widgetId) => {
  const index = removedWidgets.value.findIndex((widget) => widget.id === widgetId)

  if (index === -1) {
    return
  }

  const [restored] = removedWidgets.value.splice(index, 1)
  widgets.value.push(restored)
}

const restoreAll = () => {
  if (!removedWidgets.value.length) {
    return
  }

  widgets.value.push(...removedWidgets.value)
  removedWidgets.value = []
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

          <button class="action-btn" @click="toggleMerge">
            {{ mergedView ? 'Разделить окна' : 'Объединить в одно' }}
          </button>
        </div>
      </header>

      <section class="content-grid">
        <div class="chat-area">
          <div class="window-toolbar">
            <div>
              <p class="toolbar-title">Центральная область</p>
              <p class="toolbar-subtitle">Окна можно удалять и возвращать из правой панели.</p>
            </div>
            <button v-if="removedWidgets.length" class="ghost-btn" @click="restoreAll">
              Вернуть всё
            </button>
          </div>

          <div class="chat-grid" :class="{ merged: mergedView }">
            <article
              v-for="widget in visibleWidgets"
              :key="widget.id"
              class="chat-card"
              :class="[widget.accentClass, { merged: mergedView }]"
            >
              <div class="chat-card-header">
                <div>
                  <p class="card-service">{{ mergedView ? 'Объединённое окно' : widget.service }}</p>
                  <h3>{{ mergedView ? 'Все сообщения в одном окне' : widget.title }}</h3>
                </div>
                <button
                  v-if="!mergedView"
                  class="close-btn"
                  @click="removeWidget(widget.id)"
                  aria-label="Удалить окно"
                >
                  ✕
                </button>
              </div>

              <div class="chat-body">
                <div v-for="message in widget.messages" :key="message.id" class="message-row">
                  <span class="message-source">{{ mergedView ? message.source : widget.title }}</span>
                  <p>{{ message.text }}</p>
                </div>
              </div>
            </article>
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

