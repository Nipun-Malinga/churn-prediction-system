import { FetchListResponse, FetchResponse } from '@/models/FetchResponse';
import axios, { AxiosRequestConfig } from 'axios';

/* Store the JWT token in local storage */
const token =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDM5NjU3MywianRpIjoiMzdjMWRhM2ItMDkxYy00MjkxLWJjNTktNGExN2ZiNWYwNzg2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcInVzZXJfaWQ6XCI6IDF9IiwibmJmIjoxNzQ0Mzk2NTczLCJjc3JmIjoiZWE5Y2Q2NDMtMjNlMS00MmE1LWJiODEtODE2NjQ4YzY0MDAzIiwiZXhwIjoxNzQ2OTg4NTczLCJlbWFpbCI6Im5pcHVubWFsaW5nYUBnbWFpbC5jb20ifQ.STbFZ21cRlSun8QrpHOT_B4vYX5mMm4fixclDVCkKHI';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
class APIClient<T> {
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
    const resp = await axiosInstance.post<FetchResponse<T>>(this.endpoint, data, requestConfig);
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
