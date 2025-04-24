import { Alert } from '@chakra-ui/react';

interface Props {
  type: 'error' | 'info' | 'neutral' | 'success' | 'warning';
  notification: string;
}

const NotificationBar = ({ type, notification }: Props) => {
  return (
    <Alert.Root
      status={type}
      my='4'
      onClick={() => console.log('')}
      cursor={'pointer'}
      _hover={{
        boxShadow: 'rgba(0, 0, 0, 0.24) 0px 3px 8px;',
        transition: '0.15s ease-in-out',
      }}
    >
      <Alert.Indicator />
      <Alert.Title>{notification}</Alert.Title>
    </Alert.Root>
  );
};

export default NotificationBar;
