import navLinks from '@/data/navLinks';
import { Spacer, VStack } from '@chakra-ui/react';
import NavButton from '../NavButton';
import { useNavigate } from 'react-router-dom';

const Sidebar = () => {
  const navigate = useNavigate();

  return (
    <VStack background='white' height='100%' padding={5} position={'fixed'}>
      {navLinks
        .filter((link) => link.isMain)
        .map((link, id) => (
          <NavButton key={id} children={link} />
        ))}

      <Spacer />

      {navLinks
        .filter((link) => !link.isMain)
        .map((link, id) => (
          <NavButton
            key={id}
            children={link}
            onClick={() => {
              localStorage.removeItem('auth_token');
              navigate('/signIn');
            }}
          />
        ))}
    </VStack>
  );
};

export default Sidebar;
