import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const useUploadCSV = () => {
  const apiClient = new APIClient('/v1/data/csv');

  return useMutation({
    mutationFn: (file: File) => {
      const formData = new FormData();
      formData.append('data_source', file);
      return apiClient.post(undefined, formData);
    },
  });
};

export default useUploadCSV;
