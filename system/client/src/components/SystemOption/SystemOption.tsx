import { Box, Button, HoverCard, Portal, Span, VStack } from '@chakra-ui/react';
import React, { useState } from 'react';
import { IconType } from 'react-icons';

interface Props {
  icon?: IconType;
  description: string;
  disable?: boolean;
  onClick?: () => void;
}

const SystemOption = ({ icon, description, disable, onClick }: Props) => {
  const [open, setOpen] = useState(false);

  return (
    <HoverCard.Root size='sm' open={open} onOpenChange={(e) => setOpen(e.open)}>
      <HoverCard.Trigger asChild>
        <Button
          width={{
            base: '7.5rem',
            md: '5rem',
          }}
          height={{
            base: '2.5rem',
          }}
          background={'#ffffff'}
          color={'#000'}
          marginX={1}
          onClick={() => onClick && onClick()}
          _hover={{
            background: '#4880FF',
            color: '#fff',
          }}
          disabled={disable}
        >
          <VStack>
            <Span padding={2}>{icon && React.createElement(icon)}</Span>
          </VStack>
        </Button>
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
