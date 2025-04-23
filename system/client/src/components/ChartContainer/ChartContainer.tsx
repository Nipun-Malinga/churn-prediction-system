import { ReactElement } from 'react';
import { ResponsiveContainer } from 'recharts';

interface Props {
  children: ReactElement;
}

const ChartContainer = ({ children }: Props) => {
  return (
    <ResponsiveContainer width={'100%'} height={325}>
      {children}
    </ResponsiveContainer>
  );
};

export default ChartContainer;
