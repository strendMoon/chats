<template>
  <div class="home-card">
    <div class="hero">
      <h1>WithChats</h1>
      <p>Единая авторизация и подключение Google, YouTube, Twitch и VK Live к одному профилю.</p>
    </div>

    <div v-if="loading" class="state">Загрузка...</div>

    <div v-else-if="user" class="user-panel">
      <div class="user-info">
        <img v-if="user.picture" :src="user.picture" alt="avatar" class="avatar" />
        <div>
          <h2>{{ user.name || 'Пользователь' }}</h2>
          <p>{{ user.email }}</p>
        </div>
      </div>
      <button class="btn btn-secondary" @click="logout">Выйти</button>
    </div>

    <div v-else class="auth-box">
      <button class="btn btn-primary" @click="loginWithGoogle">Авторизоваться через Google</button>
    </div>

    <div v-if="user" class="provider-grid">
      <button class="provider-btn google" @click="loginWithGoogle">Google</button>
      <button class="provider-btn youtube" @click="loginWithYoutube">YouTube</button>
      <button class="provider-btn twitch" @click="loginWithTwitch">Twitch</button>
      <button class="provider-btn vk" @click="loginWithVk">VK Live</button>
    </div>

    <div v-if="user" class="providers-status">
      <div>Google: {{ user.providers?.google ? 'подключено' : 'не подключено' }}</div>
      <div>YouTube: {{ user.providers?.youtube ? 'подключено' : 'не подключено' }}</div>
      <div>Twitch: {{ user.providers?.twitch ? 'подключено' : 'не подключено' }}</div>
      <div>VK: {{ user.providers?.vk ? 'подключено' : 'не подключено' }}</div>
    </div>

    <div v-if="statusMessage" class="status-message">{{ statusMessage }}</div>

    <div v-if="user" class="info-grid">
      <section class="panel">
        <h3>Профиль</h3>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Имя:</strong> {{ user.name || '—' }}</p>
        <p><strong>Google ID:</strong> {{ user.google_id || '—' }}</p>
      </section>

      <section class="panel">
        <h3>YouTube канал</h3>
        <div v-if="user.youtube?.connected && user.youtube?.channel">
          <p><strong>Название:</strong> {{ user.youtube.channel.snippet?.title || '—' }}</p>
          <p><strong>Подписчики:</strong> {{ user.youtube.channel.statistics?.subscriberCount || '—' }}</p>
          <p><strong>Просмотры:</strong> {{ user.youtube.channel.statistics?.viewCount || '—' }}</p>
          <p><strong>Видео:</strong> {{ user.youtube.channel.statistics?.videoCount || '—' }}</p>
        </div>
        <div v-else-if="user.youtube?.connected">
          <p>Канал ещё не доступен или токен не дал прав на чтение.</p>
        </div>
        <div v-else>
          <p>YouTube не подключён.</p>
        </div>
      </section>

      <section class="panel">
        <h3>Текущая трансляция</h3>
        <div v-if="user.youtube?.stream">
          <p class="live-pill" :class="{ live: user.youtube.stream.status?.lifeCycleStatus === 'live', offline: user.youtube.stream.status?.lifeCycleStatus !== 'live' }">
            {{ user.youtube.stream.status?.lifeCycleStatus === 'live' ? 'В прямом эфире' : 'Оффлайн' }}
          </p>
          <p><strong>Заголовок:</strong> {{ user.youtube.stream.snippet?.title || '—' }}</p>
          <p><strong>Статус:</strong> {{ user.youtube.stream.status?.lifeCycleStatus || '—' }}</p>
          <p><strong>Live Chat ID:</strong> {{ user.youtube.stream.contentDetails?.liveChatId || '—' }}</p>
          <p><strong>Начало:</strong> {{ user.youtube.stream.snippet?.publishedAt || '—' }}</p>
          <p><strong>Конфиденциальность:</strong> {{ user.youtube.stream.status?.privacyStatus || '—' }}</p>
        </div>
        <div v-else>
          <p>Активная трансляция не найдена.</p>
        </div>
      </section>

      <section class="panel">
        <h3>Чат прямой трансляции</h3>
        <div v-if="user.youtube?.live_chat?.messages?.length">
          <ul class="chat-list">
            <li v-for="(message, index) in user.youtube.live_chat.messages.slice(0, 8)" :key="index">
              <strong>{{ message.authorDetails?.displayName || 'Аноним' }}:</strong>
              {{ message.snippet?.displayMessage || '—' }}
            </li>
          </ul>
        </div>
        <div v-else>
          <p>{{ user.youtube?.live_chat?.reason || 'Сообщения чата пока отсутствуют.' }}</p>
        </div>
        <p v-if="user.youtube?.error" class="warning">{{ user.youtube.error }}</p>
        <a v-if="user.youtube?.live_chat_url" :href="user.youtube.live_chat_url" target="_blank" rel="noopener" class="chat-link">
          Открыть чат в YouTube Studio
        </a>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      user: null,
      statusMessage: '',
      pollingTimer: null,
    }
  },
  mounted() {
    this.fetchUser()
    this.pollingTimer = setInterval(() => this.fetchUser(), 15000)
    this.$watch('$route.query', () => this.fetchUser(), { deep: true })
  },
  beforeUnmount() {
    if (this.pollingTimer) {
      clearInterval(this.pollingTimer)
    }
  },
  methods: {
    async fetchUser() {
      try {
        const response = await fetch('http://localhost:8000/auth/me', {
          credentials: 'include',
        })
        if (!response.ok) {
          this.user = null
          return
        }
        const data = await response.json()
        this.user = data.user || null
        this.statusMessage = this.getStatusMessage()
      } catch (error) {
        this.user = null
      } finally {
        this.loading = false
      }
    },
    loginWithGoogle() {
      window.location.href = 'http://localhost:8000/auth/google/url'
    },
    loginWithYoutube() {
      window.location.href = 'http://localhost:8000/auth/google/youtube/url'
    },
    loginWithTwitch() {
      window.location.href = 'http://localhost:8000/auth/twitch/url'
    },
    loginWithVk() {
      window.location.href = 'http://localhost:8000/auth/vk/url'
    },
    getStatusMessage() {
      const provider = this.$route?.query?.provider
      if (!provider) {
        return ''
      }

      const label = {
        google: 'Google',
        youtube: 'YouTube',
        twitch: 'Twitch',
        vk: 'VK Live',
      }[provider] || provider

      if (this.$route?.query?.auth_error) {
        return `Ошибка подключения ${label}: ${this.$route.query.auth_error}`
      }

      return `Подключено: ${label}`
    },
    async logout() {
      await fetch('http://localhost:8000/auth/logout', {
        method: 'POST',
        credentials: 'include',
      })
      this.user = null
      this.statusMessage = ''
    },
  },
}
</script>

