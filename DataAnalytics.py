import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
csv_filename = 'gun_violence_data.csv'
df = pd.read_csv(csv_filename)

# Display basic information about the dataset
print("Dataset Information:")
print(df.info())

# Display the first few rows of the dataset
print("\nFirst few rows of the dataset:")
print(df.head())

# Statistical measures for the numerical variables
target_variable = 'victims_killed'

mean_value = df[target_variable].mean()
median_value = df[target_variable].median()
std_deviation = df[target_variable].std()

print("\nStatistical Measures:")
print(f"Mean: {mean_value}")
print(f"Median: {median_value}")
print(f"Standard Deviation: {std_deviation}")

# Visualization 1: Histogram showing the distribution of the target variable
plt.figure(figsize=(10, 6))
plt.hist(df[target_variable], bins=20, color='blue', edgecolor='black')
plt.title(f'Distribution of {target_variable}')
plt.xlabel(target_variable)
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Visualization 2: Bar chart comparing the target variable across different states
plt.figure(figsize=(14, 6))
df_state_mean = df.groupby('state')[target_variable].mean().sort_values(ascending=False)
df_state_mean.plot(kind='bar', color='green')
plt.title(f'{target_variable} by State')
plt.xlabel('State')
plt.ylabel(target_variable)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.show()


