import CardContainer from '@/components/CardContainer';
import DetailCard from '@/components/DetailCard';
import MainContainer from '@/components/MainContainer';
import PerformanceChart from '@/components/PerformanceChart';
import PerformanceDriftChart from '@/components/PerformanceDriftChart';
import SystemOption from '@/components/SystemOption';
import SystemOptionContainer from '@/components/SystemOptionContainer';
import { useBasicModelInfo } from '@/hooks/useModelInfo';
import usePerformanceDriftHistory from '@/hooks/usePerformanceDriftHistory';
import usePerformanceHistory from '@/hooks/usePerformanceHistory';
import useSelectedModeStore from '@/store/useSelectedModeStore';
import { Box, SimpleGrid, Text, VStack } from '@chakra-ui/react';
import { IoDownloadOutline } from 'react-icons/io5';
import { TbRefresh } from 'react-icons/tb';

// TODO: Build a separate hook to fetch base model information
const Home = () => {
  const { selectedMode } = useSelectedModeStore();

  const { data: basicModelData } = useBasicModelInfo();
  const { data: performanceHistoryData } = usePerformanceHistory(4, selectedMode);
  const { data: performanceDriftHistoryData } = usePerformanceDriftHistory();

  return (
    <>
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
        {basicModelData &&
          basicModelData.data.map((model, id) => <DetailCard key={id} model={model} />)}
      </CardContainer>
      <Box
        alignSelf={{
          base: 'center',
          md: 'flex-end',
        }}
      >
        <SystemOptionContainer>
          {/* Implement button operations */}
          <SystemOption
            icon={TbRefresh}
            description='System Retrain'
            onClick={() => console.log('Hello')}
          ></SystemOption>
          <SystemOption
            icon={IoDownloadOutline}
            description='Download Model'
            onClick={() => console.log('Hello')}
          ></SystemOption>
        </SystemOptionContainer>
      </Box>

      <SimpleGrid
        columns={{
          base: 1,
          md: 2,
        }}
        gap={'1rem'}
        width={'100%'}
      >
        <MainContainer title='Performance Drift History' modeSelectorVisible={false}>
          {performanceDriftHistoryData?.data && (
            <PerformanceDriftChart performanceDriftHistory={performanceDriftHistoryData?.data} />
          )}
        </MainContainer>
        <MainContainer modeSelectorVisible={true}>
          {performanceHistoryData?.data && (
            <PerformanceChart performanceHistory={performanceHistoryData?.data} />
          )}
        </MainContainer>
      </SimpleGrid>
    </>
  );
};

export default Home;
