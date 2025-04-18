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
          fontWeight={'medium'}
          fontSize={{
            lg: '1.25rem',
          }}
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
