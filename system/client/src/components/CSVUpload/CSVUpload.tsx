import useUploadCSV from '@/hooks/useUploadCSV';
import csvUploadSchema from '@/schemas/csvUploadSchema';
import useNotificationStore from '@/store/useNotificationStore';
import { Box, Button, FileUpload, HStack } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useEffect } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { HiUpload } from 'react-icons/hi';
import { z } from 'zod';

const CSVUpload = () => {
  const { mutate, error, isPending, isError, isSuccess } = useUploadCSV();
  const { setNotification } = useNotificationStore();

  useEffect(() => {
    isSuccess &&
      setNotification({
        type: 'success',
        info: 'Dataset File Uploaded Successfully.',
      });
    error &&
      setNotification({ type: 'error', info: 'Failed to upload CSV file.' });
  }, [isSuccess, isError]);

  type FormData = z.infer<typeof csvUploadSchema>;

  const {
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(csvUploadSchema),
  });

  const onSubmit = (data: FormData) => {
    mutate(data.file[0]);
  };

  return (
    <Box as='form' onSubmit={handleSubmit(onSubmit)} width='100%'>
      <Controller
        name='file'
        control={control}
        defaultValue={undefined}
        render={({ field: { onChange } }) => (
          <FileUpload.Root>
            <FileUpload.List />
            <FileUpload.HiddenInput
              type='file'
              accept='.csv'
              onChange={(e) => onChange(e.target.files)}
            />
            <HStack alignItems={'center'}>
              <FileUpload.Trigger asChild>
                <Button variant='outline' size='sm'>
                  <HiUpload /> Upload file
                </Button>
              </FileUpload.Trigger>
              <Button
                type='submit'
                size='sm'
                width={'7rem'}
                loading={isPending}
              >
                Submit
              </Button>
            </HStack>
          </FileUpload.Root>
        )}
      />
      {errors.file && (
        <p style={{ color: 'red', marginTop: '0.5rem' }}>
          {errors.file.message}
        </p>
      )}
    </Box>
  );
};

export default CSVUpload;
