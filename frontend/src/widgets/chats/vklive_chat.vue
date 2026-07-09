<script setup>

const widget = ref([
  {
    id: 1,
    title: 'VK Live',
    service: 'vk',
    accentClass: 'accent-vk',
    messages: [
      { id: 1, text: 'Пользователь задал вопрос о новом стриме.' },
      { id: 2, text: 'Новый комментарий пришёл из сообщества.' }
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