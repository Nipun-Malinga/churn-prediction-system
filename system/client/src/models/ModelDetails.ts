interface BasicModelInfo {
  id: number;
  base_model: number;
  name: number;
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

export type { AdvancedModelInfo, BasicModelInfo };
