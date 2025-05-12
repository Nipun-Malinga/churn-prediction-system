import NavLink from '@/models/NavLink';
import { BsClipboardDataFill } from 'react-icons/bs';
import { IoSettings } from 'react-icons/io5';
import { MdDashboard, MdTrendingUp } from 'react-icons/md';
import { RiLogoutBoxRLine } from 'react-icons/ri';

const navLinks: NavLink[] = [
  { name: 'Dashboard', navigateTo: '/', icon: MdDashboard, isMain: true },
  { name: 'Prediction', navigateTo: '/predict', icon: MdTrendingUp, isMain: true },
  { name: 'Dataset', navigateTo: '/dataset', icon: BsClipboardDataFill, isMain: true },
  { name: 'Configuration', navigateTo: '/config', icon: IoSettings, isMain: true },
  { name: 'Logout', navigateTo: '/logout', icon: RiLogoutBoxRLine, isMain: false },
];

export default navLinks;
