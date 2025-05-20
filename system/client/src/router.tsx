import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import Configuration from './pages/Configuration';
import DatasetInfo from './pages/DatasetInfo';
import Home from './pages/Home';
import Model from './pages/Model';
import NotFound from './pages/NotFound';
import SignIn from './pages/SignIn';
import Prediction from './pages/Prediction';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: '/dashboard', element: <Home /> },
      {
        path: 'dashboard/model/:model/:id',
        element: <Model />,
      },
      { path: '/signin', element: <SignIn /> },
      { path: '/model/:model/:id', element: <Model /> },
      { path: '/predict', element: <Prediction /> },
      { path: '/dataset', element: <DatasetInfo /> },
      { path: '/config', element: <Configuration /> },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
]);

export default router;
