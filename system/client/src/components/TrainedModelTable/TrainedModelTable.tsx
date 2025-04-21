import useTrainedModelStore from '@/store/useTrainedModelStore';
import { Button, Table } from '@chakra-ui/react';
import { format } from 'date-fns';

const TrainedModelTable = () => {
  const { trainedModel } = useTrainedModelStore();

  return (
    <Table.ScrollArea width={'100%'}>
      <Table.Root size='lg' borderRadius={'1rem'} overflow={'hidden'}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader>Model</Table.ColumnHeader>
            <Table.ColumnHeader>Version</Table.ColumnHeader>
            <Table.ColumnHeader>Trained Date</Table.ColumnHeader>
            <Table.ColumnHeader>Accuracy</Table.ColumnHeader>
            <Table.ColumnHeader>Precision</Table.ColumnHeader>
            <Table.ColumnHeader>Recall</Table.ColumnHeader>
            <Table.ColumnHeader>F1 Score</Table.ColumnHeader>
            <Table.ColumnHeader textAlign='end'>Status</Table.ColumnHeader>
            {/* <Table.ColumnHeader textAlign='end'>Trigger Dag Run</Table.ColumnHeader> */}
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {trainedModel && (
            <Table.Row>
              <Table.Cell>{trainedModel.model_name}</Table.Cell>
              <Table.Cell>{trainedModel.version_name}</Table.Cell>
              <Table.Cell>{format(new Date(trainedModel.trained_date), 'yyyy-MM-dd')}</Table.Cell>
              <Table.Cell>{(trainedModel.accuracy * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell>{(trainedModel.precision * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell>{(trainedModel.recall * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell>{(trainedModel.f1_score * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell textAlign='end'>
                <Button width={'6.5rem'} disabled={trainedModel.is_production_model}>
                  {'Ready'}
                </Button>
              </Table.Cell>
            </Table.Row>
          )}
        </Table.Body>
      </Table.Root>
    </Table.ScrollArea>
  );
};

export default TrainedModelTable;
