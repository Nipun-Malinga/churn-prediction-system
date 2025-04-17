import { Model } from '@/models/ModelDetails';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';

/* Change the model info fetcher to*/
const useModel = () => {
  const apiClient = new APIClient<Model>('/v1/models/');
  const fetchData = () => apiClient.getAll();

  return useQuery({
    queryKey: ['models'],
    queryFn: fetchData,
  });
};

export default useModel;
