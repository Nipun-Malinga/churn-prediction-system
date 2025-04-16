import usePerformanceHistory from '@/hooks/usePerformanceHistory';
import { HStack, NativeSelect, Text, VStack } from '@chakra-ui/react';
import { useState } from 'react';
import PerformanceChart from '../PerformanceChart';
import { useParams } from 'react-router-dom';

interface Props {
  isBaseModel: boolean;
}

const ChartContainer = ({ isBaseModel }: Props) => {
  const [selectedChart, setSelectedChart] = useState('accuracy');
  const params = useParams();

  /*
    TODO: 
      * Develop a Separate API Endpoint for Base Model 
      * Implement Loading Skeleton and Error Massage Components

  */

  const { data, isFetching, error } = isBaseModel
    ? usePerformanceHistory(4, selectedChart)
    : usePerformanceHistory(Number(params?.id!), selectedChart);

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
          Performance History
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
