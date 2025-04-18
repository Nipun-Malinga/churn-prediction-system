import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const useModelRetrain = (dag_id: string) => {
  const apiClient = new APIClient('/v1/airflow/dags');
  const postData = () =>
    apiClient.post({
      params: { dag_id },
    });

  return useMutation({
    mutationFn: postData,
  });
};

export default useModelRetrain;
