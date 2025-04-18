import { create } from 'zustand';

interface SelectedMode {
  selectedMode: string;
  setSelectedMode: (mode: string) => void;
}

const useSelectedModeStore = create<SelectedMode>((set) => ({
  selectedMode: 'accuracy',
  setSelectedMode: (mode: string) => {
    set({ selectedMode: mode });
  },
}));

export default useSelectedModeStore;
