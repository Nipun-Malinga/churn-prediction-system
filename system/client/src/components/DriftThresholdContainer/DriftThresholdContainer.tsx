import { VStack } from '@chakra-ui/react';
import DriftDetectorForm from '../DriftDetectorForm';
import DriftThresholdCards from '../DriftThresholdCards';

const DriftThresholdContainer = () => {
  return (
    <VStack width={'100%'}>
      <DriftThresholdCards />
      <DriftDetectorForm />
    </VStack>
  );
};

export default DriftThresholdContainer;
