import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import Configuration from './pages/Configuration';
import DatasetInfo from './pages/DatasetInfo';
import Home from './pages/Home';
import Model from './pages/Model';
import NotFound from './pages/NotFound';
import Prediction from './pages/Prediction';
import SignIn from './pages/SignIn';
import ProtectedRoute from './ProtectedRoute';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: (
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        ),
      },
      {
        path: '/dashboard',
        element: (
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        ),
      },
      {
        path: 'dashboard/model/:model/:id',
        element: (
          <ProtectedRoute>
            <Model />
          </ProtectedRoute>
        ),
      },
      {
        path: '/predict',
        element: (
          <ProtectedRoute>
            <Prediction />
          </ProtectedRoute>
        ),
      },
      {
        path: '/dataset',
        element: (
          <ProtectedRoute>
            <DatasetInfo />
          </ProtectedRoute>
        ),
      },
      {
        path: '/config',
        element: (
          <ProtectedRoute>
            <Configuration />
          </ProtectedRoute>
        ),
      },
    ],
  },
  { path: '/signin', element: <SignIn /> },
  {
    path: '*',
    element: <NotFound />,
  },
]);

export default router;
