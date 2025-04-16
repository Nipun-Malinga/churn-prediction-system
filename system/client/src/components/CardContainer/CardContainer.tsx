import { SimpleGrid } from '@chakra-ui/react';
import DetailCard from '../DetailCard';
import { Model } from '@/models';

const modelInfo: Model[] = [
  { id: 1, name: 'VOTING CLASSIFIER', base_model: true },
  { id: 2, name: 'XGBOOST', base_model: false },
  { id: 3, name: 'LIGHTGBM', base_model: false },
  { id: 4, name: 'RANDOM FOREST', base_model: false },
];

const CardContainer = () => {
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
      {modelInfo.map((info, id) => (
        <DetailCard key={id} children={info} />
      ))}
    </SimpleGrid>
  );
};

export default CardContainer;
