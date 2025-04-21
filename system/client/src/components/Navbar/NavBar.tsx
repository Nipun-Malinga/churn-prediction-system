import useTrainedModels from '@/hooks/useTrainedModels';
import useTrainedModelStore from '@/store/useTrainedModelStore';
import { Button, HStack, Popover, Portal } from '@chakra-ui/react';
import { useEffect } from 'react';
import { FaRegBell } from 'react-icons/fa6';
import { IoMdMenu } from 'react-icons/io';
import NotificationBar from '../NotificationButton';


const NavBar = () => {
  const { data } = useTrainedModels();
  const { setTrainedModel } = useTrainedModelStore();

  useEffect(() => {
    data?.data && setTrainedModel(data.data);
  }, [data?.data]);

  return (
    <HStack
      justifyContent={'space-between'}
      width={'100%'}
      background={'#fff'}
      paddingX={5}
      paddingY={2}
    >
      {/*TODO:Build button to toggle sidebar view*/}
      <IoMdMenu />
      <Popover.Root>
        <Popover.Trigger asChild>
          <Button size='sm' variant='outline'>
            <FaRegBell />
          </Button>
        </Popover.Trigger>
        <Portal>
          <Popover.Positioner>
            <Popover.Content>
              <Popover.Arrow />
              <Popover.Body>
                <Popover.Title fontWeight='medium'>Notifications</Popover.Title>
                {data?.data && (
                  <NotificationBar type='warning' notification='New Trained Model Available' />
                )}
              </Popover.Body>
            </Popover.Content>
          </Popover.Positioner>
        </Portal>
      </Popover.Root>
    </HStack>
  );
};

export default NavBar;
