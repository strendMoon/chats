import { defineStore } from 'pinia'

export const useAppStore = defineStore('appState', {
  state: () => ({
    buttons: {
      sidebarOpen: true,
      currentPage: 'home',
    },
    theme: 'dark',
    sidebarCollapsed: false,
  }),
  getters: {
    currentPageObject(state) {
    const pages = [
      { id: 'chats', label: 'Чаты', icon: '💬', router_link: '/chats' },
      { id: 'alerts', label: 'Оповещения', icon: '🔔', router_link: '/alerts' },
      { id: 'stats', label: 'Статистика', icon: '📊', router_link: '/statistics' },
      { id: 'home', label: 'Workspace', icon: '🏠', router_link: '/' },
    ];
      return pages.find(p => p.id === state.buttons.currentPage) || pages[0];
    },
    currentPageLabel(state) {
      return this.currentPageObject?.label || 'Workspace';
    }
  },
  actions: {
    setTheme(value) {
      this.theme = value;
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark';
    },
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    setCurrentPage(pageId) {
      this.buttons.currentPage = pageId;
    },
  },
  persist: true,
});