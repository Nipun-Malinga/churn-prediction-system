import { z } from 'zod';

const driftDetectorSchema = z.object({
  accuracy: z.preprocess(
    (val) => Number(val),
    z.number().min(-100, 'Accuracy must be negative').max(-1, 'Maximum threshold is -1')
  ),
  precision: z.preprocess(
    (val) => Number(val),
    z.number().min(-100, 'Precision must be negative').max(-1, 'Maximum threshold is -1')
  ),
  recall: z.preprocess(
    (val) => Number(val),
    z.number().min(-100, 'Recall must be negative').max(-1, 'Maximum threshold is -1')
  ),
  f1_score: z.preprocess(
    (val) => Number(val),
    z.number().min(-100, 'F1 Score must be negative').max(-1, 'Maximum threshold is -1')
  ),
});

export default driftDetectorSchema;
