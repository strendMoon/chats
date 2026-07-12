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
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      user: null,
      statusMessage: '',
    }
  },
  mounted() {
    this.fetchUser()
    this.$watch('$route.query', () => this.fetchUser(), { deep: true })
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
.btn { border: none; border-radius: 999px; padding: 0.8rem 1.2rem; cursor: pointer; font-weight: 600; }
.btn-primary { background: #4285f4; color: white; }
.btn-secondary { background: #eceff5; color: #263238; }
</style>