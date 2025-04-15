import { Box } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <>
      <Box padding={5}>
        <Outlet />
      </Box>
    </>
  );
};

export default Layout;
