import { PredictionResponse } from '@/models/Prediction';
import { Box, Heading, HStack, Text, VStack } from '@chakra-ui/react';

interface Props {
  predictionResponse: PredictionResponse;
}

const PredictionCard = ({ predictionResponse }: Props) => {
  const isChurn = predictionResponse.Prediction === 1;
  const probability = isChurn
    ? predictionResponse.Probability[0]
    : predictionResponse.Probability[0];

  return (
    <VStack  borderRadius='xl' align='center' width={'100%'}>
      <Box
        padding={'1rem'}
        border='1px solid'
        width={'20rem'}
        borderColor='gray.200'
        borderRadius={'1rem'}
      >
        <Heading size='md'>Prediction Results</Heading>
        <HStack width={'100%'} justifyContent={'space-between'}>
          <Text fontWeight='semibold'>Churn:</Text>
          <Text>{isChurn ? 'Yes' : 'No'}</Text>
        </HStack>
        <HStack width={'100%'} justifyContent={'space-between'}>
          <Text fontWeight='semibold'>Probability:</Text>
          <Text>{(probability * 100).toFixed(2)}%</Text>
        </HStack>
      </Box>
    </VStack>
  );
};

export default PredictionCard;
