import { z } from 'zod';

const predictionSchema = z.object({
  balance: z.preprocess((val) => Number(val), z.number().min(0, 'Balance must be positive')),

  credit_score: z.preprocess(
    (val) => Number(val),
    z.number().min(0, 'Credit Score must be positive')
  ),

  num_of_products: z.preprocess(
    (val) => Number(val),
    z.number().min(0, 'Number of Products must be positive')
  ),

  age: z.preprocess((val) => Number(val), z.number().min(18, 'Age must be above 18')),

  estimated_salary: z.preprocess(
    (val) => Number(val),
    z.number().min(0, 'Estimated Salary must be positive')
  ),

  tenure: z.preprocess((val) => Number(val), z.number().min(0, 'Tenure must be positive')),

  gender: z.enum(['Male', 'Female'], {
    errorMap: () => ({ message: 'Gender must be Male or Female' }),
  }),

  education: z.enum(['primary', 'secondary', 'tertiary', 'unknown'], {
    errorMap: () => ({ message: 'Required' }),
  }),

  geography: z.enum(['France', 'Germany', 'Spain'], {
    errorMap: () => ({ message: 'Required' }),
  }),

  has_cr_card: z
    .enum(['0', '1'], {
      errorMap: () => ({ message: 'Required' }),
    })
    .transform(Number),

  card_type: z.enum(['SILVER', 'GOLD', 'DIAMOND', 'PLATINUM', 'None'], {
    errorMap: () => ({ message: 'Required' }),
  }),

  is_active_member: z
    .enum(['0', '1'], {
      errorMap: () => ({ message: 'Required' }),
    })
    .transform(Number),

  housing: z.enum(['yes', 'no'], {
    errorMap: () => ({ message: 'Housing must be Yes or No' }),
  }),

  loan: z.enum(['yes', 'no'], {
    errorMap: () => ({ message: 'Loan must be Yes or No' }),
  }),
});

export default predictionSchema;
