import useNotificationStore from '@/store/useNotificationStore';
import { useEffect } from 'react';
import { Toaster, toaster } from '../ui/toaster';

const NotificationBar = () => {
  const { notification, clearNotification } = useNotificationStore();

  useEffect(() => {
    notification &&
      toaster.create({
        description: notification.info,
        type: notification.type,
        closable: true,
      });
    clearNotification();
  }, [notification]);

  return <Toaster />;
};

export default NotificationBar;
