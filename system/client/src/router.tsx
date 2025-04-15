import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import Configuration from './pages/Configuration';
import Home from './pages/Home';
import Model from './pages/Model';
import SignIn from './pages/SignIn';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: '/signin', element: <SignIn /> },
      { path: '/model/:id', element: <Model /> },
      { path: '/config', element: <Configuration /> },
    ],
  },
]);

export default router;
