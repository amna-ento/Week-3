import joblib

pipeline = None


def load_pipeline():
    global pipeline
    pipeline = joblib.load("churn_pipeline.pkl")


def get_pipeline():
    return pipeline


def predict(data):
    return pipeline.predict(data)


def predict_probability(data):
    return pipeline.predict_proba(data)