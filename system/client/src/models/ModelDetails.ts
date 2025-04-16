interface Model {
  id: number;
  name: string;
  base_model: boolean;
}

interface BasicModelInfo {
  accuracy: number;
  updatedDate: string;
}

interface AdvancedModelInfo {}

export type { Model, BasicModelInfo, AdvancedModelInfo };
