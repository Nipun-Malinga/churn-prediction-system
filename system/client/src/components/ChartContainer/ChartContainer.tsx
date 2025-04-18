import useSelectedModeStore from '@/store/useSelectedModeStore';
import { HStack, NativeSelect, Text, VStack } from '@chakra-ui/react';
import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
  title?: string;
}

const ChartContainer = ({ children, title }: Props) => {
  /*
    TODO: 
      * Implement Loading Skeleton and Error Massage Components
  */

  const { setSelectedMode } = useSelectedModeStore();

  return (
    <VStack
      width={'100%'}
      gap={'2.5rem'}
      background={'#ffffff'}
      borderRadius={'1rem'}
      padding={{
        base: 5,
      }}
    >
      <HStack width={'100%'} justifyContent={'space-between'}>
        <Text
          fontWeight={'bold'}
          fontSize={{
            lg: '1.25rem',
          }}
        >
          {title ? title : 'Performance History'}
        </Text>
        <NativeSelect.Root
          width={{
            base: '7.5rem',
            lg: '10rem',
          }}
        >
          <NativeSelect.Field onChange={(e) => setSelectedMode(e.target.value)}>
            <option value='accuracy'>Accuracy</option>
            <option value='precision'>Precision</option>
            <option value='recall'>Recall</option>
            <option value='f1_score'>F1 Score</option>
          </NativeSelect.Field>
          <NativeSelect.Indicator />
        </NativeSelect.Root>
      </HStack>
      {children}
    </VStack>
  );
};

export default ChartContainer;
