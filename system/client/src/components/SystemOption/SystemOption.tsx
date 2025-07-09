import {
  Box,
  Button,
  HoverCard,
  HStack,
  Icon,
  Portal,
  Span,
} from '@chakra-ui/react';
import React, { useState } from 'react';
import { IconType } from 'react-icons';

interface Props {
  icon?: IconType;
  description: string;
  disable?: boolean;
}

const SystemOption = ({ icon, description, disable }: Props) => {
  const [open, setOpen] = useState(false);

  return (
    <HoverCard.Root size='sm' open={open} onOpenChange={(e) => setOpen(e.open)}>
      <HoverCard.Trigger asChild>
        <HStack
          width={{
            base: '7.5rem',
            md: '5rem',
          }}
          height={{
            base: '2.5rem',
          }}
          transition='0.15s all ease-in-out'
          _hover={{
            background: '#4880FF',
            color: '#fff',
          }}
          background='#ffffff'
          color='#000'
          marginX={1}
          borderRadius='5px'
          textAlign='center'
          justifyContent='center'
          cursor='pointer'
        >
          <Icon size={'md'}>{icon && React.createElement(icon)}</Icon>
        </HStack>
      </HoverCard.Trigger>
      <Portal>
        <HoverCard.Positioner>
          <HoverCard.Content maxWidth='240px'>
            <HoverCard.Arrow />
            <Box>{description}</Box>
          </HoverCard.Content>
        </HoverCard.Positioner>
      </Portal>
    </HoverCard.Root>
  );
};

export default SystemOption;
