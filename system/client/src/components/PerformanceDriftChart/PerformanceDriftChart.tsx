import { PerformanceDriftHistory } from '@/models/ModelPerformance';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { format } from 'date-fns';

interface Props {
  performanceDriftHistory: PerformanceDriftHistory[];
}

const PerformanceDriftChart = ({ performanceDriftHistory }: Props) => {
  console.log(performanceDriftHistory);
  return (
    <ResponsiveContainer width='100%' height={400}>
      <BarChart
        width={500}
        height={300}
        data={performanceDriftHistory}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray='3 3' />
        <XAxis dataKey='date' tickFormatter={(v) => `${format(new Date(v), 'yyyy-MM-dd')}`} />
        <YAxis />
        <Tooltip />
        <Legend />
        <ReferenceLine y={0} stroke='#000' />
        <Bar width={10} dataKey='accuracy_drift' fill='#4e79a7' /> 
        <Bar width={10} dataKey='precision_drift' fill='#f28e2b' /> 
        <Bar width={10} dataKey='recall_drift' fill='#e15759' />
        <Bar width={10} dataKey='f1_score_drift' fill='#76b7b2' /> 
      </BarChart>
    </ResponsiveContainer>
  );
};

export default PerformanceDriftChart;
