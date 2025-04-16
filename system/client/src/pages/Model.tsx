import ChartContainer from '@/components/ChartContainer';
import { VStack } from '@chakra-ui/react';

const Model = () => {
  return (
    <VStack alignItems='flex-start' padding={5}>
      <ChartContainer isBaseModel={false}></ChartContainer>
    </VStack>
  );
};

export default Model;
