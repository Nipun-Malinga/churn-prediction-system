interface SampleData {
  age: number;
  balance: number;
  card_type: string;
  credit_score: number;
  education: string;
  estimated_salary: number;
  exited: number;
  gender: string;
  geography: string;
  has_cr_card: number;
  housing: string;
  is_active_member: number;
  loan: string;
  num_of_products: number;
  tenure: number;
}

interface ClassImbalance {
  churned: number;
  not_churned: number;
}

interface Features {
  name: string;
  type: number;
}

interface Shape {
  total_features: number;
  total_rows: number;
}

interface BasicDatasetInfo {
  class_imbalance: ClassImbalance;
  features: Features[];
  sample_data: SampleData[];
  shape: Shape;
}

export type { BasicDatasetInfo, ClassImbalance };
