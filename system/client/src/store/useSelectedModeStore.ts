import { create } from 'zustand';

interface SelectedModeState {
  selectedMode: string;
  setSelectedMode: (mode: string) => void;
}

const useSelectedModeStore = create<SelectedModeState>((set) => ({
  selectedMode: 'accuracy',
  setSelectedMode: (data) => {
    set({ selectedMode: data });
  },
}));

export default useSelectedModeStore;
