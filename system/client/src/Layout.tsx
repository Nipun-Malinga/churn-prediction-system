import Sidebar from '@/components/Sidebar';
import { Grid, GridItem, Show, useBreakpointValue, VStack } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';
import NavBar from './components/Navbar';

const Layout = () => {
  const isDesktop = useBreakpointValue({ base: false, lg: true });

  return (
    <>
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
        <GridItem area={'main'} background='#F5F6FA'>
          {/* <NavBar /> */}
          <VStack alignItems='flex-start' padding={5} rowGap={5}>
            <Outlet />
          </VStack>
        </GridItem>
      </Grid>
    </>
  );
};

export default Layout;
