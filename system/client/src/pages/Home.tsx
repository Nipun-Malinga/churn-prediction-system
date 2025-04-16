import CardContainer from '@/components/CardContainer';
import ChartContainer from '@/components/ChartContainer';
import DetailCard from '@/components/DetailCard';
import { Model } from '@/models/ModelDetails';
import { Text, VStack } from '@chakra-ui/react';

const Home = () => {
  /* TODO: Fetch Model Info From the Server*/
  const modelInfo: Model[] = [
    { id: 1, name: 'VOTING CLASSIFIER', base_model: true },
    { id: 2, name: 'XGBOOST', base_model: false },
    { id: 3, name: 'LIGHTGBM', base_model: false },
    { id: 4, name: 'RANDOM FOREST', base_model: false },
  ];

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
        {modelInfo.map((info, id) => (
          <DetailCard key={id} children={info} />
        ))}
      </CardContainer>
      <ChartContainer isBaseModel={true} />
    </VStack>
  );
};

export default Home;
