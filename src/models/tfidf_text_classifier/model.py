import re
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class TfidfTextClassifier:
    """
    The TfidfTextClassifier class is designed for text classification using
    TfidfVectorizer and LogisticRegression algorithms. This class has methods
    for model training, saving and loading the model, and making predictions.
    """

    def __init__(self, estimator=LogisticRegression()):
        self.clf = estimator
        self.vectorizer = TfidfVectorizer(ngram_range=(2, 3))
        self.pipeline = Pipeline(
            [('tfidf', self.vectorizer), ('clf', self.clf)])

    def fit(self, feature: pd.Series, target: pd.Series):
        """
        A method that takes a feature and a target Series as input and trains
        the model using the LogisticRegression algorithm.
        """
        feature = feature.astype('U').apply(self._preprocess_text)
        target = target.astype('int')

        self.pipeline.fit(feature, target)

    def predict(self, text: str) -> int:
        """
        A method that takes a text string as input, preprocesses it,
        vectorized it, and returns the predicted label as an integer.
        """
        text = self._preprocess_text(text)
        text = self.vectorizer.transform([text])
        label = self.clf.predict(text)
        predict = int(label[0])
        return predict

    def predict_proba(self, text: str) -> int:
        """
        A method that takes a text string as input, preprocesses it,
        vectorized it, and returns the probability estimates.
        """
        text = self._preprocess_text(text)
        text = self.vectorizer.transform([text])
        probability = self.clf.predict_proba(text)
        probability = probability[0][1]
        return probability

    @staticmethod
    def _preprocess_text(text: str) -> str:
        """
        A static method that takes a text string as input and returns a
        preprocessed version of it.
        """
        text = re.sub(r'[^А-Яа-яёЁ]', ' ', text.lower())
        return text

    def save_model(self,
                   path_to_model: str = 'model.pkl',
                   path_to_vectorizer: str = 'vectorizer.pkl'):
        """
        A method that saves the trained model and vectorizer
        to the specified file paths.
        """
        joblib.dump(self.clf, path_to_model)
        joblib.dump(self.vectorizer, path_to_vectorizer)

    def load_model(self,
                   path_to_model: str = 'model.pkl',
                   path_to_vectorizer: str = 'vectorizer.pkl'):
        """
        A method that loads the trained model and vectorizer
        from the specified file paths.
        """
        self.clf = joblib.load(path_to_model)
        self.vectorizer = joblib.load(path_to_vectorizer)
        self.pipeline = Pipeline(
            [('tfidf', self.vectorizer), ('clf', self.clf)])
