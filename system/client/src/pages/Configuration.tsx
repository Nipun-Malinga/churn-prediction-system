import DagInfoTable from '@/components/DagInfoTable';
import DriftThresholdContainer from '@/components/DriftThresholdContainer';
import MainContainer from '@/components/MainContainer';
import NotificationBar from '@/components/NotificationBar';
import SystemOption from '@/components/SystemOption';
import SystemOptionContainer from '@/components/SystemOptionContainer';
import TrainedModelCard from '@/components/TrainedModelCard';
import useDagRun from '@/hooks/useDagRun';
import useSetProductionModel from '@/hooks/useSetProductionModel';
import useTrainedModels from '@/hooks/useTrainedModels';
import {
  Box,
  Button,
  CloseButton,
  Dialog,
  GridItem,
  Portal,
  SimpleGrid,
  Text,
} from '@chakra-ui/react';
import { FaRegCircleCheck } from 'react-icons/fa6';
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
        <Dialog.Root>
          <Dialog.Trigger width='5rem' asChild>
            <Button variant={'ghost'}>
              <SystemOption icon={TbRefresh} description='System Retrain'></SystemOption>
            </Button>
          </Dialog.Trigger>
          <Portal>
            <Dialog.Backdrop />
            <Dialog.Positioner>
              <Dialog.Content>
                <Dialog.Header>
                  <Dialog.Title>System Retrain</Dialog.Title>
                </Dialog.Header>
                <Dialog.Body>
                  <Text>This action will cause system retrain. Do you want to proceed?</Text>
                </Dialog.Body>
                <Dialog.Footer>
                  <Dialog.ActionTrigger asChild>
                    <Button width='100%' onClick={() => handleModelRetrainRun()}>
                      <FaRegCircleCheck />
                    </Button>
                  </Dialog.ActionTrigger>
                </Dialog.Footer>
                <Dialog.CloseTrigger asChild>
                  <CloseButton size='sm' />
                </Dialog.CloseTrigger>
              </Dialog.Content>
            </Dialog.Positioner>
          </Portal>
        </Dialog.Root>
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
      <MainContainer title='Drift Detector Thresholds' modeSelectorVisible={false}>
        <DriftThresholdContainer />
      </MainContainer>
    </>
  );
};

export default Configuration;
