import DagInfoTable from '@/components/DagInfoTable';
import MainContainer from '@/components/MainContainer';
import NotificationBar from '@/components/NotificationBar';
import SystemOption from '@/components/SystemOption';
import SystemOptionContainer from '@/components/SystemOptionContainer';
import TrainedModelCard from '@/components/TrainedModelCard';
import useDagRun from '@/hooks/useDagRun';
import useSetProductionModel from '@/hooks/useSetProductionModel';
import useTrainedModels from '@/hooks/useTrainedModels';
import { Box, GridItem, SimpleGrid } from '@chakra-ui/react';
import { TbRefresh } from 'react-icons/tb';

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

  const { mutate: triggerDagRun, isSuccess } = useDagRun();

  const handleModelRetrainRun = () => {
    triggerDagRun({
      dag_id: 'model_evaluating_dag',
    });
  };

  return (
    <>
      <Box width={'100%'} hidden={!isSuccess}>
        <NotificationBar notification='Model Training In Progress' type='info' />
      </Box>
      <SystemOptionContainer>
        {/* Implement button operations */}
        <SystemOption
          icon={TbRefresh}
          description='System Retrain'
          onClick={() => handleModelRetrainRun()}
        ></SystemOption>
      </SystemOptionContainer>
      <SimpleGrid columns={2} width={'100%'} gap={'1rem'}>
        <GridItem colSpan={{ base: 2, md: 2 }}>
          {data?.data && (
            <MainContainer title='New Trained Model' modeSelectorVisible={false}>
              <TrainedModelCard
                trainedModel={data?.data}
                onApprove={(batch_id) => handleSubmit(batch_id)}
              />
            </MainContainer>
          )}
        </GridItem>
        <GridItem colSpan={2} borderRadius={'1rem'} overflow={'hidden'}>
          <MainContainer title='Dag Information' modeSelectorVisible={false}>
            <DagInfoTable />
          </MainContainer>
        </GridItem>
      </SimpleGrid>
    </>
  );
};

export default Configuration;
