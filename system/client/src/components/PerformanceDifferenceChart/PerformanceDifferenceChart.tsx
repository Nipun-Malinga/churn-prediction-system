import { AdvancedModelInfo } from '@/models/ModelDetails';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import ChartContainer from '../ChartContainer';

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
      current: currentModelData.precision,
    },
    {
      subject: 'Recall',
      base: baseModelData.recall,
      current: currentModelData.recall,
    },
    {
      subject: 'F1 Score',
      base: baseModelData.f1_score,
      current: currentModelData.f1_score,
    },
  ];

  return (
    <ChartContainer>
      <ResponsiveContainer width='100%' height='100%'>
        <RadarChart cx='50%' cy='50%' outerRadius='75%' data={data}>
          <PolarGrid 
            stroke='#e5e7eb'
            strokeWidth={1}
          />
          <PolarAngleAxis 
            dataKey='subject'
            tick={{ 
              fill: '#374151', 
              fontSize: 14, 
              fontWeight: 500 
            }}
          />
          <PolarRadiusAxis 
            angle={90}
            tick={{ 
              fill: '#6b7280', 
              fontSize: 12 
            }}
            stroke='#d1d5db'
          />
          <Legend 
            wrapperStyle={{
              paddingTop: '1rem',
              fontSize: '0.875rem',
              fontWeight: 500,
            }}
            iconType='circle'
          />
          <Radar 
            name='Base Model' 
            dataKey='base' 
            stroke='#10b981' 
            fill='#10b981' 
            fillOpacity={0.25}
            strokeWidth={2}
            dot={{ 
              fill: '#10b981', 
              r: 4,
              strokeWidth: 2,
              stroke: '#fff'
            }}
            activeDot={{ 
              r: 6,
              strokeWidth: 2
            }}
          />
          <Radar
            name={currentModelName}
            dataKey='current'
            stroke='#8b5cf6'
            fill='#8b5cf6'
            fillOpacity={0.25}
            strokeWidth={2}
            dot={{ 
              fill: '#8b5cf6', 
              r: 4,
              strokeWidth: 2,
              stroke: '#fff'
            }}
            activeDot={{ 
              r: 6,
              strokeWidth: 2
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
};

export default PerformanceDifferenceChart;