import { Box, Heading } from '@chakra-ui/react';
import { ReactNode } from 'react';

interface props {
  title: string;
  children: ReactNode;
}

const PageContainer = ({ title, children }: props) => {
  return (
    <Box width='100%'>
      <Heading fontSize='1.75rem' mb='1.5rem'>
        {title}
      </Heading>
      {children}
    </Box>
  );
};

export default PageContainer;
