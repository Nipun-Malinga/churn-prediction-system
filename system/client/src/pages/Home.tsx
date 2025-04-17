import CardContainer from '@/components/CardContainer';
import ChartContainer from '@/components/ChartContainer';
import DetailCard from '@/components/DetailCard';
import SystemOption from '@/components/SystemOption';
import SystemOptionContainer from '@/components/SystemOptionContainer';
import { useBasicModelInfo } from '@/hooks/useModelInfo';
import { Box, Text, VStack } from '@chakra-ui/react';
import { IoDownloadOutline } from 'react-icons/io5';
import { TbRefresh } from 'react-icons/tb';

const Home = () => {
  const { data, isLoading, error } = useBasicModelInfo();

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
        {data && data.data.map((model, id) => <DetailCard key={id} model={model} />)}
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
      <ChartContainer isBaseModel={true} />
    </VStack>
  );
};

export default Home;
