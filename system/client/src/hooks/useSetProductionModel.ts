import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const useSetProductionModel = () => {
  const apiClient = new APIClient('/v1/models/production');

  return useMutation({
    mutationFn: ({ batch_id }: { batch_id: string }) => apiClient.post({ params: { batch_id } }),
    onError: (err) => {
      console.log(err);
    },
  });
};

export default useSetProductionModel;
