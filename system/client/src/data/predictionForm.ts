const formInputs = [
  {
    title: 'Balance',
    name: 'balance',
  },
  {
    title: 'Credit Score',
    name: 'credit_score',
  },
  {
    title: 'Number of Products',
    name: 'num_of_products',
  },
  {
    title: 'Age',
    name: 'age',
  },
  {
    title: 'Estimated Salary',
    name: 'estimated_salary',
  },
  {
    title: 'Tenure',
    name: 'tenure',
  },
];

const selectionData = [
  {
    title: 'Gender',
    name: 'gender',
    data: [
      { key: 'Male', value: 'Male' },
      { key: 'Female', value: 'Female' },
    ],
  },
  {
    title: 'Education',
    name: 'education',
    data: [
      { key: 'Primary', value: 'primary' },
      { key: 'Secondary', value: 'secondary' },
      { key: 'Tertiary', value: 'tertiary' },
      { key: 'Unknown', value: 'unknown' },
    ],
  },
  {
    title: 'Geography',
    name: 'geography',
    data: [
      { key: 'France', value: 'France' },
      { key: 'Germany', value: 'Germany' },
      { key: 'Spain', value: 'Spain' },
    ],
  },
  {
    title: 'Has Credit Card',
    name: 'has_cr_card',
    data: [
      { key: 'Yes', value: '1' },
      { key: 'No', value: '0' },
    ],
  },
  {
    title: 'Card Type',
    name: 'card_type',
    data: [
      { key: 'None', value: 'None' },
      { key: 'Silver', value: 'SILVER' },
      { key: 'Gold', value: 'GOLD' },
      { key: 'Diamond', value: 'DIAMOND' },
      { key: 'Platinum', value: 'PLATINUM' },
    ],
  },
  {
    title: 'Is Active Member',
    name: 'is_active_member',
    data: [
      { key: 'Yes', value: '1' },
      { key: 'No', value: '0' },
    ],
  },
  {
    title: 'Housing',
    name: 'housing',
    data: [
      { key: 'Yes', value: 'yes' },
      { key: 'No', value: 'no' },
    ],
  },
  {
    title: 'Loan',
    name: 'loan',
    data: [
      { key: 'Yes', value: 'yes' },
      { key: 'No', value: 'no' },
    ],
  },
];

export { formInputs, selectionData };
