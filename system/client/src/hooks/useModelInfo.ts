import { AdvancedModelInfo, BasicModelInfo } from '@/models/ModelDetails';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';

const useBasicModelInfo = (model_id: number) => {
  const apiClient = new APIClient<BasicModelInfo>('/v1/models/info/basic');
  const fetchData = () =>
    apiClient.get({
      params: { model_id },
    });

  return useQuery({
    queryKey: ['basicModelInfo', model_id],
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
