import NavLink from '@/models/NavLink';
import { Button, ButtonProps, Text } from '@chakra-ui/react';
import { useLocation, useNavigate } from 'react-router-dom';

interface Props {
  children: NavLink;
}

const NavButton = ({ children }: Props) => {
  const location = useLocation();
  const navigate = useNavigate();

  const goTo = (endpoint: string) => {
    navigate(endpoint);
  };

  const isLocation = location.pathname == children.navigateTo;
  const buttonColors: ButtonProps = {
    background: isLocation ? '#4880FF' : '#fff',
    color: isLocation ? '#fff' : '#000',
  };

  return (
    <>
      <Button
        {...buttonColors}
        width={{
          base: '12.5rem',
        }}
        height={{
          base: '3rem',
        }}
        borderRadius={6}
        justifyContent={'flex-start'}
        gap={{
          base: '1rem',
        }}
        _hover={{
          background: '#4880EE',
          color: '#fff',
        }}
        onClick={() => {
          goTo(children.navigateTo);
        }}
      >
        <children.icon />
        <Text>{children.name}</Text>
      </Button>
    </>
  );
};

export default NavButton;
