import useDagInfo from '@/hooks/useDagInfo';
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
    <Table.ScrollArea 
      width={'100%'}
      borderRadius={'0.75rem'}
      border={'1px solid'}
      borderColor={'gray.200'}
      boxShadow={'0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)'}
    >
      <Table.Root 
        size='lg' 
        borderRadius={'0.75rem'} 
        overflow={'hidden'}
        variant={'outline'}
      >
        <Table.Header 
          bg={'gray.50'}
          borderBottom={'2px solid'}
          borderColor={'gray.200'}
        >
          <Table.Row>
            <Table.ColumnHeader 
              fontWeight={'600'}
              fontSize={'0.875rem'}
              color={'gray.700'}
              textTransform={'uppercase'}
              letterSpacing={'0.05em'}
              py={'1rem'}
            >
              Dag Name
            </Table.ColumnHeader>
            <Table.ColumnHeader 
              fontWeight={'600'}
              fontSize={'0.875rem'}
              color={'gray.700'}
              textTransform={'uppercase'}
              letterSpacing={'0.05em'}
            >
              Description
            </Table.ColumnHeader>
            <Table.ColumnHeader 
              fontWeight={'600'}
              fontSize={'0.875rem'}
              color={'gray.700'}
              textTransform={'uppercase'}
              letterSpacing={'0.05em'}
            >
              Last Triggered Time
            </Table.ColumnHeader>
            <Table.ColumnHeader 
              fontWeight={'600'}
              fontSize={'0.875rem'}
              color={'gray.700'}
              textTransform={'uppercase'}
              letterSpacing={'0.05em'}
            >
              Next Dag Run
            </Table.ColumnHeader>
            <Table.ColumnHeader 
              fontWeight={'600'}
              fontSize={'0.875rem'}
              color={'gray.700'}
              textTransform={'uppercase'}
              letterSpacing={'0.05em'}
            >
              Scheduled Interval
            </Table.ColumnHeader>
            <Table.ColumnHeader 
              textAlign='end'
              fontWeight={'600'}
              fontSize={'0.875rem'}
              color={'gray.700'}
              textTransform={'uppercase'}
              letterSpacing={'0.05em'}
            >
              Status
            </Table.ColumnHeader>
            {/* <Table.ColumnHeader textAlign='end'>Trigger Dag Run</Table.ColumnHeader> */}
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {data?.data.dags &&
            data?.data.dags.map((dag, key) => (
              <Table.Row 
                key={key}
                transition={'all 0.2s'}
                _hover={{
                  bg: 'gray.50',
                }}
                borderBottom={'1px solid'}
                borderColor={'gray.100'}
              >
                <Table.Cell 
                  fontWeight={'500'}
                  color={'gray.800'}
                  py={'1rem'}
                >
                  {dag.dag_display_name}
                </Table.Cell>
                <Table.Cell 
                  color={'gray.600'}
                  fontSize={'0.875rem'}
                >
                  {dag.description ?? 'Not Available'}
                </Table.Cell>
                <Table.Cell 
                  color={'gray.600'}
                  fontSize={'0.875rem'}
                  fontFamily={'mono'}
                >
                  {dag.last_parsed_time}
                </Table.Cell>
                <Table.Cell 
                  color={'gray.600'}
                  fontSize={'0.875rem'}
                  fontFamily={'mono'}
                >
                  {dag.next_dagrun ?? 'Not Available'}
                </Table.Cell>
                <Table.Cell 
                  color={'gray.600'}
                  fontSize={'0.875rem'}
                  fontFamily={'mono'}
                >
                  {dag.schedule_interval.value}
                </Table.Cell>
                <Table.Cell textAlign='end'>
                  <Button
                    width={'6.5rem'}
                    size={'sm'}
                    background={dag.is_paused ? 'red.500' : 'green.500'}
                    color={'white'}
                    fontWeight={'600'}
                    fontSize={'0.75rem'}
                    letterSpacing={'0.025em'}
                    borderRadius={'0.5rem'}
                    loading={isPending}
                    onClick={() => handleToggleRun(dag.dag_id, !dag.is_paused)}
                    transition={'all 0.2s'}
                    _hover={{
                      background: dag.is_paused ? 'red.600' : 'green.600',
                      transform: 'scale(1.02)',
                    }}
                    _active={{
                      transform: 'scale(0.98)',
                    }}
                    boxShadow={'0 1px 2px 0 rgba(0, 0, 0, 0.05)'}
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