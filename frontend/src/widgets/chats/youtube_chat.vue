<script setup>
import { ref } from 'vue'


const youTube_chat_widgets = ref([
    {
    id: 2,
    title: 'YouTube',
    service: 'youtube',
    messages: [
      { id: 3, name: 'Подписчик', text: 'Подписчик оставил благодарность за видео.' },
      { id: 4, name: 'Пользователь', text: 'Появился новый комментарий из прямой трансляции.' }
    ]
  },
])

</script>

<template>
  <div class="chat-body">
    <div v-for="widget in youTube_chat_widgets" :key="widget.id" class="message-row">
      <div v-for="message in widget.messages" class="name_viewer">
        <span class="message-source">{{ message.name }}</span>
        <p>{{ message.text }}</p>
      </div>
    </div>
  </div>

  
  <!-- <div class="chat-body">
                <div v-for="message in widget.messages" :key="message.id" class="message-row">
                  <span class="message-source">{{ mergedView ? message.source : widget.title }}</span>
                  <p>{{ message.text }}</p>
                </div>
              </div> -->
</template>

<style scoped src="../../assets/app-dashboard.css"></style>