# Logs-ADS Web Server Access Logs Anomaly Detection System
## Description 
**Logs-ADS** is a real-time anomaly detection system designed to continuously monitor Apache and Nginx web server logs, identifying unusual patterns and potential security threats. Utilizing the Isolation Forest algorithm, a powerful anomaly detection technique, Logs-ADS effectively isolates and flags anomalous data points within the web server logs.

The system offers customizable time intervals, allowing users to define the frequency of log analysis and anomaly detection. This flexibility ensures that the system can adapt to different monitoring requirements and detect anomalies in a timely manner. Furthermore, Logs-ADS features a user-friendly PyQt interface, providing a visual representation of detected anomalies and enabling easy interaction with the system. By continuously monitoring web server logs and promptly identifying anomalies, Logs-ADS serves as a valuable tool for safeguarding the integrity and security of web applications.
## Features
- Continuous monitoring of the log file for new logs.
- Customizable time intervals for checking logs.
- Automated model building and monitoring process.
- Looks for anomalies in these five things
   - 'num_clients'
   - 'num_requests'
   - 'num_get_requests'
   - 'num_4xx_5xx_codes'
   - 'avg_req_size'
   - 'num_requests_per_client'
## Working
- The logs are first preprocessed and converted into csv format.
- Then the logs are grouped according to the time intervals they belong to.
- After that Isolation Forest model is trained on that data.
- Then the monitoring is started on the previous data and the new incoming data.
- The results of the model are shown to the user on a user interface built using PyQt
![image](https://github.com/user-attachments/assets/da3c2353-a13a-4a3b-8899-ed18a5eb2bdf)

## Installation and Setup Guide
- First clone the project into your folder using `git clone https://github.com/Sohail4625/ServerLogsADS.git`.
- Then install all the requirements using `pip install -r requirements.txt`.
- To build the model, run the command `python start_monitor.py`.
- Specify the path for the logs file. If you want to test the system, use the sample log file and enter `access.log`.
- Once the model is built, run the command again.
- Now monitoring has started and when u restart the monitoring, the same model will be used and new data will be processed.
- If you want to rebuild the model, just delete the `model.pkl` in your folder and clear the data in the data.csv file and use the same commands.
- The tables in the interface show the anomaly scores and also percentage deviation from the average value.
## Further development
- It can be built as a tool for anyone to download and use.
- It can be configured to take inputs from multiple types of sources.
