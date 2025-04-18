import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import Configuration from './pages/Configuration';
import Home from './pages/Home';
import Model from './pages/Model';
import SignIn from './pages/SignIn';
import NotFound from './pages/NotFound';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: '/signin', element: <SignIn /> },
      { path: '/model/:model/:id', element: <Model /> },
      { path: '/config', element: <Configuration /> },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
]);

export default router;
