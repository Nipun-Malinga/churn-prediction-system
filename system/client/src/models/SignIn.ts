interface SignIn {
  email: string;
  password: string;
}

interface SignInResponse {
  auth_token: string;
}

export type { SignIn, SignInResponse };
