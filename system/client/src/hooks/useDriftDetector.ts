import DriftDetectorResponse from '@/models/DriftDetector';
import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const useDriftDetectorThreshold = () => {
  const apiClient = new APIClient<DriftDetectorResponse>('/v1/models/evaluation-threshold');

  return useMutation({
    mutationFn: (data: DriftDetectorResponse) => apiClient.post(undefined, data),
    onError: (err) => {
      console.log(err);
    },
  });
};

export default useDriftDetectorThreshold;
