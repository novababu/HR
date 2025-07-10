import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="HR Data Analysis Dashboard", page_icon="📊")

@st.cache_data # Cache the data loading to improve performance
def load_data(filename):
    """
    Loads HR data from a CSV file into a pandas DataFrame.
    Uses st.cache_data to cache the function result for performance.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded HR data.
        None: If an error occurs during loading.
    """
    try:
        df = pd.read_csv(filename)
        st.success(f"Successfully loaded data from **{filename}**")
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{filename}' was not found. Please ensure it's in the correct directory.")
        return None
    except pd.errors.EmptyDataError:
        st.error(f"Error: The file '{filename}' is empty.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading data: {e}")
        return None

def display_basic_info(df):
    """
    Displays basic information about the DataFrame using Streamlit.

    Args:
        df (pandas.DataFrame): The DataFrame to analyze.
    """
    st.subheader("📊 Basic DataFrame Information")

    st.write("---")
    st.write("**First 5 Rows:**")
    st.dataframe(df.head())

    st.write("---")
    st.write("**DataFrame Info (Data Types, Non-Null Counts):**")
    # Redirect info to a string buffer to display in Streamlit
    import io
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.write("---")
    st.write("**Descriptive Statistics:**")
    st.dataframe(df.describe())

def analyze_employment_status(df):
    """
    Analyzes and visualizes employment status using Streamlit and Matplotlib/Seaborn.

    Args:
        df (pandas.DataFrame): The HR DataFrame.
    """
    st.subheader("📈 Employment Status Distribution")
    if 'EmploymentStatus' in df.columns:
        status_counts = df['EmploymentStatus'].value_counts()
        st.write("**Counts of Each Employment Status:**")
        st.dataframe(status_counts)

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=status_counts.index, y=status_counts.values, palette='viridis', ax=ax)
        ax.set_title('Distribution of Employment Status', fontsize=16)
        ax.set_xlabel('Employment Status', fontsize=12)
        ax.set_ylabel('Number of Employees', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig) # Display plot in Streamlit
        plt.close(fig) # Close the plot to free memory
    else:
        st.warning("The 'EmploymentStatus' column was not found in the dataset.")

def analyze_department_distribution(df):
    """
    Analyzes and visualizes department distribution using Streamlit and Matplotlib.

    Args:
        df (pandas.DataFrame): The HR DataFrame.
    """
    st.subheader("🌐 Employee Distribution Across Departments")
    if 'Department' in df.columns:
        department_counts = df['Department'].value_counts()
        st.write("**Counts of Employees Per Department:**")
        st.dataframe(department_counts)

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.pie(department_counts, labels=department_counts.index, autopct='%1.1f%%', startangle=140, cmap='Pastel1',
               pctdistance=0.85) # pctdistance moves percentages closer to center
        ax.set_title('Employee Distribution Across Departments', fontsize=16)
        ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout()
        st.pyplot(fig) # Display plot in Streamlit
        plt.close(fig) # Close the plot to free memory
    else:
        st.warning("The 'Department' column was not found in the dataset.")

def main():
    """
    Main function to run the Streamlit HR analysis dashboard.
    """
    st.title("Human Resources Data Analysis Dashboard")
    st.markdown("""
    Welcome to the HR Data Analysis Dashboard!
    This application allows you to explore key metrics and visualizations
    from your HR dataset.
    """)

    # Define the path to your dataset
    dataset_path = 'HRDataset_v14.csv'

    # Use a sidebar for dataset path input (optional, but good for flexibility)
    st.sidebar.header("Configuration")
    uploaded_file = st.sidebar.file_uploader("Upload your HR CSV file", type=["csv"])

    if uploaded_file is not None:
        # If a file is uploaded, use it
        hr_df = load_data(uploaded_file)
    else:
        # Otherwise, try to load from the default path
        st.sidebar.info(f"No file uploaded. Attempting to load from default path: **{dataset_path}**")
        hr_df = load_data(dataset_path)

    if hr_df is not None:
        # You can add a selection box or tabs for different analyses
        st.sidebar.subheader("Analysis Options")
        analysis_choice = st.sidebar.radio(
            "Choose an analysis:",
            ("Basic Info", "Employment Status", "Department Distribution")
        )

        if analysis_choice == "Basic Info":
            display_basic_info(hr_df)
        elif analysis_choice == "Employment Status":
            analyze_employment_status(hr_df)
        elif analysis_choice == "Department Distribution":
            analyze_department_distribution(hr_df)
    else:
        st.info("Please load a valid HR dataset to proceed with the analysis.")

    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")

if __name__ == "__main__":
    main()

