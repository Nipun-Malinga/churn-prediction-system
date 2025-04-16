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
            value={data.data?.accuracy.toFixed(3) * 100}
            title='Accuracy'
          ></PerformanceCard>
          <PerformanceCard
            value={data.data?.precision.toFixed(3) * 100}
            title='Precision'
          ></PerformanceCard>
          <PerformanceCard
            value={data.data?.recall.toFixed(3) * 100}
            title='Recall'
          ></PerformanceCard>
          <PerformanceCard
            value={data.data?.f1_score.toFixed(3) * 100}
            title='F1 Score'
          ></PerformanceCard>
        </CardContainer>
      )}
    </VStack>
  );
};

export default Model;
