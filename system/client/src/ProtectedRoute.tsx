import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

interface Props {
  children: React.ReactNode;
}

const ProtectedRoute = ({ children }: Props) => {
  const isTokenValid = (): boolean => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return false;

      const decoded: { exp: number } = jwtDecode(token);
      return decoded.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  };

  if (!isTokenValid()) {
    return <Navigate to='/signin' replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
