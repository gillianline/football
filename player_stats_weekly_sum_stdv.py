import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Read the data from the Excel sheet into a pandas DataFrame
data = pd.read_csv('player_profiles.csv')

# Calculate the weekly sum for each player for each metric
weekly_sum = data.groupby(['Week', 'Player Name']).sum().reset_index()

# Define color palette for metrics
colors = ['red', 'blue', 'green', 'purple']

# Create a PDF to save all the graphs
with PdfPages('player_stats_all_weeks_sums_with_stdv.pdf') as pdf:
    for week in range(1, data['Week'].max() + 1):
        plt.figure(figsize=(24, 8))

        # List of metrics
        metrics = ['Player Load', 'Sprint Distance', 'Power Plays', 'Distance']
        
        # Dictionary to store max values for each metric
        max_values = {}
        
        # Calculate max values for each metric
        for metric in metrics:
            max_value = data[metric].max()
            max_values[metric] = max_value
        
        # Plotting for each metric
        for i, metric in enumerate(metrics, start=1):
            plt.subplot(2, 3, i)
            plt.title(f'{metric} Weekly Sum (Week {week})')
            plt.xlabel('Player Name')
            plt.ylabel(f'{metric}')
            
            week_data = weekly_sum[(weekly_sum['Week'] == week) & (weekly_sum['Player Name'].isin(data['Player Name']))]
            
            if not week_data.empty:
                plt.bar(week_data['Player Name'], week_data[metric], color=colors[i-1])  # Assign color from the palette
                plt.xticks(rotation=45, ha='right')
                if metric == 'Power Plays':
                    plt.ylim(0, max_values[metric] * 3.5)  # Increase y-axis limit for Power Plays
                else:
                    plt.ylim(0, max_values[metric] * 3)  # Set y-axis limit based on maximum weekly sum multiplied by 3
                
                # Plot standard deviation lines
                avg_value = week_data[metric].mean()
                std_value = week_data[metric].std()
                plt.axhline(y=avg_value + std_value, color='black', linestyle='--', linewidth=1)
                plt.axhline(y=avg_value - std_value, color='black', linestyle='--', linewidth=1)
                
                # Plot solid black line for overall average
                plt.axhline(y=avg_value, color='black', linestyle='-', linewidth=1)
            
            plt.tight_layout()
        
        # Save the figure to the PDF if there's data to plot
        if not all(week_data.empty for week_data in [weekly_sum]):
            pdf.savefig()
            plt.close()
