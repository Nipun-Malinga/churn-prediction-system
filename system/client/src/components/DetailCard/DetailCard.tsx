import { Model } from '@/models';
import { Card, HStack, Span, Text } from '@chakra-ui/react';
import { format } from 'date-fns';
import { FaLongArrowAltRight } from 'react-icons/fa';
import { LuBrainCircuit } from 'react-icons/lu';
import { RxUpdate } from 'react-icons/rx';
import { Link } from 'react-router-dom';

/*TODO: Use Real Data From Server */
const isoDate = '2025-04-13T05:32:50.435610';
const formattedDate = format(new Date(isoDate), 'yyyy-MM-dd HH:mm:ss');

interface Props {
  children: Model;
}

const DetailCard = ({ children }: Props) => {
  const mainColor = children.base_model ? '#FEC53D' : '#5893FF';

  return (
    <Card.Root width={'100%'} borderRadius={'1rem'} color={'#fff'} background={mainColor}>
      <Card.Body gap={'1'}>
        <HStack justifyContent={'space-between'}>
          <Text
            fontSize={{
              base: '1.5rem',
              lg: '1.15rem',
            }}
            fontWeight={'medium'}
          >
            {children.name}
          </Text>
          <Span background={'#fff'} padding={1} borderRadius={'5px'}>
            <LuBrainCircuit size={35} color={mainColor} />
          </Span>
        </HStack>
        <Text
          fontWeight={'bold'}
          fontSize={{
            lg: '1.5rem',
          }}
        >

          {/*TODO: Implement logic to change the font color base on the accuracy*/}

          Accuracy: {91}%
        </Text>
        <HStack>
          <RxUpdate size={20} />
          <Text fontWeight={'medium'}>Last Updated: {formattedDate}</Text>
        </HStack>
        <HStack justifyContent={'flex-end'}>
          <Link to={`/model/${children.id}`}>
            <HStack gap={'1'}>
              <Text>More Information</Text>
              <FaLongArrowAltRight />
            </HStack>
          </Link>
        </HStack>
      </Card.Body>
    </Card.Root>
  );
};

export default DetailCard;
