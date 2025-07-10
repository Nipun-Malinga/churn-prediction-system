import DagInfoTable from '@/components/DagInfoTable';
import DriftThresholdContainer from '@/components/DriftThresholdContainer';
import MainContainer from '@/components/MainContainer';
import PageContainer from '@/components/PageContainer';
import SystemOption from '@/components/SystemOption';
import SystemOptionContainer from '@/components/SystemOptionContainer';
import TrainedModelCard from '@/components/TrainedModelCard';
import useDagRun from '@/hooks/useDagRun';
import useSetProductionModel from '@/hooks/useSetProductionModel';
import useTrainedModels from '@/hooks/useTrainedModels';
import useNotificationStore from '@/store/useNotificationStore';
import {
  Button,
  CloseButton,
  Dialog,
  GridItem,
  Portal,
  SimpleGrid,
  Text,
  VStack,
} from '@chakra-ui/react';
import { useEffect } from 'react';
import { FaRegCircleCheck } from 'react-icons/fa6';
import { TbRefresh } from 'react-icons/tb';

const Configuration = () => {
  const { data, refetch } = useTrainedModels();
  const { mutate } = useSetProductionModel();
  const { mutate: triggerDagRun, isError, isSuccess } = useDagRun();
  const { setNotification } = useNotificationStore();

  useEffect(() => {
    isSuccess &&
      setNotification({ info: 'System Training In Progress', type: 'success' });
    isError &&
      setNotification({
        info: 'Failed to trigger system retrain',
        type: 'error',
      });
  }, [isSuccess, isError]);

  const handleModelRetrainRun = () => {
    triggerDagRun({
      dag_id: 'model_evaluating_dag',
    });
  };

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
    <PageContainer title='Configuration'>
      <SystemOptionContainer>
        <Dialog.Root>
          <Dialog.Trigger width='5rem'>
            <SystemOption icon={TbRefresh} description='System Retrain' />
          </Dialog.Trigger>
          <Portal>
            <Dialog.Backdrop />
            <Dialog.Positioner>
              <Dialog.Content>
                <Dialog.Header>
                  <Dialog.Title>System Retrain</Dialog.Title>
                </Dialog.Header>
                <Dialog.Body>
                  <Text>
                    This action will cause system retrain. Do you want to
                    proceed?
                  </Text>
                </Dialog.Body>
                <Dialog.Footer>
                  <Dialog.ActionTrigger asChild>
                    <Button
                      width='100%'
                      onClick={() => handleModelRetrainRun()}
                    >
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
      <VStack height='100%' gap='1rem'>
        <SimpleGrid columns={2} width='100%' gap='1rem'>
          <GridItem colSpan={{ base: 2, md: 2 }}>
            {data?.data && (
              <MainContainer
                title='New Trained Model'
                modeSelectorVisible={false}
              >
                <TrainedModelCard
                  trainedModel={data?.data}
                  onApprove={(batch_id) => handleSubmit(batch_id)}
                />
              </MainContainer>
            )}
          </GridItem>
          <GridItem colSpan={2} borderRadius='1rem' overflow='hidden'>
            <MainContainer title='Dag Information' modeSelectorVisible={false}>
              <DagInfoTable />
            </MainContainer>
          </GridItem>
        </SimpleGrid>
        <MainContainer
          title='Drift Detector Thresholds'
          modeSelectorVisible={false}
        >
          <DriftThresholdContainer />
        </MainContainer>
      </VStack>
    </PageContainer>
  );
};

export default Configuration;
