################### FUNCTIONS #######################

import pandas as pd

def create_temperature_dataframe(temperatures):
    """
    Prepares a Pandas DataFrame from a list of temperatures and formats it.
    
    Parameters:
    - temperatures (list): A list of temperature values.
    
    Returns:
    - DataFrame: A formatted Pandas DataFrame with renamed columns.
    """
    # Create a DataFrame
    temperatures_df = pd.DataFrame(temperatures, columns=['temperature']).reset_index(drop=True)
    
    # Rename the column
    temperatures_df.rename(columns={'temperature': 'Temp (°F)'}, inplace=True)
    
    return temperatures_df


def print_temperature_dataframe(df):
    """
    Prints a Pandas DataFrame with specific formatting for numeric columns.
    
    Parameters:
    - df (DataFrame): The Pandas DataFrame to print.
    """
    print(df.to_string(formatters={'Temp (°F)': '{:.1f}'.format}, index=False))


def dal_temps():
    """
    Main function to handle the workflow of preparing, modifying, and printing the DataFrame.
    
    Returns:
    - DataFrame: The created DataFrame.
    """
    # Input your data
    temperatures = [36, 36, 44, 41, 44, 45, 53, 61, 63, 58, 58, 55, 52, 56]
    
    print(f"\nDallas, TX 14 Day Forecast\n", f"========================\n")
    
    # Prepare the DataFrame
    temperatures_df = create_temperature_dataframe(temperatures)
    
    # Print the DataFrame
    print_temperature_dataframe(temperatures_df)
    
    # Return the DataFrame for further use
    return temperatures_df
    
# ===================================== STATS FUNCTION =================================

def calc_des_stats(df, column_name):
    """
    Calculates and prints descriptive statistics for a specified column in a DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame containing the data.
    - column_name (str): The name of the column to calculate statistics for.

    Returns:
    - None
    """
    # Calculate individual statistics
    mean = df[column_name].mean()
    median = df[column_name].median()
    variance = df[column_name].var()
    stdeviation = df[column_name].std()

    # Print the calculated statistics
    print("Descriptive Statistics for", column_name)
    print("---------------------------------------")
    print("Mean =", round(mean, 2))
    print("Median =", round(median, 2))
    print("Variance =", round(variance, 2))
    print("Standard Deviation =", round(stdeviation, 2))
    print("")

    # Use the describe method to print a summary of statistics
    print("Describe Method Output")
    print("----------------------")
    print(df[column_name].describe())



# ===================================== PLOT FUNCTIONS =================================



import seaborn as sns
import matplotlib.pyplot as plt

def plot_temperature_trends(df, column_name):
    """
    Plots temperature trends with descriptive annotations, mean, and dynamic ranges.

    Parameters:
    - df (DataFrame): The Pandas DataFrame containing the temperature data.
    - column_name (str): The column name containing temperature values.

    Returns:
    - None
    """
    # Set plot style and size
    sns.set_style("darkgrid")
    plt.figure(figsize=(12, 8))

    # Line plot with markers
    sns.lineplot(data=df, x=df.index, y=column_name, marker='o', color='blue', label='Dallas Temperatures')

    # Highlight max temperature
    max_temp = df[column_name].max()
    max_temp_day = df[column_name].idxmax()
    plt.annotate(
        f'Highest: {max_temp}°',
        xy=(max_temp_day, max_temp),
        xytext=(max_temp_day + 1, max_temp + 2),
        arrowprops=dict(facecolor='black', arrowstyle='->'),
        bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white')
    )

    # Add horizontal line for mean temperature
    mean_temp = df[column_name].mean()
    plt.axhline(y=mean_temp, color='red', linestyle='--', label=f'Mean Temperature: {mean_temp:.1f}°F')

    # Add vertical line for max temperature
    plt.axvline(x=max_temp_day, color='green', linestyle='--', label='Day of Max Temp')

    # Highlight temperature range dynamically
    plt.fill_between(
        df.index,
        df[column_name],
        mean_temp,
        where=(df[column_name] > mean_temp),
        interpolate=True,
        color='lightblue',
        alpha=0.3,
        label='Above Mean'
    )

    # Add labels, title, and legend
    plt.title('Dallas, TX: 14-Day Temperature Trends', fontsize=22, pad=20, loc='center')
    plt.xlabel('Days', fontsize=16, labelpad=10)
    plt.ylabel('Temperature (°F)', fontsize=16, labelpad=10)
    plt.xticks(ticks=range(len(df)), labels=[f"Day {i+1}" for i in range(len(df))], rotation=45)
    plt.legend(title='Legend', fontsize=12)

    # Show dynamic range as text
    plt.text(
        x=0.5,
        y=df[column_name].min() - 2,
        s=f"Range: {df[column_name].min()}°F - {df[column_name].max()}°F",
        fontsize=12,
        color='black',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
    )

    # Show plot
    plt.show()



################################ PLOT 2 ######################################


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import random

def plot_temperature_comparison(temperatures_df, column_name):
    """
    Generates a side-by-side boxplot comparing your temperature data with randomly generated data.

    Parameters:
    - temperatures_df (DataFrame): Your DataFrame containing the temperature data.
    - column_name (str): The name of the temperature column in your DataFrame.

    Returns:
    - None
    """
    # Create temperature data for Zion (randomly generated)
    mean = random.randint(int(temperatures_df[column_name].min()), int(temperatures_df[column_name].max()))
    std_deviation = random.randint(
        int(round(temperatures_df[column_name].std(), 0)),
        int(round(2 * temperatures_df[column_name].std(), 0))
    )
    zion_temperatures = np.random.normal(mean, std_deviation, 25)
    zion_temperatures = pd.DataFrame(zion_temperatures, columns=[column_name])

    # Prepare data for side-by-side boxplots
    temperatures_df['Dataset'] = 'My Data'
    zion_temperatures['Dataset'] = 'Zion Data'
    both_temp_df = pd.concat([temperatures_df, zion_temperatures], ignore_index=True)

    # Set up the plot
    plt.figure(figsize=(12, 8))
    sns.set_style("darkgrid")

    # Boxplot with color palette
    sns.boxplot(x="Dataset", y=column_name, data=both_temp_df, palette="pastel", showfliers=True)

    # Overlay individual data points
    sns.stripplot(x="Dataset", y=column_name, data=both_temp_df, color="black", size=5, jitter=True, alpha=0.6)

    # Add horizontal mean line
    mean_temp = both_temp_df[column_name].mean()
    plt.axhline(
        y=mean_temp,
        color='red',
        linestyle='--',
        linewidth=1.5,
        label=f'Mean Temperature: {mean_temp:.2f}°F'
    )

    # Add title and labels
    plt.title('Comparison of Temperature Distributions', fontsize=20, pad=15)
    plt.xlabel('Dataset', fontsize=14, labelpad=10)
    plt.ylabel('Temperature (°F)', fontsize=14, labelpad=10)
    plt.ylim([both_temp_df[column_name].min() - 5, both_temp_df[column_name].max() + 5])

    # Add legend
    plt.legend(loc='upper right')

    # Show the plot
    plt.show()


