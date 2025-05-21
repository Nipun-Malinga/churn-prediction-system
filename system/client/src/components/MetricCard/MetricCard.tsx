import { Box, Text, VStack } from '@chakra-ui/react';

const MetricCard = ({ label, value }: { label: string; value: number }) => (
  <Box
    borderWidth='1px'
    borderRadius='2xl'
    padding='4'
    boxShadow='md'
    bg='gray.50'
    textAlign='center'
    width={{ base: '100%', sm: '150px' }}
  >
    <VStack gap={1}>
      <Text fontSize='2xl' fontWeight='bold' color='blue.600'>
        {value}
      </Text>
      <Text fontSize='sm' color='gray.600'>
        {label}
      </Text>
    </VStack>
  </Box>
);

export default MetricCard;
