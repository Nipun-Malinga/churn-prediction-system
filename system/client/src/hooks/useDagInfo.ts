import { DagDetails } from '@/models/DagDetails';
import APIClient from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import ms from 'ms';

const useDagInfo = () => {
  const apiClient = new APIClient<DagDetails>('/v1/airflow/dags');
  const fetchData = () => apiClient.get();

  return useQuery({
    queryKey: ['dagDetails'],
    queryFn: fetchData,
    staleTime: ms('5 Minutes'),
  });
};

export default useDagInfo;
