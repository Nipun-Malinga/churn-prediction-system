import predictionSchema from '@/schemas/predictionSchema';
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
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { formInputs, selectionData } from '@/data/predictionForm';
import usePredictResults from '@/hooks/usePredictResults';
import PredictionResult from '../PredictionResult';
import { useState } from 'react';
import { PredictionResponse } from '@/models/Prediction';

type FormData = z.infer<typeof predictionSchema>;

const PredictionForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(predictionSchema) });

  const { mutate, isPending } = usePredictResults();

  const [predictionResponse, setPredictionResponse] = useState<PredictionResponse>();

  const onSubmit = (data: FormData) => {
    mutate(data, {
      onSuccess: (data) => {
        console.log(data);
        setPredictionResponse(data.data);
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
                    <Field.Label color={'#494f52'}>{input.title}</Field.Label>
                    <Input {...register(input.name as keyof FormData)} name={input.name} />
                    {errors[input.name as keyof FormData] && (
                      <Box color='red' fontSize='sm'>
                        {errors[input.name as keyof FormData]?.message?.toString()}
                      </Box>
                    )}
                  </Field.Root>
                ))}
              </SimpleGrid>

              <HStack wrap='wrap' justifyContent='center'>
                {selectionData.map((data, key) => (
                  <Field.Root key={key} width={{ base: '100%', sm: '48%', md: '23%' }}>
                    <Field.Label color='#494f52'>{data.title}</Field.Label>

                    <NativeSelect.Root>
                      <NativeSelect.Field
                        {...register(data.name as keyof FormData)}
                        name={data.name}
                        color='#838c91'
                        defaultValue=''
                      >
                        <option value='' disabled>{`Select ${data.title}`}</option>
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
            background={'#4880FF'}
            color={'#FFFFFF'}
            width={'10rem'}
            margin={'1rem'}
          >
            Submit
          </Button>
        </VStack>
      </form>
      {predictionResponse && <PredictionResult predictionResponse={predictionResponse} />}
    </>
  );
};

export default PredictionForm;
