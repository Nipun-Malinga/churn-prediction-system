import PredictionForm from '@/components/PredictionForm';
import { Text } from '@chakra-ui/react';

const Prediction = () => {
  return (
    <>
      <Text
        fontSize={{
          base: '1rem',
          lg: '1.5rem',
        }}
        fontWeight={'medium'}
      >
        Prediction
      </Text>
      <PredictionForm />
    </>
  );
};

export default Prediction;
