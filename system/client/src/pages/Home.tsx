import CardContainer from '@/components/CardContainer';
import { Text, VStack } from '@chakra-ui/react';

const Home = () => {
  return (
    <VStack alignItems='flex-start' padding={5}>
      <Text
        fontSize={{
          base: '1rem',
          lg: '1.5rem',
        }}
        fontWeight={'medium'}
      >
        Dashboard
      </Text>
      <CardContainer />
    </VStack>
  );
};

export default Home;
