import { FetchListResponse, FetchResponse } from '@/models/FetchResponse';
import axios, { AxiosRequestConfig } from 'axios';

/* Store the JWT token in local storage */
/* Add type safety for the incoming response separately */
const token = localStorage.getItem('auth_token');

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    Authorization: `Bearer ${token}`,
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
