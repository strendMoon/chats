<template>
  <div class="youtube-chat-widget">
    <!-- Шапка виджета -->
    <div class="chat-header">
      <div class="header-left">
        <span class="youtube-icon">▶️</span>
        <span class="platform-name">YouTube</span>
        <span class="live-badge">LIVE</span>
      </div>
      <div class="header-right">
        <span class="viewers-count">👁️ 1.2K</span>
        <button class="settings-btn" title="Настройки">⚙️</button>
      </div>
    </div>

    <!-- Область сообщений с прокруткой -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in youTube_chat_widgets[0]?.messages || []"
        :key="index"
        class="message-item"
        :class="{
          'same-user': index > 0 && message.name === youTube_chat_widgets[0].messages[index - 1].name
        }"
      >
        <!-- Аватарка (только если сообщение от нового пользователя) -->
        <div v-if="!sameUser(index)" class="avatar">
          {{ getInitials(message.name) }}
        </div>
        <div v-else class="avatar-placeholder"></div>

        <!-- Тело сообщения -->
        <div class="message-body">
          <div class="message-meta">
            <span class="username">{{ message.name }}</span>
            <span class="message-time">{{ message.time || 'Сейчас' }}</span>
          </div>
          <div class="message-text">
            {{ message.text }}
          </div>
        </div>
      </div>
    </div>

    <!-- Поле ввода (для демонстрации) -->
    <div class="chat-input-area">
      <input type="text" placeholder="Написать в чат..." class="chat-input" />
      <button class="send-btn">➤</button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

// Данные виджета (можно расширить временем)
const youTube_chat_widgets = ref([
  {
    id: 2,
    title: 'YouTube',
    service: 'youtube',
    messages: [
      {
        id: 3,
        name: 'Подписчик',
        text: 'Подписчик оставил благодарность за видео.Подписчик оставил благодарность за видео.Подписчик оставил благодарность за видео.Подписчик оставил благодарность за видео.Подписчик оставил благодарность за видео.Подписчик оставил благодарность за видео.',
        time: '12:34'
      },
      {
        id: 4,
        name: 'Пользователь',
        text: 'Появился новый комментарий из прямой трансляции.',
        time: '12:36'
      },
      {
        id: 5,
        name: 'Подписчик',
        text: 'Отличный контент, спасибо!',
        time: '12:38'
      },
      {
        id: 6,
        name: 'Зритель',
        text: 'Когда следующая трансляция?',
        time: '12:41'
      }
    ]
  },
])

// Ссылка на контейнер для автоматического скролла
const messagesContainer = ref(null)

// Функция для получения инициалов (для аватарки)
const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Проверка, что текущее сообщение от того же пользователя, что и предыдущее
const sameUser = (index) => {
  const messages = youTube_chat_widgets.value[0]?.messages || []
  if (index === 0) return false
  return messages[index].name === messages[index - 1].name
}

// Автоматическая прокрутка вниз при добавлении новых сообщений
watch(
  () => youTube_chat_widgets.value[0]?.messages.length,
  () => {
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  },
  { flush: 'post' }
)
</script>

<style scoped src="../../assets/widget_youtube_chat.css"></style>