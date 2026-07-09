import { defineStore } from 'pinia'

export const useAppStore = defineStore('appState', {
  state: () => ({
    // Состояние кнопок (ключ — ID или имя кнопки, значение — true/false)
    buttons: {
      sidebarOpen: true,
      darkMode: false,
      notificationsEnabled: false,
    },
    // Токены для внешних интеграций
    externalTokens: {
      crmService: '',
      billingApi: '',
      analyticsPlatform: '',
    }
  }),
  actions: {
    // Метод для переключения конкретной кнопки
    toggleButton(buttonKey) {
      if (buttonKey in this.buttons) {
        this.buttons[buttonKey] = !this.buttons[buttonKey]
      }
    },
    // Метод для обновления конкретного токена
    setExternalToken(serviceName, token) {
      this.externalTokens[serviceName] = token
    }
  },
  // Плагин автоматически сохранит всё это в localStorage
  persist: true, 
})