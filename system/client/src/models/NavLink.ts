import { IconType } from 'react-icons';

interface NavLink {
  name: string;
  navigateTo: string;
  icon: IconType;
  isMain?: boolean;
}

export default NavLink;