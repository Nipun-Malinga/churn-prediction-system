import { Box, Text, VStack } from '@chakra-ui/react';

const MetricCard = ({ label, value }: { label: string; value: number }) => (
  <Box
    borderWidth='1px'
    borderRadius='0.75rem'
    padding={{ base: '1rem', md: '1.25rem' }}
    boxShadow='0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)'
    bg='white'
    textAlign='center'
    width={{ base: '100%', sm: '150px' }}
    borderColor='gray.100'
  >
    <VStack gap='0.5rem'>
      <Text 
        fontSize={{ base: '1.75rem', md: '2rem' }} 
        fontWeight='700' 
        color='#5893FF'
        lineHeight='1'
        letterSpacing='-0.02em'
      >
        {value}
        <Text 
          as='span' 
          fontSize={{ base: '1.25rem', md: '1.5rem' }}
          fontWeight='600'
          color='gray.600'
          ml='0.125rem'
        >
          %
        </Text>
      </Text>
      <Text 
        fontSize='0.875rem' 
        color='gray.600'
        fontWeight='500'
        letterSpacing='0.01em'
      >
        {label}
      </Text>
    </VStack>
  </Box>
);

export default MetricCard;