from sklearn.ensemble import IsolationForest

def model_fit(df):
    model = IsolationForest(contamination='auto')
    model.fit(df)
    return model