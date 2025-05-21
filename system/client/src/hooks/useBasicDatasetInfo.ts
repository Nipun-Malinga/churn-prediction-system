import { BasicDatasetInfo } from '@/models/DatasetInfo';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import ms from 'ms';

const useBasicDatasetInfo = () => {
  const apiClient = new APIClient<BasicDatasetInfo>('/v1/data/info');
  const fetchData = () => apiClient.get();

  return useQuery({
    queryKey: ['basicDatasetInfo'],
    queryFn: fetchData,
    staleTime: ms('1 Minutes'),
    refetchInterval: ms('1 Minutes'),
  });
};

export default useBasicDatasetInfo;
