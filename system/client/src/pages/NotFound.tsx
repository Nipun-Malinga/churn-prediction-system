import { Button, HStack, Image, Text, VStack } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <HStack height={'100vh'} width={'100%'} background={'#4880FF'} justifyContent={'center'}>
      <VStack
        width={{
          base: '90%',
          md: '50%',
        }}
        height={'75%'}
        background={'#FFFFFF'}
        borderRadius={'1rem'}
        justifyContent={'center'}
        gap={'2.5rem'}
        padding={{
          base: 1,
        }}
      >
        <Image src={'../../public/404.svg'} />
        <Text
          fontSize={{
            base: '1.25rem',
            md: '1.75rem',
          }}
          fontWeight={'bold'}
        >
          Looks Like you've got lost
        </Text>
        <Button
          background={'#4880FF'}
          width={'40%'}
          onClick={() => {
            navigate('/');
          }}
        >
          Back to Dashboard
        </Button>
      </VStack>
    </HStack>
  );
};

export default NotFound;
