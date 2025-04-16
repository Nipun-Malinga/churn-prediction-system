import { Card, HStack, Text } from '@chakra-ui/react';
import ProgressIndicator from '../ProgressIndicator';

interface Props {
  value: number;
  title: string;
}

const PerformanceCard = ({ value, title }: Props) => {
  return (
    <Card.Root width={'100%'} borderRadius={'1rem'}>
      <Card.Body gap={5}>
        <Text
          fontSize={{
            base: '2rem',
            lg: '1rem',
          }}
          fontWeight={'medium'}
        >
          {title}
        </Text>
        <HStack justifyContent={'center'}>
          <ProgressIndicator value={value} />
        </HStack>
      </Card.Body>
    </Card.Root>
  );
};

export default PerformanceCard;
