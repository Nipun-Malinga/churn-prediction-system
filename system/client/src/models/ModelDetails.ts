interface Model {
  id: number;
  name: string;
  base_model: boolean;
}

interface BasicModelInfo {
  accuracy: number;
  updatedDate: string;
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

export type { AdvancedModelInfo, BasicModelInfo, Model };
