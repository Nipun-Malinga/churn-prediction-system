import { ClassImbalance } from '@/models/DatasetInfo';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  YAxis,
} from 'recharts';

interface Props {
  classImbalance: ClassImbalance;
}

const DataImbalanceChart = ({ classImbalance }: Props) => {
  console.log(classImbalance.churned);

  const data = [
    {
      name: 'Class Imbalance',
      churned: classImbalance.churned,
      notChurned: classImbalance.not_churned,
      amt: 2400,
    },
  ];

  return (
    <ResponsiveContainer width='100%' height={400}>
      <BarChart
        width={500}
        height={300}
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray='3 3' />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey='churned' fill='#8884d8' />
        <Bar dataKey='notChurned' fill='#82ca9d' />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default DataImbalanceChart;
