<script setup>

const widget = ref([
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