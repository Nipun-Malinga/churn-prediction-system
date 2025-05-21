import formInputs from '@/data/driftDetector';
import useDriftDetectorThreshold from '@/hooks/useDriftDetector';
import driftDetectorSchema from '@/schemas/driftDetectorSchema';
import useTriggerFetchThresholdsStore from '@/store/useTriggerFetchThresholdsStore';
import { Box, Button, Field, Fieldset, Input, SimpleGrid, VStack } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import NotificationBar from '../NotificationBar';

type FormData = z.infer<typeof driftDetectorSchema>;

const DriftDetectorForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(driftDetectorSchema) });

  const { mutate, isPending, isError, isSuccess } = useDriftDetectorThreshold();
  const { fetchThresholds } = useTriggerFetchThresholdsStore();

  const onSubmit = (data: FormData) => {
    mutate(data, {
      onSuccess: () => {
        fetchThresholds();
      },
    });
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} style={{ width: '100%' }}>
        <VStack alignItems={'center'} width={'100%'}>
          <Fieldset.Root size='lg'>
            <Fieldset.Content width={'100%'}>
              <SimpleGrid columns={2} gap={'1rem'} width={'100%'} justifyContent={'space-between'}>
                {formInputs.map((input, key) => (
                  <Field.Root key={key}>
                    <Field.Label htmlFor={input.name} color={'#494f52'}>
                      {input.title}
                    </Field.Label>
                    <Input
                      id={input.name}
                      {...register(input.name as keyof FormData)}
                      name={input.name}
                    />
                    {errors[input.name as keyof FormData] && (
                      <Box color='red' fontSize='sm'>
                        {errors[input.name as keyof FormData]?.message?.toString()}
                      </Box>
                    )}
                  </Field.Root>
                ))}
              </SimpleGrid>
            </Fieldset.Content>
          </Fieldset.Root>
          <Button
            loading={isPending}
            type='submit'
            background={'#4880FF'}
            color={'#FFFFFF'}
            width={'10rem'}
            margin={'1rem'}
          >
            Submit
          </Button>
        </VStack>
      </form>
      {isSuccess && (
        <NotificationBar
          type={'success'}
          notification='Drift detector thresholds set successfully.'
        />
      )}
      {isError && (
        <NotificationBar type={'error'} notification='Failed to set Drift detector thresholds.' />
      )}
    </>
  );
};

export default DriftDetectorForm;
