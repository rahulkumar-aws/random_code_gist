import os
import json
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Directory to save logs and models
experiment_dir = 'experiment_logs'
if not os.path.exists(experiment_dir):
    os.makedirs(experiment_dir)

# Function to run an experiment and log results
def run_experiment(n_estimators, experiment_id):
    # Load dataset
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

    # Train the model
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"Experiment {experiment_id} - n_estimators: {n_estimators}, Accuracy: {accuracy}")

    # Log parameters, metrics, and model
    log_data = {
        "experiment_id": experiment_id,
        "parameters": {"n_estimators": n_estimators},
        "metrics": {"accuracy": accuracy}
    }

    # Save logs to a JSON file
    with open(f'{experiment_dir}/log_{experiment_id}.json', 'w') as f:
        json.dump(log_data, f)

    # Save the model
    joblib.dump(model, f'{experiment_dir}/model_{experiment_id}.pkl')

    return log_data

# Run multiple experiments with different parameters
experiments = []
for i, n_estimators in enumerate([10, 50, 100, 200, 500]):
    log_data = run_experiment(n_estimators, experiment_id=i+1)
    experiments.append(log_data)

# Save all experiments to a summary file
with open(f'{experiment_dir}/experiment_summary.json', 'w') as f:
    json.dump(experiments, f)

# Visualize the Results

# Load experiment logs
experiment_logs = []
for file_name in os.listdir(experiment_dir):
    if file_name.startswith('log_') and file_name.endswith('.json'):
        with open(os.path.join(experiment_dir, file_name), 'r') as f:
            experiment_logs.append(json.load(f))

# Convert logs to a DataFrame
df = pd.DataFrame([{
    'experiment_id': log['experiment_id'],
    'n_estimators': log['parameters']['n_estimators'],
    'accuracy': log['metrics']['accuracy']
} for log in experiment_logs])

# Plot the results
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='n_estimators', y='accuracy', marker='o')
plt.title('Model Accuracy vs. Number of Estimators')
plt.xlabel('Number of Estimators')
plt.ylabel('Accuracy')
plt.grid(True)
plt.show()
