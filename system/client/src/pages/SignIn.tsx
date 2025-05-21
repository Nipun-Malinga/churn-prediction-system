import NotificationBar from '@/components/NotificationBar';
import loginInputs from '@/data/login';
import useLogin from '@/hooks/useLogin';
import signInSchema from '@/schemas/signInSchema';
import { Box, Button, Field, Fieldset, Heading, Input, Text, VStack } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { z } from 'zod';

type FormData = z.infer<typeof signInSchema>;

const SignIn = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(signInSchema) });

  const navigate = useNavigate();

  const { mutate, isPending, isError, isSuccess } = useLogin();

  const onSubmit = (data: FormData) => {
    mutate(data, {
      onSuccess: (data) => {
        localStorage.setItem('auth_token', data.data.auth_token);
        navigate('/dashboard');
      },
    });
  };

  return (
    <VStack bg='#568AFF' height='100vh' align='center' justify='center' p={4}>
      <Box
        as='form'
        onSubmit={handleSubmit(onSubmit)}
        bg='white'
        borderRadius='2xl'
        boxShadow='lg'
        p={{ base: 6, md: 10 }}
        width={{ base: '90%', md: '50%' }}
      >
        <VStack gap={6} align='stretch'>
          <Box textAlign='center'>
            <Heading fontSize='2xl' fontWeight='bold'>
              Login to Account
            </Heading>
            <Text fontSize='md' color='gray.600'>
              Enter your credentials below
            </Text>
          </Box>

          <Fieldset.Root size='lg'>
            <Fieldset.Content>
              <VStack gap={5} align='stretch'>
                {loginInputs.map((input, key) => (
                  <Field.Root key={key}>
                    <Field.Label htmlFor={input.name} color='gray.700' mb={1}>
                      {input.title}
                    </Field.Label>
                    <Input
                      id={input.name}
                      {...register(input.name as keyof FormData)}
                      name={input.name}
                      type={input.type}
                      bg='gray.50'
                      _focus={{ borderColor: '#4880FF', boxShadow: 'outline' }}
                    />
                    {errors[input.name as keyof FormData] && (
                      <Text color='red.500' fontSize='sm'>
                        {errors[input.name as keyof FormData]?.message?.toString()}
                      </Text>
                    )}
                  </Field.Root>
                ))}
              </VStack>
            </Fieldset.Content>
          </Fieldset.Root>

          <Button
            type='submit'
            loading={isPending}
            bg='#4880FF'
            _hover={{ bg: '#3a6edc' }}
            color='white'
            size='lg'
            width='full'
          >
            Submit
          </Button>
        </VStack>
        {isSuccess && (
          <NotificationBar type='success' notification='User authenticated successfully.' />
        )}
        {isError && <NotificationBar type='error' notification='Failed to authenticate user.' />}
      </Box>
    </VStack>
  );
};

export default SignIn;
