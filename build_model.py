import re
import csv
import pickle
from sklearn.ensemble import IsolationForest
import pandas as pd
from logs_to_df import logs_to_df
from monitor import monitor_log_file
from preprocess_pipeline import preprocess_pipeline
from model_fit import model_fit

def build_model(path):
    monitor_log_file(path)
    df = preprocess_pipeline()
    model = model_fit(df)
    with open('model.pkl','wb') as f:
        pickle.dump(model,f)


