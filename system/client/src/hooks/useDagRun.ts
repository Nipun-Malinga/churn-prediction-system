import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const useDagRun = () => {
  const apiClient = new APIClient('/v1/airflow/dags');
  
  return useMutation({
    mutationFn: ({ dag_id }: { dag_id: string }) => apiClient.post({ params: { dag_id } }),
  });
};

export default useDagRun;
