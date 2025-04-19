import { PerformanceDriftHistory } from '@/models/ModelPerformance';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import ms from 'ms';

const usePerformanceDriftHistory = () => {
  const apiClient = new APIClient<PerformanceDriftHistory>('/v1/models/drift');
  const fetchData = () =>
    apiClient.getAll();

  return useQuery({
    queryKey: ['performanceDriftHistory'],
    queryFn: fetchData,
    staleTime: ms('5 Minutes'),
  });
};

export default usePerformanceDriftHistory;
