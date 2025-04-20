import NavLink from '@/models/NavLink';
import { IoSettings } from 'react-icons/io5';
import { MdDashboard } from 'react-icons/md';
import { BsClipboardDataFill } from 'react-icons/bs';
import { RiLogoutBoxRLine } from 'react-icons/ri';

const navLinks: NavLink[] = [
  { name: 'Dashboard', navigateTo: '/', icon: MdDashboard, isMain: true },
  { name: 'Dataset', navigateTo: '/dataset', icon: BsClipboardDataFill, isMain: true },
  { name: 'Configuration', navigateTo: '/config', icon: IoSettings, isMain: true },
  { name: 'Logout', navigateTo: '/logout', icon: RiLogoutBoxRLine, isMain: false },
];

export default navLinks;