<style scoped>
.home-card {
  max-width: 920px;
  margin: 3rem auto;
  padding: 2rem;
  border-radius: 24px;
  background: linear-gradient(135deg, #ffffff, #f5f8ff);
  box-shadow: 0 16px 50px rgba(0, 0, 0, 0.08);
}
.hero { margin-bottom: 1.5rem; }
.hero h1 { margin-bottom: 0.3rem; }
.user-panel, .auth-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border-radius: 16px;
  background: #f8faff;
}
.user-info { display: flex; align-items: center; gap: 1rem; }
.avatar { width: 64px; height: 64px; border-radius: 50%; object-fit: cover; }
.provider-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-top: 1rem; }
.provider-btn { border: none; border-radius: 999px; padding: 0.8rem 1rem; color: white; font-weight: 600; cursor: pointer; }
.provider-btn.google { background: #4285f4; }
.provider-btn.youtube { background: #ff0000; }
.provider-btn.twitch { background: #9146ff; }
.provider-btn.vk { background: #0077ff; }
.providers-status { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin-top: 1rem; color: #455a64; }
.status-message { margin-top: 0.75rem; padding: 0.75rem 1rem; border-radius: 12px; background: #e8f5e9; color: #2e7d32; font-weight: 600; }
.info-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin-top: 1rem; }
.panel { padding: 1rem; border-radius: 16px; background: #f8faff; }
.panel h3 { margin-top: 0; margin-bottom: 0.75rem; }
.live-pill { display: inline-block; margin-bottom: 0.75rem; padding: 0.35rem 0.7rem; border-radius: 999px; font-weight: 700; }
.live-pill.live { background: #e8f5e9; color: #2e7d32; }
.live-pill.offline { background: #eceff5; color: #546e7a; }
.chat-list { padding-left: 1rem; display: grid; gap: 0.5rem; }
.chat-link { display: inline-block; margin-top: 0.75rem; color: #ff0000; font-weight: 600; text-decoration: none; }
.warning { color: #c62828; font-size: 0.95rem; }
.btn { border: none; border-radius: 999px; padding: 0.8rem 1.2rem; cursor: pointer; font-weight: 600; }
.btn-primary { background: #4285f4; color: white; }
.btn-secondary { background: #eceff5; color: #263238; }
</style>