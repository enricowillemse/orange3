from Orange import classification
import numpy as np


class DummyLearner(classification.Fitter):
    def fit(self, X, Y, W):
        rows = Y.shape[0]
        value = Y[np.random.randint(0, rows), 0]
        class_vals = np.unique(Y)
        prob = (class_vals == value) * 0.8 + 0.1
        return DummyPredictor(value, prob)


class DummyPredictor(classification.Model):
    def __init__(self, value, prob):
        self.value = value
        self.prob = prob

    def predict(self, X):
        rows = X.shape[0]
        return np.tile(self.value, rows), np.tile(self.prob, (rows, 1))


class DummyMulticlassLearner(classification.Fitter):
    supports_multiclass = True

    def fit(self, X, Y, W):
        rows, class_vars = Y.shape
        value = Y[np.random.randint(0, rows)]
        used_vals = [np.unique(y) for y in Y.T]
        max_vals = max(len(np.unique(y)) for y in Y.T)
        prob = np.zeros((class_vars, max_vals))
        for c in range(class_vars):
            class_prob = (used_vals[c] == value[c]) * 0.8 + 0.1
            prob[c, :] = np.hstack((class_prob, np.zeros(max_vals - len(class_prob))))
        return DummyMulticlassPredictor(value, prob)


class DummyMulticlassPredictor(classification.Model):
    def __init__(self, value, prob):
        self.value = value
        self.prob = prob

    def predict(self, X):
        rows = X.shape[0]
        return np.tile(self.value, (rows, 1)), np.tile(self.prob, (rows, 1, 1))