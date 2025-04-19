import { AdvancedModelInfo } from '@/models/ModelDetails';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
} from 'recharts';

/* Build a separate API endpoint 
   for performance difference chart
*/

interface Props {
  currentModelName: string;
  baseModelData: AdvancedModelInfo;
  currentModelData: AdvancedModelInfo;
}

const PerformanceDifferenceChart = ({
  currentModelName,
  baseModelData,
  currentModelData,
}: Props) => {
  const data = [
    {
      subject: 'Accuracy',
      base: baseModelData.accuracy,
      current: currentModelData.accuracy,
    },
    {
      subject: 'Precision',
      base: baseModelData.precision,
      current: currentModelData.accuracy,
    },
    {
      subject: 'Recall',
      base: baseModelData.recall,
      current: currentModelData.accuracy,
    },
    {
      subject: 'F1 Score',
      base: baseModelData.f1_score,
      current: currentModelData.accuracy,
    },
  ];

  return (
    <ResponsiveContainer width='100%' height={400}>
      <RadarChart cx='50%' cy='50%' outerRadius='80%' data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey='subject' />
        <PolarRadiusAxis />
        <Legend />
        <Radar name='Base Model' dataKey='base' stroke='#2ca02c' fill='#2ca02c' fillOpacity={0.6} />
        <Radar
          name={currentModelName}
          dataKey='current'
          stroke='#9467bd'
          fill='#9467bd'
          fillOpacity={0.5}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
};

export default PerformanceDifferenceChart;
