import NavLink from '@/models/NavLink';
import { IoIosSpeedometer } from 'react-icons/io';
import { IoSettings } from 'react-icons/io5';
import { MdDashboard } from 'react-icons/md';
import { RiLogoutBoxRLine } from 'react-icons/ri';

const navLinks: NavLink[] = [
  { name: 'Dashboard', navigateTo: '/', icon: MdDashboard, isMain: true },
  { name: 'Model', navigateTo: '/model/1', icon: IoIosSpeedometer, isMain: true },
  { name: 'Configuration', navigateTo: '/config', icon: IoSettings, isMain: true },
  { name: 'Logout', navigateTo: '/logout', icon: RiLogoutBoxRLine, isMain: false },
];

export default navLinks;
