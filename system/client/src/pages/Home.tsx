import CardContainer from '@/components/CardContainer';
import ChartContainer from '@/components/ChartContainer';
import DetailCard from '@/components/DetailCard';
import PerformanceChart from '@/components/PerformanceChart';
import SystemOption from '@/components/SystemOption';
import SystemOptionContainer from '@/components/SystemOptionContainer';
import { useBasicModelInfo } from '@/hooks/useModelInfo';
import usePerformanceHistory from '@/hooks/usePerformanceHistory';
import useSelectedModeStore from '@/store/useSelectedModeStore';
import { Box, Text, VStack } from '@chakra-ui/react';
import { IoDownloadOutline } from 'react-icons/io5';
import { TbRefresh } from 'react-icons/tb';

// TODO: Build a separate hook to fetch base model information
const Home = () => {
  const { selectedMode } = useSelectedModeStore();

  const { data: basicModelData } = useBasicModelInfo();
  const { data: performanceHistoryData } = usePerformanceHistory(4, selectedMode);

  return (
    <VStack alignItems='flex-start' padding={5} rowGap={5}>
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
      <ChartContainer>
        {performanceHistoryData?.data && (
          <PerformanceChart performanceHistory={performanceHistoryData?.data} />
        )}
      </ChartContainer>
    </VStack>
  );
};

export default Home;
