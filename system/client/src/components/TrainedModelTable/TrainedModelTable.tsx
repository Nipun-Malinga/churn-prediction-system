import useTrainedModels from '@/hooks/useTrainedModels';
import { Button, Table } from '@chakra-ui/react';
import { format } from 'date-fns';

const TrainedModelTable = () => {
  const { data } = useTrainedModels();

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
          {data?.data && (
            <Table.Row>
              <Table.Cell>{data.data.model_name}</Table.Cell>
              <Table.Cell>{data.data.version_name}</Table.Cell>
              <Table.Cell>{format(new Date(data.data.trained_date), 'yyyy-MM-dd')}</Table.Cell>
              <Table.Cell>{(data.data.accuracy * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell>{(data.data.precision * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell>{(data.data.recall * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell>{(data.data.f1_score * 100).toFixed(2)}%</Table.Cell>
              <Table.Cell textAlign='end'>
                <Button width={'6.5rem'} disabled={data.data.is_production_model}>
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
