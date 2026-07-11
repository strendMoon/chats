<script setup>
import { YoutubeChat, VkliveChat, TwitchChat } from '@/widgets/chats/index.js'
import {ref} from 'vue'

</script>

<template>
  <div class="chat-grid">
    <YoutubeChat/>
    <VkliveChat/>
    <TwitchChat/>
  </div>
  </template>