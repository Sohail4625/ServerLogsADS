import pandas as pd
def preprocess_pipeline():
    columns = ['client', 'userid', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'user_agent']
    logs_df = pd.read_csv('data.csv',names=columns)
    logs_df['client'] = logs_df['client'].astype('category')
    del logs_df['userid']
    logs_df['datetime'] = pd.to_datetime(logs_df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
    logs_df['method'] = logs_df['method'].astype('category')
    logs_df['status'] = logs_df['status'].astype('int16')
    logs_df['size'] = logs_df['size'].astype('int32')
    logs_df['referer'] = logs_df['referer'].astype('category')
    logs_df['user_agent'] = logs_df['user_agent'].astype('category')
    logs_df['time_interval'] = logs_df['datetime'].dt.floor('h')
    # For hourly intervals
    # Group by time interval and create new features
    grouped_df = logs_df.groupby('time_interval').agg(
        num_clients=('client', 'nunique'),
        num_requests=('request', 'count'),
        num_get_requests=('method', lambda x: (x == 'GET').sum()),
        num_4xx_5xx_codes=('status', lambda x: ((x >= 400) & (x < 600)).sum()),
        avg_req_size=('size','mean'),
    )
    grouped_df['num_requests_per_client'] = grouped_df['num_requests']/grouped_df['num_clients']
    return grouped_df
