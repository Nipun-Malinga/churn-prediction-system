import { PerformanceDataPoint } from '@/models/ModelPerformance';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import ms from 'ms';

const usePerformanceHistory = (model_id: number, filter_type: string) => {
  const apiClient = new APIClient<PerformanceDataPoint>('/v1/models/charts');
  const fetchData = () =>
    apiClient.getAll({
      params: { model_id, filter_type },
    });

  return useQuery({
    queryKey: ['performanceHistory', model_id, filter_type],
    queryFn: fetchData,
    staleTime: ms('1 Minutes'),
    refetchInterval: ms('1 Minutes'),
  });
};

export default usePerformanceHistory;
