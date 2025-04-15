import { Provider } from '@/components/ui/provider';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import router from './router';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider disableTransitionOnChange={false}>
      <RouterProvider router={router}/>
    </Provider>
  </StrictMode>
);
