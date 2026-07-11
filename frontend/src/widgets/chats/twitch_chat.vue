<template>
  <div class="twitch-chat-widget">
    <!-- Шапка в стиле Twitch -->
    <div class="chat-header">
      <div class="header-left">
        <span class="twitch-icon">🟣</span>
        <span class="platform-name">Twitch</span>
        <span class="live-badge">LIVE</span>
      </div>
      <div class="header-right">
        <span class="viewers-count">👁️ 3.4K</span>
        <button class="settings-btn" title="Настройки">⚙️</button>
      </div>
    </div>

    <!-- Область сообщений -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in twitchChatWidgets[0]?.messages || []"
        :key="message.id || index"
        class="message-item"
        :class="{
          'same-user': index > 0 && message.name === twitchChatWidgets[0].messages[index - 1].name
        }"
      >
        <!-- Аватарка (только если новое сообщение от другого пользователя) -->
        <div v-if="!sameUser(index)" class="avatar">
          {{ getInitials(message.name) }}
        </div>
        <div v-else class="avatar-placeholder"></div>

        <!-- Тело сообщения -->
        <div class="message-body">
          <div class="message-meta">
            <span class="username">{{ message.name }}</span>
            <span class="message-time">{{ message.time || 'Сейчас' }}</span>
            <!-- Бейдж подписчика (для разнообразия) -->
            <span v-if="message.isSubscriber" class="sub-badge">SUB</span>
          </div>
          <div class="message-text">
            {{ message.text }}
          </div>
        </div>
      </div>
    </div>

    <!-- Поле ввода (декоративное) -->
    <div class="chat-input-area">
      <input type="text" placeholder="Написать в чат..." class="chat-input" />
      <button class="send-btn">➤</button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

// Данные для Twitch-чата (можно расширить)
const twitchChatWidgets = ref([
  {
    id: 1,
    title: 'Twitch',
    service: 'twitch',
    messages: [
      {
        id: 101,
        name: 'Геймер_Pro',
        text: 'Привет, стример! Отличный стрим!',
        time: '15:22',
        isSubscriber: true,
      },
      {
        id: 102,
        name: 'Зритель_42',
        text: 'Классный мув!',
        time: '15:24',
        isSubscriber: false,
      },
      {
        id: 103,
        name: 'Геймер_Pro',
        text: 'Когда следующий стрим?',
        time: '15:27',
        isSubscriber: true,
      },
      {
        id: 104,
        name: 'Новичок',
        text: 'Какой у тебя ранг в CS?',
        time: '15:30',
        isSubscriber: false,
      },
    ]
  },
])

const messagesContainer = ref(null)

// Инициалы для аватарки
const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Проверка, что это тот же пользователь, что и предыдущее сообщение
const sameUser = (index) => {
  const messages = twitchChatWidgets.value[0]?.messages || []
  if (index === 0) return false
  return messages[index].name === messages[index - 1].name
}

// Автоскролл при добавлении новых сообщений
watch(
  () => twitchChatWidgets.value[0]?.messages.length,
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

<style scoped src="../../assets/widget_twitch_chat.css"></style>