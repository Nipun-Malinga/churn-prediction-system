import { Box } from '@chakra-ui/react';
import { PolarAngleAxis, RadialBar, RadialBarChart } from 'recharts';

interface Props {
  value: number;
}

const ProgressIndicator = ({ value }: Props) => {
  const data = [
    {
      name: 'progress',
      value: value,
      fill: '#4AD991',
    },
  ];

  return (
    <Box position={'relative'} width={'7.5rem'} height={'7.5rem'}>
      <RadialBarChart
        width={120}
        height={120}
        cx='50%'
        cy='50%'
        innerRadius='100%'
        outerRadius='100%'
        barSize={10}
        data={data}
        startAngle={90}
        endAngle={450}
      >
        <PolarAngleAxis type='number' domain={[0, 100]} angleAxisId={0} tick={false} />
        <RadialBar background autoReverse dataKey='value' cornerRadius={20} />
      </RadialBarChart>

      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          fontSize: '1.25rem',
          fontWeight: 'bold',
          color: '#004D40',
        }}
      >
        {value}%
      </div>
    </Box>
  );
};

export default ProgressIndicator;
