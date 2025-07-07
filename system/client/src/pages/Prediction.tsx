import MainContainer from '@/components/MainContainer';
import PageContainer from '@/components/PageContainer';
import PredictionForm from '@/components/PredictionForm';

const Prediction = () => {
  return (
    <PageContainer title='Prediction'>
      <MainContainer title='Fill the form to predict' modeSelectorVisible={false}>
        <PredictionForm />
      </MainContainer>
    </PageContainer>
  );
};

export default Prediction;
