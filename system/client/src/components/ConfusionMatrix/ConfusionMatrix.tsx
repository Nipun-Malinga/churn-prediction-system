import { Box, BoxProps, SimpleGrid, Text, TextProps, VStack } from '@chakra-ui/react';

interface Props {
  tp: number;
  fp: number;
  tn: number;
  fn: number;
}

const getNormalizedShade = (value: number, max: number, color: string): string => {
  if (max === 0) return `${color}.50`; // Avoid divide by zero

  const percentage = (value / max) * 100;

  if (percentage <= 10) return `${color}.50`;
  if (percentage <= 25) return `${color}.100`;
  if (percentage <= 50) return `${color}.200`;
  if (percentage <= 75) return `${color}.300`;
  if (percentage <= 90) return `${color}.400`;
  return `${color}.500`;
};

const boxStyles = (value: number, max: number, color: string): BoxProps => ({
  alignContent: 'center',
  textAlign: 'center',
  width: '100%',
  height: { base: '5rem', md: '100%' },
  background: getNormalizedShade(value, max, color),
});

const textStyles: TextProps = {
  color: '#000000',
  fontWeight: 'medium',
  fontSize: { base: '1rem' },
};

const ConfusionMatrix = ({ tp, tn, fp, fn }: Props) => {
  const maxValue = Math.max(tp, tn, fp, fn); // For normalization

  return (
    <VStack
      width='100%'
      height='100%'
      background='#fff'
      borderRadius='1rem'
      gap='2.5rem'
      alignItems='flex-start'
      padding={{ base: 5 }}
    >
      <Text fontWeight='bold' fontSize={{ lg: '1.25rem' }}>
        Confusion Matrix
      </Text>
      <SimpleGrid
        columns={2}
        width='100%'
        height='100%'
        justifyItems='center'
        borderRadius='1rem'
        overflow='hidden'
      >
        <Box {...boxStyles(tp, maxValue, 'green')}>
          <Text {...textStyles}>TP: {tp}</Text>
        </Box>
        <Box {...boxStyles(fn, maxValue, 'orange')}>
          <Text {...textStyles}>FN: {fn}</Text>
        </Box>
        <Box {...boxStyles(fp, maxValue, 'red')}>
          <Text {...textStyles}>FP: {fp}</Text>
        </Box>
        <Box {...boxStyles(tn, maxValue, 'teal')}>
          <Text {...textStyles}>TN: {tn}</Text>
        </Box>
      </SimpleGrid>
    </VStack>
  );
};

export default ConfusionMatrix;
