import CardContainer from '@/components/CardContainer';
import ChartContainer from '@/components/ChartContainer';
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
      <ChartContainer />
    </VStack>
  );
};

export default Home;
