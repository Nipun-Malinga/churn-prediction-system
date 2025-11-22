import { Box, BoxProps, SimpleGrid, Text, TextProps, VStack } from '@chakra-ui/react';

interface Props {
  tp: number;
  fp: number;
  tn: number;
  fn: number;
}

const getNormalizedShade = (value: number, max: number, color: string): string => {
  if (max === 0) return `${color}.50`;

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
  height: { base: '6rem', md: '100%' },
  background: getNormalizedShade(value, max, color),
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  _hover: {
    transform: 'scale(1.02)',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    zIndex: 1,
  },
  cursor: 'default',
  position: 'relative',
});

const textStyles: TextProps = {
  color: 'gray.900',
  fontWeight: '600',
  fontSize: { base: '1.125rem', md: '1.25rem' },
  letterSpacing: '-0.01em',
};

const ConfusionMatrix = ({ tp, tn, fp, fn }: Props) => {
  const maxValue = Math.max(tp, tn, fp, fn);

  return (
    <VStack
      width='100%'
      height='100%'
      background='#fff'
      borderRadius='0.75rem'
      gap='1.5rem'
      alignItems='flex-start'
      padding={{ base: '1.25rem', md: '1.5rem', lg: '2rem' }}
      boxShadow='0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)'
      border='1px solid'
      borderColor='gray.100'
    >
      <Text 
        fontWeight='600' 
        fontSize={{ base: '1.125rem', lg: '1.25rem' }}
        color='gray.800'
        letterSpacing='-0.01em'
      >
        Confusion Matrix
      </Text>
      <SimpleGrid
        columns={2}
        width='100%'
        height='100%'
        gap='0.5rem'
        justifyItems='center'
        borderRadius='0.75rem'
        overflow='hidden'
        padding='0.25rem'
      >
        <Box {...boxStyles(tp, maxValue, 'green')} borderRadius='0.5rem'>
          <VStack gap='0.25rem'>
            <Text 
              fontSize={{ base: '0.75rem', md: '0.875rem' }}
              fontWeight='500'
              color='gray.700'
              textTransform='uppercase'
              letterSpacing='0.05em'
            >
              True Positive
            </Text>
            <Text {...textStyles}>{tp}</Text>
          </VStack>
        </Box>
        <Box {...boxStyles(fn, maxValue, 'orange')} borderRadius='0.5rem'>
          <VStack gap='0.25rem'>
            <Text 
              fontSize={{ base: '0.75rem', md: '0.875rem' }}
              fontWeight='500'
              color='gray.700'
              textTransform='uppercase'
              letterSpacing='0.05em'
            >
              False Negative
            </Text>
            <Text {...textStyles}>{fn}</Text>
          </VStack>
        </Box>
        <Box {...boxStyles(fp, maxValue, 'red')} borderRadius='0.5rem'>
          <VStack gap='0.25rem'>
            <Text 
              fontSize={{ base: '0.75rem', md: '0.875rem' }}
              fontWeight='500'
              color='gray.700'
              textTransform='uppercase'
              letterSpacing='0.05em'
            >
              False Positive
            </Text>
            <Text {...textStyles}>{fp}</Text>
          </VStack>
        </Box>
        <Box {...boxStyles(tn, maxValue, 'teal')} borderRadius='0.5rem'>
          <VStack gap='0.25rem'>
            <Text 
              fontSize={{ base: '0.75rem', md: '0.875rem' }}
              fontWeight='500'
              color='gray.700'
              textTransform='uppercase'
              letterSpacing='0.05em'
            >
              True Negative
            </Text>
            <Text {...textStyles}>{tn}</Text>
          </VStack>
        </Box>
      </SimpleGrid>
    </VStack>
  );
};

export default ConfusionMatrix;