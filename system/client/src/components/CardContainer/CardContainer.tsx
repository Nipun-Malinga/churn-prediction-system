import { SimpleGrid } from '@chakra-ui/react';
import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

const CardContainer = ({ children }: Props) => {
  return (
    <SimpleGrid
      columns={{
        base: 1,
        md: 2,
        xl: 4,
      }}
      gap={2}
      width={'100%'}
    >
      {children}
    </SimpleGrid>
  );
};

export default CardContainer;
