import useDagInfo from '@/hooks/useDagInfo';
// import useDagRun from '@/hooks/useDagRun';
import useDagToggle from '@/hooks/useDagToggle';
import { Button, Table } from '@chakra-ui/react';

const DagInfoTable = () => {
  const { data, refetch } = useDagInfo();
  const { mutate, isPending } = useDagToggle();
  // const { mutate: runDag } = useDagRun();

  const handleToggleRun = (dag_id: string, is_paused: boolean) => {
    mutate(
      { dag_id, is_paused },
      {
        onSuccess: () => {
          refetch();
        },
      }
    );
  };

  // const handleDagRun = (dag_id: string) => {
  //   runDag({ dag_id });
  // };

  return (
    <Table.ScrollArea width={'100%'}>
      <Table.Root size='lg' borderRadius={'1rem'} overflow={'hidden'}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader>Dag Name</Table.ColumnHeader>
            <Table.ColumnHeader>Description</Table.ColumnHeader>
            <Table.ColumnHeader>Last Triggered Time</Table.ColumnHeader>
            <Table.ColumnHeader>Next Dag Run</Table.ColumnHeader>
            <Table.ColumnHeader>Scheduled Interval</Table.ColumnHeader>
            <Table.ColumnHeader textAlign='center'>Status</Table.ColumnHeader>
            {/* <Table.ColumnHeader textAlign='end'>Trigger Dag Run</Table.ColumnHeader> */}
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {data?.data.dags &&
            data?.data.dags.map((dag, key) => (
              <Table.Row key={key}>
                <Table.Cell>{dag.dag_display_name}</Table.Cell>
                <Table.Cell>{dag.description ?? 'Not Available'}</Table.Cell>
                <Table.Cell>{dag.last_parsed_time}</Table.Cell>
                <Table.Cell>{dag.next_dagrun ?? 'Not Available'}</Table.Cell>
                <Table.Cell>{dag.schedule_interval.value}</Table.Cell>
                <Table.Cell textAlign='end'>
                  <Button
                    width={'6.5rem'}
                    background={dag.is_paused ? 'red.500' : 'blue.400'}
                    loading={isPending}
                    onClick={() => handleToggleRun(dag.dag_id, !dag.is_paused)}
                  >
                    {dag.is_paused ? 'PAUSED' : 'ACTIVE'}
                  </Button>
                </Table.Cell>

                {/*Add Safety Mechanism To prevent triggering more than one dag run */}

                {/* <Table.Cell textAlign='end'>
                  <Button
                    width={'6.5rem'}
                    background={'red.500'}
                    loading={isPending}
                    onClick={() => handleDagRun(dag.dag_id)}
                  >
                    {'Trigger'}
                  </Button>
                </Table.Cell> */}
              </Table.Row>
            ))}
        </Table.Body>
      </Table.Root>
    </Table.ScrollArea>
  );
};

export default DagInfoTable;
