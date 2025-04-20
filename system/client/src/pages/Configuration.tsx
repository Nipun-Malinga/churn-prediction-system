import DagInfoTable from '@/components/DagInfoTable';
import MainContainer from '@/components/MainContainer';
import TrainedModelTable from '@/components/TrainedModelTable';
import { GridItem, SimpleGrid } from '@chakra-ui/react';

const Configuration = () => {
  return (
    <>
      <SimpleGrid columns={10} width={'100%'} gap={'1rem'}>
        <GridItem colSpan={10} borderRadius={'1rem'} overflow={'hidden'}>
          <MainContainer title='Dag Information' modeSelectorVisible={false}>
            <DagInfoTable />
          </MainContainer>
        </GridItem>
        <GridItem colSpan={10}>
          <MainContainer title='New Trained Models' modeSelectorVisible={false}>
            <TrainedModelTable />
          </MainContainer>
        </GridItem>
      </SimpleGrid>
    </>
  );
};

export default Configuration;
