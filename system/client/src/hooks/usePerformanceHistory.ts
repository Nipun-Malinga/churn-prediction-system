import APIClient from '@/services/apiClient';
import { PerformanceDataPoint } from '@/models';
import { useQuery } from '@tanstack/react-query';

const usePerformanceHistory = (model_id: number, filter_type: string) => {
  const apiClient = new APIClient<PerformanceDataPoint>('/v1/models/charts');
  const fetchData = () =>
    apiClient.getAll({
      params: { model_id, filter_type },
    });

  return useQuery({
    queryKey: ['performanceHistory', model_id, filter_type],
    queryFn: fetchData,
  });
};

export default usePerformanceHistory;
