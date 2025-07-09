import { TrainedModel } from '@/models/ModelDetails';
import { create } from 'zustand';

interface NewTrainedModel {
  trainedModel: TrainedModel | null;
  setTrainedModel: (model: TrainedModel) => void;
}

const useTrainedModelStore = create<NewTrainedModel>((set) => ({
  trainedModel: null,
  setTrainedModel: (model: TrainedModel) => {
    set({ trainedModel: model });
  },
}));

export default useTrainedModelStore;
