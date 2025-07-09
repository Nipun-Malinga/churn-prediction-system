import { TrainedModel } from '@/models/ModelDetails';
import { create } from 'zustand';

interface TrainedModelState {
  trainedModel: TrainedModel | null;
  setTrainedModel: (model: TrainedModel) => void;
}

const useTrainedModelStore = create<TrainedModelState>((set) => ({
  trainedModel: null,
  setTrainedModel: (data) => {
    set({ trainedModel: data });
  },
}));

export default useTrainedModelStore;
