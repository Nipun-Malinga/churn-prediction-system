import CardContainer from '@/components/CardContainer';
import ChartContainer from '@/components/ChartContainer';
import PerformanceCard from '@/components/PerformanceCard';
import { useAdvancedModelInfo } from '@/hooks/useModelInfo';
import { VStack } from '@chakra-ui/react';
import { useParams } from 'react-router-dom';

const Model = () => {
  const params = useParams();
  const { data } = useAdvancedModelInfo(Number(params?.id!));

  return (
    <VStack alignItems='flex-start' padding={5}>
      <ChartContainer isBaseModel={false}></ChartContainer>
      {data && (
        <CardContainer>
          <PerformanceCard
            value={Number((data.data.accuracy * 100).toFixed(2))}
            title='Accuracy'
          ></PerformanceCard>
          <PerformanceCard
            value={Number((data.data?.precision * 100).toFixed(2))}
            title='Precision'
          ></PerformanceCard>
          <PerformanceCard
            value={Number((data.data?.recall * 100).toFixed(2))}
            title='Recall'
          ></PerformanceCard>
          <PerformanceCard
            value={Number((data.data?.f1_score * 100).toFixed(2))}
            title='F1 Score'
          ></PerformanceCard>
        </CardContainer>
      )}
    </VStack>
  );
};

export default Model;
