import { Card, HStack, Span, Text } from '@chakra-ui/react';
import { format } from 'date-fns';
import React from 'react';
import { IconType } from 'react-icons';
import { FaLongArrowAltRight } from 'react-icons/fa';
import { Link } from 'react-router-dom';

interface InfoCardProps {
  title: string;
  subtitle?: string;
  date?: string;
  icon?: IconType;
  color?: '#FEC53D' | '#5893FF';
  link?: string;
  linkLabel?: string;
  linkIcon?: IconType;
}

const InfoCard = ({
  title,
  subtitle,
  date,
  icon,
  color = '#5893FF',
  link,
  linkLabel = 'More Information',
  linkIcon,
}: InfoCardProps) => {
  return (
    <Card.Root width={'100%'} borderRadius={'1rem'} color={'#fff'} background={color}>
      <Card.Body gap={'1'}>
        <HStack justifyContent={'space-between'}>
          <Text fontSize={{ base: '1.5rem', lg: '1.15rem' }} fontWeight='medium'>
            {subtitle}
          </Text>
          {icon && (
            <Span background='#fff' padding={1} borderRadius='5px'>
              {React.createElement(icon, { color: color, size: 35 })}
            </Span>
          )}
        </HStack>

        {title && (
          <Text fontWeight='bold' fontSize={{ lg: '1.5rem' }}>
            {title}
          </Text>
        )}

        {date && (
          <HStack>
            {linkIcon && React.createElement(linkIcon, { size: 20 })}
            <Text fontWeight='medium'>Last Updated: {format(new Date(date), 'yyyy-MM-dd')}</Text>
          </HStack>
        )}

        {link && (
          <HStack justifyContent='flex-end'>
            <Link to={link}>
              <HStack gap='1'>
                <Text>{linkLabel}</Text>
                <FaLongArrowAltRight />
              </HStack>
            </Link>
          </HStack>
        )}
      </Card.Body>
    </Card.Root>
  );
};

export default InfoCard;
