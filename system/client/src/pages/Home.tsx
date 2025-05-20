import CardContainer from '@/components/CardContainer';
import InfoCard from '@/components/InfoCard';
import MainContainer from '@/components/MainContainer';
import NotificationBar from '@/components/NotificationBar';
import PerformanceChart from '@/components/PerformanceChart';
import PerformanceDriftChart from '@/components/PerformanceDriftChart';
import SystemOption from '@/components/SystemOption';
import SystemOptionContainer from '@/components/SystemOptionContainer';
import useDagRun from '@/hooks/useDagRun';
import { useBasicModelInfo } from '@/hooks/useModelInfo';
import usePerformanceDriftHistory from '@/hooks/usePerformanceDriftHistory';
import usePerformanceHistory from '@/hooks/usePerformanceHistory';
import useSelectedModeStore from '@/store/useSelectedModeStore';
import { Box, SimpleGrid, Text, VisuallyHidden } from '@chakra-ui/react';
import { IoDownloadOutline } from 'react-icons/io5';
import { LuBrainCircuit } from 'react-icons/lu';
import { TbRefresh } from 'react-icons/tb';

// TODO: Build a separate hook to fetch base model information
const Home = () => {
  const { selectedMode } = useSelectedModeStore();

  const { data: basicModelData } = useBasicModelInfo();
  const { data: performanceHistoryData } = usePerformanceHistory(1, selectedMode);
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
          basicModelData.data.map((model, id) => (
            <InfoCard
              key={id}
              title={`Accuracy ${(model.accuracy * 100).toFixed(2)}%`}
              subtitle={model.name}
              icon={LuBrainCircuit}
              date={model.updated_date}
              link={`/model/${model.name}/${model.id}`}
              linkIcon={TbRefresh}
              color={model.base_model ? '#FEC53D' : '#5893FF'}
            />
          ))}
      </CardContainer>
      <Box
        alignSelf={{
          base: 'center',
          md: 'flex-end',
        }}
      >
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
