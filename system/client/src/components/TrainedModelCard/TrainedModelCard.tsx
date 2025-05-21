import useBaseModelInfo from '@/hooks/useBaseModelInfo';
import { TrainedModel } from '@/models/ModelDetails';
import {
  Box,
  Button,
  Card,
  CloseButton,
  Dialog,
  HStack,
  Portal,
  SimpleGrid,
  Span,
  Tabs,
  Text,
  VStack,
} from '@chakra-ui/react';
import { format } from 'date-fns';
import { FaRegCircleCheck, FaArrowUp, FaArrowDown } from 'react-icons/fa6';

interface Props {
  trainedModel: TrainedModel;
  onApprove: (batch_id: string) => void;
}

const DriftText = ({ value }: { value: number }) => {
  const isPositive = value >= 0;

  return (
    <HStack gap={1}>
      {isPositive ? <FaArrowUp color='green' /> : <FaArrowDown color='red' />}
      <Text fontSize='1rem' color={isPositive ? 'green.400' : 'red.400'}>
        {value.toFixed(2)}% performance
      </Text>
    </HStack>
  );
};

const TrainedModelCard = ({ trainedModel, onApprove }: Props) => {
  const { data: baseModelInfo } = useBaseModelInfo();

  const drift = (newVal: number, oldVal: number) => (newVal - oldVal) * 100;

  return (
    <Card.Root width={'100%'} border={'none'}>
      <Tabs.Root defaultValue='members'>
        <Tabs.Content value='members'>
          <Card.Body>
            <SimpleGrid columns={{ base: 2, md: 4 }} textAlign='center' gap='1rem'>
              {baseModelInfo?.data && (
                <>
                  <MetricBlock
                    label='Accuracy'
                    value={trainedModel.accuracy}
                    driftValue={drift(trainedModel.accuracy, baseModelInfo.data.accuracy)}
                  />
                  <MetricBlock
                    label='Precision'
                    value={trainedModel.precision}
                    driftValue={drift(trainedModel.precision, baseModelInfo.data.precision)}
                  />
                  <MetricBlock
                    label='Recall'
                    value={trainedModel.recall}
                    driftValue={drift(trainedModel.recall, baseModelInfo.data.recall)}
                  />
                  <MetricBlock
                    label='F1 Score'
                    value={trainedModel.f1_score}
                    driftValue={drift(trainedModel.f1_score, baseModelInfo.data.f1_score)}
                  />
                </>
              )}
            </SimpleGrid>
          </Card.Body>
        </Tabs.Content>
      </Tabs.Root>

      <Card.Footer justifyContent='space-between'>
        <HStack gap='1rem' fontSize='0.9rem'>
          <Text>
            <Span fontWeight='bold'>Model: </Span>
            {trainedModel.model_name}
          </Text>
          <Text>
            <Span fontWeight='bold'>Version:</Span> {trainedModel.version_name}
          </Text>
          <Text>
            <Span fontWeight='bold'>Last updated: </Span>
            {format(new Date(trainedModel.trained_date), 'yyyy-MM-dd')}
          </Text>
        </HStack>
        <HStack>
          <Dialog.Root>
            <Dialog.Trigger width='5rem' asChild>
              <Button width='100%'>
                <FaRegCircleCheck />
              </Button>
            </Dialog.Trigger>
            <Portal>
              <Dialog.Backdrop />
              <Dialog.Positioner>
                <Dialog.Content>
                  <Dialog.Header>
                    <Dialog.Title>Model Update</Dialog.Title>
                  </Dialog.Header>
                  <Dialog.Body>
                    <Text>
                      This action will update the production model. Do you want to proceed?
                    </Text>
                  </Dialog.Body>
                  <Dialog.Footer>
                    <Dialog.ActionTrigger asChild>
                      <Button variant='outline'>Cancel</Button>
                    </Dialog.ActionTrigger>
                    <Dialog.ActionTrigger asChild>
                      <Button onClick={() => onApprove(trainedModel.batch_id)}>Yes</Button>
                    </Dialog.ActionTrigger>
                  </Dialog.Footer>
                  <Dialog.CloseTrigger asChild>
                    <CloseButton size='sm' />
                  </Dialog.CloseTrigger>
                </Dialog.Content>
              </Dialog.Positioner>
            </Portal>
          </Dialog.Root>
        </HStack>
      </Card.Footer>
    </Card.Root>
  );
};

// Extracted metric block
const MetricBlock = ({
  label,
  value,
  driftValue,
}: {
  label: string;
  value: number;
  driftValue: number;
}) => (
  <Box>
    <VStack>
      <HStack>
        <Text fontSize='1.25rem'>{(value * 100).toFixed(2)}%</Text>
        <DriftText value={driftValue} />
      </HStack>
      <Text fontSize='0.9rem' fontWeight='medium'>
        {label}
      </Text>
    </VStack>
  </Box>
);

export default TrainedModelCard;
