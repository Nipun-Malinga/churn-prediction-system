import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { FileUpload, Button, HStack } from '@chakra-ui/react';
import { HiUpload } from 'react-icons/hi';
import { z } from 'zod';
import csvUploadSchema from '@/schemas/csvUploadSchema';
import useUploadCSV from '@/hooks/useUploadCSV';
import NotificationBar from '../NotificationBar';

type FormData = z.infer<typeof csvUploadSchema>;

const CSVUpload = () => {
  const { mutate: uploadCSV, isPending, isSuccess, isError } = useUploadCSV();

  const {
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(csvUploadSchema),
  });

  const onSubmit = (data: FormData) => {
    const file = data.file[0];
    uploadCSV(file);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ width: '100%' }}>
      {isSuccess && (
        <NotificationBar type={'success'} notification='Dataset File Uploaded Successfully.' />
      )}
      {isError && <NotificationBar type={'error'} notification='Failed to upload CSV file.' />}
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
              <Button type='submit' size='sm' width={'7rem'} loading={isPending}>
                Submit
              </Button>
            </HStack>
          </FileUpload.Root>
        )}
      />
      {errors.file && <p style={{ color: 'red', marginTop: '0.5rem' }}>{errors.file.message}</p>}
    </form>
  );
};

export default CSVUpload;
