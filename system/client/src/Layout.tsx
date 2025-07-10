import Sidebar from '@/components/Sidebar';
import {
  Box,
  Grid,
  GridItem,
  Show,
  useBreakpointValue,
  VStack,
} from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';
import NotificationBar from './components/NotificationBar';

const Layout = () => {
  const isDesktop = useBreakpointValue({ base: false, lg: true });

  return (
    <Box width='100%' position={'relative'}>
      <Grid
        templateAreas={{
          base: `"main"`,
          lg: `"aside main"`,
        }}
        templateColumns={{
          base: '1fr',
          lg: '250px 1fr',
        }}
        height={'100vh'}
      >
        <Show when={isDesktop}>
          <GridItem area={'aside'}>
            <Sidebar />
          </GridItem>
        </Show>
        <GridItem area={'main'} background='#F5F6FA' position={'relative'}>
          {/* <NavBar /> */}

          <Box
            animation={'fade-out, scale-out'}
            width='50%'
            zIndex={100}
            position='absolute'
            right={0}
          >
            <NotificationBar />
          </Box>
          <VStack alignItems='flex-start' padding={5} rowGap={5}>
            <Outlet />
          </VStack>
        </GridItem>
      </Grid>
    </Box>
  );
};

export default Layout;
