import CardContainer from '@/components/CardContainer';
import ChartContainer from '@/components/ChartContainer';
import DetailCard from '@/components/DetailCard';
import { useBasicModelInfo } from '@/hooks/useModelInfo';
import { Text, VStack } from '@chakra-ui/react';

const Home = () => {
  /* TODO: Fetch Model Info From the Server*/

  const { data, isLoading, error } = useBasicModelInfo();

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
      <CardContainer>
        {data && data.data.map((model, id) => <DetailCard key={id} model={model} />)}
      </CardContainer>
      <ChartContainer isBaseModel={true} />
    </VStack>
  );
};

export default Home;
