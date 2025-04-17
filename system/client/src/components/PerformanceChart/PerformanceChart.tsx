import PerformanceDataPoint from '@/models/ModelPerformance';
import { format } from 'date-fns';
import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

interface Props {
  performanceHistory: PerformanceDataPoint[];
}

const PerformanceChart = ({ performanceHistory }: Props) => {
  return (
    <ResponsiveContainer width='100%' height={400}>
      <ComposedChart data={performanceHistory}>
        <CartesianGrid strokeDasharray='3 3' />
        <XAxis
          dataKey='updated_date'
          tickFormatter={(v) => `${format(new Date(v), 'yyyy-MM-dd')}`}
        />
        <YAxis tickFormatter={(v) => `${v}%`} />
        <Tooltip formatter={(v: number) => `${v}%`} />

        <Area
          type='monotone'
          dataKey='data'
          stroke='transparent'
          fill='#4379EE'
          fillOpacity={0.2}
        />
        <Line
          type='monotone'
          dataKey='data'
          stroke='#007bff'
          strokeWidth={3}
          dot={{ r: 4, stroke: '#007bff', strokeWidth: 2, fill: '#007bff' }}
          activeDot={{ r: 6 }}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
};

export default PerformanceChart;
