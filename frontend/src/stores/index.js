import { defineStore } from 'pinia'
import {pages_config} from '../pages/index.js'
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
    pages() {
      return pages_config;
    },
    currentPageObject(state) {
      const pages = this.pages;
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