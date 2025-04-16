import { Provider } from '@/components/ui/provider';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import router from './router';

const queryProvider = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider disableTransitionOnChange={false}>
      <QueryClientProvider client={queryProvider}>
        <RouterProvider router={router} />
        <ReactQueryDevtools />
      </QueryClientProvider>
    </Provider>
  </StrictMode>
);
