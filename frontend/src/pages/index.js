import Home from './Home.vue';
import Chats from './Chats.vue';
import Alerts from './Alerts.vue';
import Statistics from './Statistics.vue';

const pageComponents = {
  home: Home,
  chats: Chats, 
  alerts: Alerts,
  stats: Statistics, 
};

const pages_config = [
  { id: 'chats', label: 'Чаты', icon: '💬', router_link: '/chats' },
  { id: 'alerts', label: 'Оповещения', icon: '🔔', router_link: '/alerts' },
  { id: 'stats', label: 'Статистика', icon: '📊', router_link: '/statistics' },
  { id: 'home', label: 'Workspace', icon: '🏠', router_link: '/' },
];

export {pageComponents, pages_config}