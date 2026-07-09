
import YoutubeChat from './youtube_chat.vue'
import VkliveChat from './vklive_chat.vue'
import TwitchChat from './twitch_chat.vue'

export const AllWidgetsPlugin = {
  install(app) {
    app.component('YoutubeChat', YoutubeChat)
    app.component('VkliveChat', VkliveChat)
    app.component('TwitchChat', TwitchChat)
  }
}

export { YoutubeChat, VkliveChat, TwitchChat }