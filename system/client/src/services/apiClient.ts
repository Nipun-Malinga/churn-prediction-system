import { FetchListResponse, FetchResponse } from '@/models/FetchResponse';
import axios, { AxiosRequestConfig } from 'axios';

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
  },
});
class APIClient<T, R = T> {
  private endpoint;

  constructor(endpoint: string) {
    this.endpoint = endpoint;
  }

  get = async (requestConfig?: AxiosRequestConfig) => {
    const resp = await axiosInstance.get<FetchResponse<T>>(this.endpoint, { ...requestConfig });
    return resp.data;
  };

  getAll = async (requestConfig?: AxiosRequestConfig) => {
    const resp = await axiosInstance.get<FetchListResponse<T>>(this.endpoint, { ...requestConfig });
    return resp.data;
  };

  post = async (requestConfig?: AxiosRequestConfig, data?: T) => {
    const resp = await axiosInstance.post<FetchResponse<R>>(this.endpoint, data, requestConfig);
    return resp.data;
  };

  patch = async (requestConfig?: AxiosRequestConfig, data?: T) => {
    const resp = await axiosInstance.patch<FetchResponse<T>>(this.endpoint, data, {
      ...requestConfig,
    });
    return resp.data;
  };
}

export default APIClient;
