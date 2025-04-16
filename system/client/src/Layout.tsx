import Sidebar from '@/components/Sidebar';
import { Grid, GridItem, Show, useBreakpointValue } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';

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
      >
        <Show when={isDesktop}>
          <GridItem area={'aside'}>
            <Sidebar />
          </GridItem>
        </Show>
        <GridItem area={'main'} background='#F5F6FA'>
          <Outlet />
        </GridItem>
      </Grid>
    </>
  );
};

export default Layout;
