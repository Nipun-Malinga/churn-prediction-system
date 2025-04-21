import DagInfoTable from '@/components/DagInfoTable';
import MainContainer from '@/components/MainContainer';
import TrainedModelCard from '@/components/TrainedModelCard';
import useSetProductionModel from '@/hooks/useSetProductionModel';
import useTrainedModels from '@/hooks/useTrainedModels';
import { GridItem, SimpleGrid } from '@chakra-ui/react';

const Configuration = () => {
  const { data, refetch } = useTrainedModels();
  const { mutate } = useSetProductionModel();

  const handleSubmit = (batch_id: string) => {
    mutate(
      {
        batch_id: batch_id,
      },
      {
        onSuccess: () => {
          refetch();
        },
      }
    );
  };

  return (
    <>
      <SimpleGrid columns={2} width={'100%'} gap={'1rem'}>
        <GridItem colSpan={2} borderRadius={'1rem'} overflow={'hidden'}>
          <MainContainer title='Dag Information' modeSelectorVisible={false}>
            <DagInfoTable />
          </MainContainer>
        </GridItem>
        <GridItem colSpan={{ base: 2, md: 1 }}>
          {data?.data && (
            <MainContainer title='New Trained Model' modeSelectorVisible={false}>
              <TrainedModelCard
                trainedModel={data?.data}
                onApprove={(batch_id) => handleSubmit(batch_id)}
              />
            </MainContainer>
          )}
        </GridItem>
      </SimpleGrid>
    </>
  );
};

export default Configuration;
