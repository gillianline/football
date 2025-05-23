import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data = pd.read_csv('player_profiles.csv')

#Day labels to actual dates
day_mapping = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'TH': 'Thursday', 'SAT': 'Saturday'}
data['Day'] = data['Day'].map(day_mapping)

#Average player load for each player for each day
average_player_load = data.groupby(['Day', 'Player Name'])['Player Load'].mean().reset_index()

#Average sprint distance for each player for each day
average_sprint_distance = data.groupby(['Day', 'Player Name'])['Sprint Distance'].mean().reset_index()

#Average top speed for each player for each day
average_top_speed = data.groupby(['Day', 'Player Name'])['Top Speed'].mean().reset_index()

#Average power plays for each player for each day
average_power_plays = data.groupby(['Day', 'Player Name'])['Power Plays'].mean().reset_index()

#Average distance for each player for each day
average_distance = data.groupby(['Day', 'Player Name'])['Distance'].mean().reset_index()

#Define color palette for metrics
colors = ['red', 'blue', 'orange', 'green', 'purple']

#Create a PDF to save all the graphs
with PdfPages('player_stats_all_days_with_stdv.pdf') as pdf:
    for date in data['Day'].unique():
        plt.figure(figsize=(24, 8))

     
        metrics = ['Player Load', 'Sprint Distance', 'Top Speed', 'Power Plays', 'Distance']
        
   
        max_values = {}
        
        #Calculate max values for each metric
        for metric in metrics:
            max_value = data[metric].max()
            max_values[metric] = max_value
        
      
        for i, metric in enumerate(metrics, start=1):
            plt.subplot(2, 3, i)
            plt.title(f'{metric} Daily Average ({date})')
            plt.xlabel('Player Name')
            plt.ylabel(f'{metric}')
            
            date_data = eval(f'average_{metric.lower().replace(" ", "_")}')
            date_data = date_data[date_data['Day'] == date]
            
            if not date_data.empty:
                plt.bar(date_data['Player Name'], date_data[metric], color=colors[i-1])  # Assign color from the palette
                plt.xticks(rotation=45, ha='right')
                
                # Adjust y-axis limit based on the metric
                if metric == 'Top Speed':
                    plt.ylim(10, 24)  # Set y-axis limit for Top Speed
                else:
                    plt.ylim(0, max_values[metric])  # Set y-axis limit for other metrics
                
                #Plot standard deviation lines
                avg_value = date_data[metric].mean()
                std_value = date_data[metric].std()
                plt.axhline(y=avg_value + std_value, color='black', linestyle='--', linewidth=1)
                plt.axhline(y=avg_value - std_value, color='black', linestyle='--', linewidth=1)
                
                #Plot solid black line for overall average
                plt.axhline(y=avg_value, color='black', linestyle='-', linewidth=1)
            
            plt.tight_layout()
        

        if not all(date_data.empty for date_data in [average_player_load, average_sprint_distance, average_top_speed, average_power_plays, average_distance]):
            pdf.savefig()
            plt.close()

