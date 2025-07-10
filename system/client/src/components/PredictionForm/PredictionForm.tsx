import { formInputs, selectionData } from '@/data/predictionForm';
import usePredictResults from '@/hooks/usePredictResults';
import predictionSchema from '@/schemas/predictionSchema';
import useNotificationStore from '@/store/useNotificationStore';
import {
  Box,
  Button,
  Field,
  Fieldset,
  HStack,
  Input,
  NativeSelect,
  SimpleGrid,
  VStack,
} from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import PredictionResult from '../PredictionResult';

const PredictionForm = () => {
  const { mutate, data, error, isPending, isSuccess } = usePredictResults();
  const { setNotification } = useNotificationStore();

  useEffect(() => {
    error &&
      setNotification({ type: 'error', info: 'Unexpected error occurred' });
    isSuccess &&
      setNotification({
        type: 'success',
        info: 'Churn probability predicted successfully',
      });
  }, [error, isSuccess]);

  type FormData = z.infer<typeof predictionSchema>;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(predictionSchema) });

  const onSubmit = (data: FormData) => {
    mutate(data);
  };

  return (
    <>
      <VStack
        as='form'
        onSubmit={handleSubmit(onSubmit)}
        alignItems={'center'}
        width={'100%'}
      >
        <Fieldset.Root size='lg'>
          <Fieldset.Content width={'100%'}>
            <SimpleGrid
              columns={2}
              gap={'1rem'}
              width={'100%'}
              justifyContent={'space-between'}
            >
              {formInputs.map((input, key) => (
                <Field.Root key={key}>
                  <Field.Label color={'#494f52'}>{input.title}</Field.Label>
                  <Input
                    {...register(input.name as keyof FormData)}
                    name={input.name}
                  />
                  {errors[input.name as keyof FormData] && (
                    <Box color='red' fontSize='sm'>
                      {errors[
                        input.name as keyof FormData
                      ]?.message?.toString()}
                    </Box>
                  )}
                </Field.Root>
              ))}
            </SimpleGrid>

            <HStack wrap='wrap' justifyContent='center'>
              {selectionData.map((data, key) => (
                <Field.Root
                  key={key}
                  width={{ base: '100%', sm: '48%', md: '23%' }}
                >
                  <Field.Label color='#494f52'>{data.title}</Field.Label>

                  <NativeSelect.Root>
                    <NativeSelect.Field
                      {...register(data.name as keyof FormData)}
                      name={data.name}
                      color='#838c91'
                      defaultValue=''
                    >
                      <option
                        value=''
                        disabled
                      >{`Select ${data.title}`}</option>
                      {data.data.map((option, i) => (
                        <option key={i} value={option.value}>
                          {option.key}
                        </option>
                      ))}
                    </NativeSelect.Field>
                    <NativeSelect.Indicator />
                  </NativeSelect.Root>

                  {errors[data.name as keyof FormData] && (
                    <Box color='red' fontSize='sm'>
                      {errors[data.name as keyof FormData]?.message?.toString()}
                    </Box>
                  )}
                </Field.Root>
              ))}
            </HStack>
          </Fieldset.Content>
        </Fieldset.Root>
        <Button
          disabled={isPending}
          loading={isPending}
          type='submit'
          background='#4880FF'
          color='#FFFFFF'
          width={'10rem'}
          margin={'1rem'}
        >
          Submit
        </Button>
      </VStack>

      {data?.data && (
        <PredictionResult
          predictionResponse={{
            Prediction: data.data.Prediction,
            Probability: data.data.Probability,
          }}
        />
      )}
    </>
  );
};

export default PredictionForm;
