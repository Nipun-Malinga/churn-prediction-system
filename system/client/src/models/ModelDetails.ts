interface BasicModelInfo {
  id: number;
  base_model: boolean;
  name: string;
  accuracy: number;
  updated_date: string;
}

interface AdvancedModelInfo {
  FN: number;
  FP: number;
  TN: number;
  TP: number;
  accuracy: number;
  f1_score: number;
  id: number;
  is_automated_tuning: boolean;
  model_id: number;
  precision: number;
  recall: number;
  updated_date: string;
}

interface TrainedModel {
  accuracy: number;
  f1_score: number;
  is_production_model: false;
  model_name: string;
  precision: number;
  recall: number;
  trained_date: string;
  version_name: string;
  batch_id: string;
}

export type { AdvancedModelInfo, BasicModelInfo, TrainedModel };
