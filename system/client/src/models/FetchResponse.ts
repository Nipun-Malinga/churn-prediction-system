interface BaseResponse {
  status: string;
  message: string;
}

interface FetchListResponse<T> extends BaseResponse {
  data: T[];
}

interface FetchResponse<T> extends BaseResponse {
  data: T;
}

export type { FetchListResponse, FetchResponse };
