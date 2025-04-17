import { AdvancedModelInfo, BasicModelInfo } from '@/models/ModelDetails';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';

const useBasicModelInfo = () => {
  const apiClient = new APIClient<BasicModelInfo>('/v1/models/info');
  const fetchData = () => apiClient.getAll();

  return useQuery({
    queryKey: ['basicModelInfo'],
    queryFn: fetchData,
  });
};

const useAdvancedModelInfo = (model_id: number) => {
  const apiClient = new APIClient<AdvancedModelInfo>('/v1/models/info/advanced');
  const fetchData = () =>
    apiClient.get({
      params: { model_id },
    });

  return useQuery({
    queryKey: ['advancedModelInfo', model_id],
    queryFn: fetchData,
  });
};

export { useAdvancedModelInfo, useBasicModelInfo };
