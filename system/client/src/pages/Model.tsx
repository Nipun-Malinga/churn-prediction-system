import ConfusionMatrix from '@/components/ConfusionMatrix';
import MainContainer from '@/components/MainContainer';
import PerformanceCard from '@/components/PerformanceCard';
import PerformanceChart from '@/components/PerformanceChart';
import PerformanceDifferenceChart from '@/components/PerformanceDifferenceChart';
import useBaseModelInfo from '@/hooks/useBaseModelInfo';
import { useAdvancedModelInfo } from '@/hooks/useModelInfo';
import usePerformanceHistory from '@/hooks/usePerformanceHistory';
import useSelectedModeStore from '@/store/useSelectedModeStore';
import { GridItem, SimpleGrid, Text } from '@chakra-ui/react';
import { useParams } from 'react-router-dom';

const Model = () => {
  const params = useParams();
  const modelId = Number(params?.id!);
  const modelName = params?.model!;

  const { selectedMode } = useSelectedModeStore();

  const { data } = useAdvancedModelInfo(modelId);
  const { data: baseModelInfo } = useBaseModelInfo();
  const { data: performanceHistoryData } = usePerformanceHistory(modelId, selectedMode);

  return (
    <>
      <Text
        fontWeight={'bold'}
        fontSize={{
          lg: '1.5rem',
        }}
      >
        {modelName}
      </Text>
      <SimpleGrid
        width={'100%'}
        columns={{
          base: 1,
          md: 3,
        }}
        gap={'1rem'}
      >
        <GridItem width={'100%'}>
          <ConfusionMatrix
            tp={data?.data.TP ? data?.data.TP : 0}
            tn={data?.data.TN ? data?.data.TN : 0}
            fp={data?.data.FP ? data?.data.FP : 0}
            fn={data?.data.FN ? data?.data.FN : 0}
          />
        </GridItem>
        <GridItem colSpan={{ md: 2 }} width={'100%'}>
          <MainContainer modeSelectorVisible={true}>
            {performanceHistoryData?.data && (
              <PerformanceChart performanceHistory={performanceHistoryData?.data} />
            )}
          </MainContainer>
        </GridItem>
      </SimpleGrid>

      <SimpleGrid
        width={'100%'}
        columns={{
          base: 1,
          md: 3,
        }}
        gap={{ md: '1rem' }}
      >
        <GridItem>
          <MainContainer title='Performance Difference' modeSelectorVisible={false}>
            {baseModelInfo?.data && data?.data && (
              <PerformanceDifferenceChart
                currentModelName={modelName}
                currentModelData={data?.data}
                baseModelData={baseModelInfo?.data}
              />
            )}
          </MainContainer>
        </GridItem>
        <GridItem colSpan={2}>
          {data && (
            <SimpleGrid columns={{ base: 1, md: 2 }} gap={'1rem'}>
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
            </SimpleGrid>
          )}
        </GridItem>
      </SimpleGrid>
    </>
  );
};

export default Model;
