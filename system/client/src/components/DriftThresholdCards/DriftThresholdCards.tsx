import { HStack } from '@chakra-ui/react';
import CardContainer from '../CardContainer';
import useDriftThresholds from '@/hooks/useDriftThresholds';
import MetricCard from '../MetricCard';
import useTriggerFetchThresholdsStore from '@/store/useTriggerFetchThresholdsStore';
import { useEffect } from 'react';

const DriftThresholdCards = () => {
  const { data, refetch } = useDriftThresholds();

  const { trigger } = useTriggerFetchThresholdsStore();

  useEffect(() => {
    refetch();
  }, [trigger]);

  const fetchedData = data?.data;
  if (!fetchedData) return null;

  return (
    <HStack width={{ base: '100%', md: 'auto' }}>
      <CardContainer>
        <MetricCard label='Accuracy' value={fetchedData.accuracy} />
        <MetricCard label='Precision' value={fetchedData.precision} />
        <MetricCard label='Recall' value={fetchedData.recall} />
        <MetricCard label='F1 Score' value={fetchedData.f1_score} />
      </CardContainer>
    </HStack>
  );
};

export default DriftThresholdCards;
