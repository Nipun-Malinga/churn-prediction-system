import { SignIn, SignInResponse } from '@/models/SignIn';
import APIClient from '@/services/apiClient';
import { useMutation } from '@tanstack/react-query';

const useLogin = () => {
  const apiClient = new APIClient<SignIn, SignInResponse>('/v1/users/login');

  return useMutation({
    mutationFn: (data: SignIn) => apiClient.post(undefined, data),
    onError: (err) => {
      console.log(err);
    },
  });
};

export default useLogin;
