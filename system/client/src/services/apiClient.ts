import axios, { AxiosRequestConfig } from 'axios';
import { FetchResponse } from '@/models';
import env from 'react-dotenv';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    Authorization:
      'Bearer ' +
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDM5NjU3MywianRpIjoiMzdjMWRhM2ItMDkxYy00MjkxLWJjNTktNGExN2ZiNWYwNzg2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcInVzZXJfaWQ6XCI6IDF9IiwibmJmIjoxNzQ0Mzk2NTczLCJjc3JmIjoiZWE5Y2Q2NDMtMjNlMS00MmE1LWJiODEtODE2NjQ4YzY0MDAzIiwiZXhwIjoxNzQ2OTg4NTczLCJlbWFpbCI6Im5pcHVubWFsaW5nYUBnbWFpbC5jb20ifQ.STbFZ21cRlSun8QrpHOT_B4vYX5mMm4fixclDVCkKHI',
  },
});
class APIClient<T> {
  private endpoint;

  constructor(endpoint: string) {
    this.endpoint = endpoint;
  }

  get = async <K>(id: string | number) => {
    const resp = await axiosInstance.get<K>(this.endpoint + '/' + id);
    return resp.data;
  };

  getAll = async (requestConfig?: AxiosRequestConfig) => {
    const resp = await axiosInstance
      .get<FetchResponse<T>>(this.endpoint, { ...requestConfig });
    return resp.data;
  };

  post = async (data: T) => {
    const resp = await axiosInstance.post<FetchResponse<T>>(this.endpoint, data);
    return resp.data;
  };
}

export default APIClient;
