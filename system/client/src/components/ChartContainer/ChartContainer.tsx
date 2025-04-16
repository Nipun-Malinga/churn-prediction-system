import usePerformanceHistory from '@/hooks/usePerformanceHistory';
import { Box, HStack, NativeSelect, Text, VStack } from '@chakra-ui/react';
import { useState } from 'react';
import PerformanceChart from '../PerformanceChart';

const ChartContainer = () => {
  const [selectedChart, setSelectedChart] = useState('accuracy');

  /*
    TODO: 
      * Develop a Separate API Endpoint for Base Model 
      * Implement Loading Skeleton and Error Massage Components

  */
  const { data, isFetching, error } = usePerformanceHistory(4, selectedChart);

  console.log(data);

  return (
    <VStack
      width={'100%'}
      gap={'2.5rem'}
      background={'#ffffff'}
      borderRadius={'1rem'}
      padding={{
        base: 0,
        md: 5,
      }}
      marginY={'1rem'}
    >
      <HStack
        width={'100%'}
        justifyContent={'space-between'}
        paddingX={{
          base: 0,
          md: 5,
        }}
      >
        <Text
          fontWeight={'medium'}
          fontSize={{
            base: '',
            lg: '1.5rem',
          }}
        >
          Performance Details
        </Text>
        <NativeSelect.Root
          width={{
            base: '7.5rem',
            lg: '10rem',
          }}
        >
          <NativeSelect.Field onChange={(e) => setSelectedChart(e.target.value)}>
            <option value='accuracy'>Accuracy</option>
            <option value='precision'>Precision</option>
            <option value='recall'>Recall</option>
            <option value='f1_score'>F1 Score</option>
          </NativeSelect.Field>
          <NativeSelect.Indicator />
        </NativeSelect.Root>
      </HStack>
      {data?.data ? <PerformanceChart performanceHistory={data?.data} /> : <></>}
    </VStack>
  );
};

export default ChartContainer;
