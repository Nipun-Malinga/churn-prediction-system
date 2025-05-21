import { TrainedModel } from '@/models/ModelDetails';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import ms from 'ms';

const useTrainedModels = () => {
  const apiClient = new APIClient<TrainedModel>('/v1/models/production');
  const fetchData = () => apiClient.get();

  return useQuery({
    queryKey: ['trainedModels'],
    queryFn: fetchData,
    staleTime: ms('1 Minutes'),
    refetchInterval: ms('1 Minutes'),
  });
};

export default useTrainedModels;
