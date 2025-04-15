import { navLinks } from '@/data';
import { Spacer, VStack } from '@chakra-ui/react';
import NavButton from '../NavButton';

const Sidebar = () => {
  return (
    <VStack background='white' height='100vh' padding={5}>
      {navLinks
        .filter((link) => link.isMain)
        .map((link, id) => (
          <NavButton key={id} children={link} />
        ))}

      <Spacer />

      {navLinks
        .filter((link) => !link.isMain)
        .map((link, id) => (
          <NavButton key={id} children={link} />
        ))}
    </VStack>
  );
};

export default Sidebar;
