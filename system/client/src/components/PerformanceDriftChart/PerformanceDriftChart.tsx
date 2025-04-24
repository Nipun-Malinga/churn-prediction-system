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
import ChartContainer from '../ChartContainer';

interface Props {
  performanceDriftHistory: PerformanceDriftHistory[];
}

const PerformanceDriftChart = ({ performanceDriftHistory }: Props) => {
  console.log(performanceDriftHistory);
  return (
    <ChartContainer>
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
        <Bar width={10} name={'Accuracy Drift'} dataKey='accuracy_drift' fill='#4e79a7' />
        <Bar width={10} name={'Precision Drift'} dataKey='precision_drift' fill='#f28e2b' />
        <Bar width={10} name={'Recall Drift'} dataKey='recall_drift' fill='#e15759' />
        <Bar width={10} name={'F1 Score Drift'} dataKey='f1_score_drift' fill='#76b7b2' />
      </BarChart>
    </ChartContainer>
  );
};

export default PerformanceDriftChart;
