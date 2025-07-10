interface Notification {
  type: 'error' | 'info' | 'neutral' | 'success' | 'warning';
  info: string;
}

export default Notification;
