import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filename):
    """
    Loads HR data from a CSV file into a pandas DataFrame.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded HR data.
        None: If an error occurs during loading.
    """
    try:
        df = pd.read_csv(filename)
        print(f"Successfully loaded data from {filename}")
        return df
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{filename}' is empty.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        return None

def display_basic_info(df):
    """
    Displays basic information about the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("\n--- Basic DataFrame Information ---")
        print(df.info())
        print("\n--- First 5 Rows ---")
        print(df.head())
        print("\n--- Descriptive Statistics ---")
        print(df.describe())

def analyze_employment_status(df):
    """
    Analyzes and visualizes employment status.

    Args:
        df (pandas.DataFrame): The HR DataFrame.
    """
    if df is not None and 'EmploymentStatus' in df.columns:
        print("\n--- Employment Status Analysis ---")
        status_counts = df['EmploymentStatus'].value_counts()
        print(status_counts)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=status_counts.index, y=status_counts.values, palette='viridis')
        plt.title('Distribution of Employment Status')
        plt.xlabel('Employment Status')
        plt.ylabel('Number of Employees')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    elif df is not None:
        print("\n'EmploymentStatus' column not found in the DataFrame.")

def analyze_department_distribution(df):
    """
    Analyzes and visualizes department distribution.

    Args:
        df (pandas.DataFrame): The HR DataFrame.
    """
    if df is not None and 'Department' in df.columns:
        print("\n--- Department Distribution Analysis ---")
        department_counts = df['Department'].value_counts()
        print(department_counts)

        plt.figure(figsize=(12, 7))
        sns.pie(department_counts, labels=department_counts.index, autopct='%1.1f%%', startangle=140, cmap='Pastel1')
        plt.title('Employee Distribution Across Departments')
        plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout()
        plt.show()
    elif df is not None:
        print("\n'Department' column not found in the DataFrame.")

def main():
    """
    Main function to run the HR analysis workflow.
    """
    print("--- Starting HR Data Analysis ---")

    # Define the path to your dataset
    dataset_path = 'HRDataset_v14.csv'

    # Load the data
    hr_df = load_data(dataset_path)

    if hr_df is not None:
        display_basic_info(hr_df)
        analyze_employment_status(hr_df)
        analyze_department_distribution(hr_df)
    else:
        print("Data loading failed. Exiting analysis.")

    print("\n--- HR Data Analysis Complete ---")

if __name__ == "__main__":
    main()
