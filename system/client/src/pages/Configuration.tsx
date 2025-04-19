import DagInfoTable from '@/components/DagInfoTable';
import MainContainer from '@/components/MainContainer';
import { GridItem, SimpleGrid } from '@chakra-ui/react';

const Configuration = () => {
  return (
    <>
      <SimpleGrid columns={10} width={'100%'}>
        <GridItem colSpan={10} borderRadius={'1rem'} overflow={'hidden'}>
          <MainContainer title='Dag Information' modeSelectorVisible={false}>
            <DagInfoTable />
          </MainContainer>
        </GridItem>
      </SimpleGrid>
    </>
  );
};

export default Configuration;
