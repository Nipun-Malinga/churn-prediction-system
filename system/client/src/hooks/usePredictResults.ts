import { Prediction, PredictionResponse } from '@/models/Prediction';
import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const usePredictResults = () => {
  const apiClient = new APIClient<Prediction, PredictionResponse>('/v1/predictions/predict');

  return useMutation({
    mutationFn: (data: Prediction) => apiClient.post(undefined, data),
    onError: (err) => {
      console.log(err);
    },
  });
};

export default usePredictResults;
