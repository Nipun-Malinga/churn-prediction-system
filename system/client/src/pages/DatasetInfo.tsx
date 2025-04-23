import DataImbalanceChart from '@/components/DataImbalanceChart';
import InfoCard from '@/components/InfoCard';
import MainContainer from '@/components/MainContainer';
import useBasicDatasetInfo from '@/hooks/useBasicDatasetInfo';
import { GridItem, SimpleGrid, Text } from '@chakra-ui/react';
import { PiShapesBold } from 'react-icons/pi';

const DatasetInfo = () => {
  const { data } = useBasicDatasetInfo();

  return (
    <>
      <Text
        fontSize={{
          base: '1rem',
          lg: '1.5rem',
        }}
        fontWeight={'medium'}
      >
        Dataset
      </Text>
      <SimpleGrid columns={1} width={'100%'} gap={'1rem'}>
        <GridItem>
          <SimpleGrid gap={'1rem'}>
            <InfoCard
              title={`Rows: ${data?.data.shape.total_rows} & Features: ${data?.data.shape.total_features}`}
              subtitle='Shape'
              icon={PiShapesBold}
            />
          </SimpleGrid>
        </GridItem>

        <GridItem>
          <MainContainer title='Class Imbalance' modeSelectorVisible={false}>
            {data?.data.class_imbalance && (
              <DataImbalanceChart classImbalance={data?.data.class_imbalance} />
            )}
          </MainContainer>
        </GridItem>
      </SimpleGrid>
    </>
  );
};

export default DatasetInfo;
