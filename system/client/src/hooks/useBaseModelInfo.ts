import { AdvancedModelInfo } from '@/models/ModelDetails';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';

const useBaseModelInfo = () => {
  const apiClient = new APIClient<AdvancedModelInfo>('/v1/models/base');
  const fetchData = () => apiClient.get();

  return useQuery({
    queryKey: ['baseModelData'],
    queryFn: fetchData,
  });
};

export default useBaseModelInfo;
