<template>
  <div class="vklive-chat-widget">
    <!-- Шапка -->
    <div class="chat-header">
      <div class="header-left">
        <span class="vk-icon">📹</span>
        <span class="platform-name">VK Live</span>
        <span class="live-badge">LIVE</span>
      </div>
      <div class="header-right">
        <span class="viewers-count">👁️ 2.1K</span>
        <button class="settings-btn" title="Настройки">⚙️</button>
      </div>
    </div>

    <!-- Сообщения -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in vkLiveChatWidgets[0]?.messages || []"
        :key="message.id || index"
        class="message-item"
        :class="{
          'same-user': index > 0 && message.name === vkLiveChatWidgets[0].messages[index - 1].name
        }"
      >
        <!-- Аватар -->
        <div v-if="!sameUser(index)" class="avatar">
          {{ getInitials(message.name) }}
        </div>
        <div v-else class="avatar-placeholder"></div>

        <!-- Тело -->
        <div class="message-body">
          <div class="message-meta">
            <span class="username">{{ message.name }}</span>
            <span class="message-time">{{ message.time || 'Сейчас' }}</span>
            <span v-if="message.isModerator" class="mod-badge">Модератор</span>
            <span v-else-if="message.isAdmin" class="admin-badge">Админ</span>
          </div>
          <div class="message-text">
            {{ message.text }}
            <span v-if="message.liked" class="like-icon">❤️</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Поле ввода -->
    <div class="chat-input-area">
      <input type="text" placeholder="Написать в чат..." class="chat-input" />
      <button class="send-btn">➤</button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

const vkLiveChatWidgets = ref([
  {
    id: 3,
    title: 'VK Live',
    service: 'vklive',
    messages: [
      {
        id: 201,
        name: 'Анна',
        text: 'Крутой концерт! Очень нравится 😊',
        time: '14:05',
        isModerator: false,
        isAdmin: false,
        liked: true,
      },
      {
        id: 202,
        name: 'Максим',
        text: 'Когда следующий эфир?',
        time: '14:07',
        isModerator: false,
        isAdmin: false,
        liked: false,
      },
      {
        id: 203,
        name: 'Екатерина',
        text: 'Супер! Подписался на канал 👍',
        time: '14:10',
        isModerator: true,
        isAdmin: false,
        liked: false,
      },
      {
        id: 204,
        name: 'Дмитрий',
        text: 'Качество видео отличное!',
        time: '14:12',
        isModerator: false,
        isAdmin: true,
        liked: false,
      },
    ]
  },
])

const messagesContainer = ref(null)

const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const sameUser = (index) => {
  const messages = vkLiveChatWidgets.value[0]?.messages || []
  if (index === 0) return false
  return messages[index].name === messages[index - 1].name
}

watch(
  () => vkLiveChatWidgets.value[0]?.messages.length,
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
<style scoped src="../../assets/widget_vklive_chat.css"></style>