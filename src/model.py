import tensorflow_datasets as tfds
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score

if (__name__ == '__main__'):
    (train, test), info = tfds.load(
        name = "imdb_reviews",
        split = ["train", "test"],
        as_supervised = True,
        with_info = True
            )
    
    train = tfds.as_dataframe(train, info)

    test = tfds.as_dataframe(test, info)

    train.columns = ["label", "text"]

    test.columns = ["label", "text"]

    train['text'] = train['text'].astype(str)

    test['text'] = test['text'].astype(str)

    # train['text'] = train['text'].str.decode('utf-8')

    # test['text'] = test['text'].str.decode('utf-8')

    model = make_pipeline(CountVectorizer(), MultinomialNB())

    X_train = train['text']

    Y_train = train['label']

    model.fit(X_train, Y_train)

    X_test = test['text']

    Y_test = test['label']

    y_pred = model.predict(X_test)

    acc = accuracy_score(Y_test, y_pred)

    print(f"Accuracy of Naive Bayes on IMdb Movie Reviews dataset: {acc}")

    probs = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(Y_test, probs)

    print(f"AUC score for Naive Bayes on IMdb Movie Reviews dataset: {auc}")

    joblib.dump(model, 'sentiment.joblib')
