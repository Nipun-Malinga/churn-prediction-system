import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import Home from './pages/Home';
import SignIn from './pages/SignIn';
import Model from './pages/Model';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: '/signin', element: <SignIn /> },
      { path: '/model/:id', element: <Model /> },
    ],
  },
]);

export default router;
