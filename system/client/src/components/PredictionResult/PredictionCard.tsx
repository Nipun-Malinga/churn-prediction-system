import { PredictionResponse } from '@/models/Prediction';
import { Box} from '@chakra-ui/react';

interface props {
  predictionResponse: PredictionResponse;
}

const PredictionCard = ({ predictionResponse }: props) => {
  return <Box>{predictionResponse.Prediction}</Box>;
};

export default PredictionCard;
