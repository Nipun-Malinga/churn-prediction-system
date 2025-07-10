import Notification from '@/models/Notification';
import { create } from 'zustand';

interface NotificationState {
  notification: Notification | null;
  setNotification: (notification: Notification) => void;
  clearNotification: () => void;
}

const useNotificationStore = create<NotificationState>((set) => ({
  notification: null,
  setNotification: (data) => set({ notification: data }),
  clearNotification: () => set({ notification: null }),
}));

export default useNotificationStore;
