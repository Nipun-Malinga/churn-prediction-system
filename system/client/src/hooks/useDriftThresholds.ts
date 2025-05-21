import DriftDetectorResponse from '@/models/DriftDetector';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import ms from 'ms';

const useDriftThresholds = () => {
  const apiClient = new APIClient<DriftDetectorResponse>('/v1/models/evaluation-threshold');
  const fetchData = () => apiClient.get();

  return useQuery({
    queryKey: ['driftDetectorThresholds'],
    queryFn: fetchData,
    staleTime: ms('1 Minutes'),
    refetchInterval: ms('1 Minutes'),
  });
};

export default useDriftThresholds;
