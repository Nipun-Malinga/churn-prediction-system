import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const useDagToggle = () => {
  const apiClient = new APIClient('/v1/airflow/dags');

  return useMutation({
    mutationFn: ({ dag_id, is_paused }: { dag_id: string; is_paused: boolean }) =>
      apiClient.patch({ params: { dag_id } }, { is_paused }),
    onError: (err) => {
      console.error(err);
    },
  });
};

export default useDagToggle;
