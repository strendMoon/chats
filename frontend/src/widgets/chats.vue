<script setup>

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

</script>

<template>
  <div class="chats">
    <div v-for="widget in widgets" :key="widget.id" class="chat-widget">
      <h2 :class="widget.accentClass">{{ widget.title }}</h2>
      <ul>
        <li v-for="message in widget.messages" :key="message.id">{{ message.text }}</li>
      </ul>
    </div>
  </div>
</template>