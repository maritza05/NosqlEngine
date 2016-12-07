import pickle
import os
import numpy as np

class PerformanceClassifier:

    def __init__(self):
        cur_dir = os.path.dirname(__file__)
        print("Actual path: %s" %(cur_dir))
        self.vect = pickle.load(open(os.path.join(cur_dir, 'pkl_objects/vectorizer.pkl'), 'rb'))
        self.clf = pickle.load(open(os.path.join(cur_dir, 'pkl_objects/classifier.pkl'), 'rb'))

    def classify(self, document):
        X = self.vect.transform([document])
        Y = self.clf.predict(X)[0]
        proba = np.max(self.clf.predict_proba(X))
        return Y, proba