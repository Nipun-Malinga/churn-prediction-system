interface PerformanceDataPoint {
  data: number;
  updated_date: string;
}

interface PerformanceDriftHistory {
  id: number;
  date: string;
  model_info_id: number;
  accuracy_drift: number;
  precision_drift: number;
  recall_drift: number;
  f1_score_drift: number;
}

export type { PerformanceDataPoint, PerformanceDriftHistory };
