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
import { FaRegCircleCheck } from 'react-icons/fa6';

interface Props {
  trainedModel: TrainedModel;
  onApprove: (batch_id: string) => void;
}

const TrainedModelCard = ({ trainedModel, onApprove }: Props) => {
  const { data: baseModelInfo } = useBaseModelInfo();

  return (
    <>
      <Card.Root width={'100%'} border={'none'}>
        <Tabs.Root defaultValue='members'>
          <Tabs.Content value='members'>
            <Card.Body>
              <SimpleGrid columns={{ base: 2, md: 4 }} textAlign={'center'} gap={'1rem'}>
                <Box>
                  <VStack>
                    <HStack>
                      <Text fontSize={'1.25rem'}>{(trainedModel.accuracy * 100).toFixed(2)}%</Text>
                      <Text fontSize={'1rem'}>
                        {baseModelInfo?.data &&
                          (
                            trainedModel.accuracy * 100 -
                            baseModelInfo?.data.accuracy * 100
                          ).toFixed(2)}
                        %
                      </Text>
                    </HStack>
                    <Text fontSize={'0.9rem'} fontWeight={'medium'}>
                      Accuracy
                    </Text>
                  </VStack>
                </Box>
                <Box>
                  <VStack>
                    <HStack>
                      <Text fontSize={'1.25rem'}>{(trainedModel.precision * 100).toFixed(2)}%</Text>
                      <Text fontSize={'1rem'}>
                        {baseModelInfo?.data &&
                          (
                            trainedModel.precision * 100 -
                            baseModelInfo?.data.precision * 100
                          ).toFixed(2)}
                        %
                      </Text>
                    </HStack>
                    <Text fontSize={'0.9rem'} fontWeight={'medium'}>
                      Precision
                    </Text>
                  </VStack>
                </Box>
                <Box>
                  <VStack>
                    <HStack>
                      <Text fontSize={'1.25rem'}>{(trainedModel.recall * 100).toFixed(2)}%</Text>
                      <Text fontSize={'1rem'}>
                        {baseModelInfo?.data &&
                          (trainedModel.recall * 100 - baseModelInfo?.data.recall * 100).toFixed(2)}
                        %
                      </Text>
                    </HStack>
                    <Text fontSize={'0.9rem'} fontWeight={'medium'}>
                      Recall
                    </Text>
                  </VStack>
                </Box>
                <Box>
                  <VStack>
                    <HStack>
                      <Text fontSize={'1.25rem'}>{(trainedModel.f1_score * 100).toFixed(2)}%</Text>
                      <Text fontSize={'1rem'}>
                        {baseModelInfo?.data &&
                          (
                            trainedModel.f1_score * 100 -
                            baseModelInfo?.data.f1_score * 100
                          ).toFixed(2)}
                        %
                      </Text>
                    </HStack>
                    <Text fontSize={'0.9rem'} fontWeight={'medium'}>
                      F1 Score
                    </Text>
                  </VStack>
                </Box>
              </SimpleGrid>
            </Card.Body>
          </Tabs.Content>
        </Tabs.Root>
        <Card.Footer justifyContent='space-between'>
          <HStack gap={'1rem'} fontSize={'0.9rem'}>
            <Text>
              <Span fontWeight={'bold'}>Model: </Span>
              {trainedModel.model_name}
            </Text>
            <Text>
              <Span fontWeight={'bold'}>Version:</Span> {trainedModel.version_name}
            </Text>
            <Text>
              <Span fontWeight={'bold'}>Last updated: </Span>
              {format(new Date(trainedModel.trained_date), 'yyyy-MM-dd')}
            </Text>
          </HStack>
          <HStack>
            <Dialog.Root>
              <Dialog.Trigger width={'5rem'} asChild>
                {/*Add Styles */}
                <Button width={'100%'}>
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
    </>
  );
};

export default TrainedModelCard;
