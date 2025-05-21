import { create } from 'zustand';

type TriggerStore = {
  trigger: boolean;
  fetchThresholds: () => void;
};

const useTriggerFetchThresholdsStore = create<TriggerStore>((set) => ({
  trigger: false,
  fetchThresholds: () =>
    set((state) => ({
      trigger: !state.trigger,
    })),
}));

export default useTriggerFetchThresholdsStore;
