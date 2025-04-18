import { BasicModelInfo } from '@/models/ModelDetails';
import { Card, HStack, Span, Text } from '@chakra-ui/react';
import { FaLongArrowAltRight } from 'react-icons/fa';
import { LuBrainCircuit } from 'react-icons/lu';
import { RxUpdate } from 'react-icons/rx';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
interface Props {
  model: BasicModelInfo;
}

const DetailCard = ({ model }: Props) => {
  const mainColor = model.base_model ? '#FEC53D' : '#5893FF';

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
            {model.name}
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
          Accuracy: {Number((model.accuracy * 100).toFixed(2))}%
        </Text>
        <HStack>
          <RxUpdate size={20} />
          <Text fontWeight={'medium'}>
            Last Updated: {format(new Date(model.updated_date), 'yyyy-MM-dd')}
          </Text>
        </HStack>
        <HStack justifyContent={'flex-end'}>
          <Link to={`/model/${model.name}/${model.id}`}>
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
