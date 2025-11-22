import { Card, HStack, Text } from '@chakra-ui/react';
import ProgressIndicator from '../ProgressIndicator';

interface Props {
  value: number;
  title: string;
}

const PerformanceCard = ({ value, title }: Props) => {
  return (
    <Card.Root 
      width={'100%'} 
      borderRadius={'0.75rem'}
      boxShadow={'0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)'}
      border={'1px solid'}
      borderColor={'gray.100'}
      transition={'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'}
      _hover={{
        transform: 'translateY(-2px)',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        borderColor: 'gray.200',
      }}
      bg={'white'}
    >
      <Card.Body 
        gap={'1.25rem'}
        padding={{
          base: '1.25rem',
          md: '1.5rem',
        }}
      >
        <Text
          fontWeight={'600'}
          fontSize={{
            base: '1rem',
            lg: '1.125rem',
          }}
          color={'gray.700'}
          letterSpacing={'-0.01em'}
        >
          {title}
        </Text>
        <HStack justifyContent={'center'} py={'0.5rem'}>
          <ProgressIndicator value={value} />
        </HStack>
      </Card.Body>
    </Card.Root>
  );
};

export default PerformanceCard;