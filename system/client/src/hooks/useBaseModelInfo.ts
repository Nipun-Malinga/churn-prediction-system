import { AdvancedModelInfo } from '@/models/ModelDetails';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import ms from 'ms';

const useBaseModelInfo = () => {
  const apiClient = new APIClient<AdvancedModelInfo>('/v1/models/base');
  const fetchData = () => apiClient.get();

  return useQuery({
    queryKey: ['baseModelData'],
    queryFn: fetchData,
    staleTime: ms('1 Minutes'),
    refetchInterval: ms('1 Minutes'),
  });
};

export default useBaseModelInfo;
