import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt5.QtCore import QTimer, Qt
import pandas as pd
import re
import pickle
import os
import csv
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
from logs_to_df import logs_to_df
from monitor import monitor_log_file
from preprocess_pipeline import preprocess_pipeline
from build_model import build_model

def calculate_deviation(row,df):
    for col in ['num_clients', 'num_requests', 'num_get_requests', 'num_4xx_5xx_codes', 'avg_req_size', 'num_requests_per_client']:
        if row[col] != 0:
            row[f"{col}_deviation%"] = (abs(row[col] - df[col].mean()) / df[col].mean())*100
        else:
            row[f"{col}_deviation%"] = 0
    return row

def update_table(table1, table2,table3, path):
    monitor_log_file(path)
    df = preprocess_pipeline()
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
        scores = model.decision_function(df)
        anomaly_df = pd.Series(scores, dtype=float)
        df = df.reset_index()
        df['anomaly_scores'] = anomaly_df
        df['anomaly_scores'] = df['anomaly_scores'].abs()
        df = df.apply(calculate_deviation, axis=1, args=(df,))
        for col in df.columns:
            if pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].round(2)
        threshold = np.percentile(np.abs(df['anomaly_scores']), 99)
        df.to_csv("anomaly_data.csv")
        high_anomaly_rows = df[np.abs(df['anomaly_scores']) > threshold]
        sorted_anomalies = high_anomaly_rows.sort_values(by=['anomaly_scores'], ascending=False)
        df1 = df.tail(10)
        table1.setHorizontalHeaderLabels(df.columns)
        table1.setRowCount(0)
        table1.setColumnCount(len(df.columns))
        header = table1.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        row_index = 0
        for _, row in df1.iterrows():
            table1.insertRow(row_index)
            for col_index, value in enumerate(row):
                table_item = QTableWidgetItem(str(value))
                table_item.setTextAlignment(Qt.AlignCenter)
                table1.setItem(row_index, col_index, table_item)
            row_index += 1
        data = [("Anomaly Score",df.iloc[-1]['anomaly_scores']), ("Number of clients",df.iloc[-1]['num_clients_deviation%']), ("Number of requests", df.iloc[-1]['num_requests_deviation%']),("Number of get requests",df.iloc[-1]['num_get_requests_deviation%']),("Number of 4xx,5xx codes",df.iloc[-1]['num_4xx_5xx_codes_deviation%']), ("Avg request size",df.iloc[-1]['avg_req_size_deviation%']), ("Number of requests per client",df.iloc[-1]['num_requests_per_client_deviation%'])]
        table3.setColumnCount(2)
        table3.setRowCount(len(data))
        for row, (name, value) in enumerate(data):
            table3.setItem(row, 0, QTableWidgetItem(name))
            table3.setItem(row, 1, QTableWidgetItem(str(value)))
        table3.resizeColumnsToContents()
        table3.resizeRowsToContents()
        table2.setHorizontalHeaderLabels(df.columns)
        table2.setRowCount(0)
        table2.setColumnCount(len(df.columns))
        header = table2.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        row_index = 0
        for _, row in sorted_anomalies.iterrows():
            table2.insertRow(row_index)
            for col_index, value in enumerate(row):
                table_item = QTableWidgetItem(str(value))
                table_item.setTextAlignment(Qt.AlignCenter)
                table2.setItem(row_index, col_index, table_item)
            row_index += 1

def show_pyqt_interface(path):

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Anomaly Detection System for Apache and Nginx Server Logs")
    layout = QVBoxLayout()
    table1_label = QLabel("Anomaly Data (Past few hours)")
    font = table1_label.font()
    font.setPointSize(24)
    table1_label.setFont(font)
    table1 = QTableWidget()
    table1.setHorizontalHeaderLabels(['time_interval', 'num_clients', 'num_requests', 'num_get_requests',
       'num_4xx_5xx_codes', 'avg_req_size', 'num_requests_per_client',
       'anomaly_scores', 'num_clients_deviation%', 'num_requests_deviation%',
       'num_get_requests_deviation%', 'num_4xx_5xx_codes_deviation%',
       'avg_req_size_deviation%', 'num_requests_per_client_deviation%'])
    table2 = QTableWidget()
    table2.setHorizontalHeaderLabels(['time_interval', 'num_clients', 'num_requests', 'num_get_requests',
       'num_4xx_5xx_codes', 'avg_req_size', 'num_requests_per_client',
       'anomaly_scores', 'num_clients_deviation%', 'num_requests_deviation%',
       'num_get_requests_deviation%', 'num_4xx_5xx_codes_deviation%',
       'avg_req_size_deviation%', 'num_requests_per_client_deviation%'])
    table3 = QTableWidget()
    table3.setHorizontalHeaderLabels(['time_interval', 'num_clients', 'num_requests', 'num_get_requests',
       'num_4xx_5xx_codes', 'avg_req_size', 'num_requests_per_client',
       'anomaly_scores', 'num_clients_deviation%', 'num_requests_deviation%',
       'num_get_requests_deviation%', 'num_4xx_5xx_codes_deviation%',
       'avg_req_size_deviation%', 'num_requests_per_client_deviation%'])
    table2_label = QLabel("Anomaly Data (Highest recorded)")
    font = table2_label.font()
    font.setPointSize(24)
    table2_label.setFont(font)
    table3_label = QLabel("Last Recorded Hour Deviation %")
    font = table3_label.font()
    font.setPointSize(24)
    table3_label.setFont(font)
    layout.addWidget(table1_label)
    layout.addWidget(table1)
    layout.addWidget(table3_label)
    layout.addWidget(table3)
    layout.addWidget(table2_label)
    layout.addWidget(table2)
    update_table(table1,table2,table3,path)
    update_table(table1,table2,table3,path)
    window.setLayout(layout)
    window.show()
    timer = QTimer()
    timer.timeout.connect(lambda: update_table(table1,table2,table3,path))
    timer.start(60000)
    sys.exit(app.exec_())

if __name__ == '__main__':
    path = input("Enter the path for the log file ")
    file_name = "model.pkl"  
    if os.path.isfile(file_name):
        show_pyqt_interface(path)
    else:
        build_model(path)
        print("Model built, run again")