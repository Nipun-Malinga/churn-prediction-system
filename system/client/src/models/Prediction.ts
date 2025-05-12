interface Prediction {
  education: string;
  credit_score: number;
  geography: string;
  gender: string;
  age: number;
  tenure: number;
  balance: number;
  num_of_products: number;
  has_cr_card: number;
  card_type: string;
  is_active_member: number;
  estimated_salary: number;
  housing: string;
  loan: string;
}

interface PredictionResponse {
  Prediction: number;
  Probability: [[number]];
}

export type { Prediction, PredictionResponse };
