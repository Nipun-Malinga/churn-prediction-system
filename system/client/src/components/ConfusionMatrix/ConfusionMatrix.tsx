import { Box, BoxProps, SimpleGrid, Text, TextProps, VStack } from '@chakra-ui/react';

interface Props {
  tp: number;
  fp: number;
  tn: number;
  fn: number;
}

const boxStyles = (threshold: number) => {
  const styles: BoxProps = {
    alignContent: 'center',
    textAlign: 'center',
    width: '100%',
    height: { base: '5rem', md: '100%' },
    /* Implement logic to change color based on the confusion matrix data */
    background:
      threshold >= 0 && threshold <= 20
        ? 'green.100'
        : threshold >= 21 && threshold <= 60
        ? 'green.200'
        : threshold >= 61 && threshold <= 90
        ? 'green.300'
        : 'green.500',
  };

  return styles;
};

const textStyles: TextProps = {
  color: '#000000',
  fontWeight: 'medium',
  fontSize: { base: '1rem' },
};

const ConfusionMatrix = ({ tp, tn, fp, fn }: Props) => {
  return (
    <VStack
      width={'100%'}
      height={'100%'}
      background={'#fff'}
      borderRadius={'1rem'}
      gap={'2.5rem'}
      alignItems={'flex-start'}
      padding={{
        base: 5,
      }}
    >
      <Text
        fontWeight={'bold'}
        fontSize={{
          lg: '1.25rem',
        }}
      >
        Confusion Matrix
      </Text>
      <SimpleGrid
        columns={2}
        width={'100%'}
        height={'100%'}
        justifyItems={'center'}
        borderRadius={'1rem'}
        overflow={'hidden'}
      >
        <Box {...boxStyles(tp)}>
          <Text {...textStyles}>TP: {tp}</Text>
        </Box>
        <Box {...boxStyles(fn)}>
          <Text {...textStyles}>FN: {fn}</Text>
        </Box>

        <Box {...boxStyles(fp)}>
          <Text {...textStyles}>FP: {fp}</Text>
        </Box>
        <Box {...boxStyles(tn)}>
          <Text {...textStyles}>TN: {tn}</Text>
        </Box>
      </SimpleGrid>
    </VStack>
  );
};

export default ConfusionMatrix;
