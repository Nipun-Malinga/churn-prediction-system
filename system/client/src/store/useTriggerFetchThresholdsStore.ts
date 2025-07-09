import { create } from 'zustand';

interface TriggerStoreState {
  trigger: boolean;
  fetchThresholds: () => void;
};

const useTriggerFetchThresholdsStore = create<TriggerStoreState>((set) => ({
  trigger: false,
  fetchThresholds: () =>
    set((state) => ({
      trigger: !state.trigger,
    })),
}));

export default useTriggerFetchThresholdsStore;
