import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


data = pd.read_csv('player_profiles.csv')

#Color palette for metrics
colors = ['red', 'blue', 'orange', 'green', 'purple']

#Overall average and standard deviation for each metric
average_overall = {}
std_overall = {}
metrics = ['Player Load', 'Sprint Distance', 'Top Speed', 'Power Plays', 'Distance']
for metric in metrics:
    average_overall[metric] = data.groupby('Player Name')[metric].mean().mean()
    std_overall[metric] = data.groupby('Player Name')[metric].std().mean()

#PDF to save all the graphs
with PdfPages('player_stats_all_weeks_stdv_horizontal.pdf') as pdf:
    for week in range(1, data['Week'].max() + 1):
        plt.figure(figsize=(24, 8))
        
       
        for i, metric in enumerate(metrics, start=1):
            plt.subplot(2, 3, i)
            plt.title(f'{metric} Weekly Average (Week {week})')
            plt.xlabel('Player Name')
            plt.ylabel(f'{metric}')
            
            #Average values
            week_data_avg = data.groupby(['Week', 'Player Name'])[metric].mean().reset_index()
            week_data_avg = week_data_avg[week_data_avg['Week'] == week]
            if not week_data_avg.empty:
                plt.bar(week_data_avg['Player Name'], week_data_avg[metric], color=colors[i-1], label='Average')
                plt.xticks(rotation=45, ha='right')
                
                #Adjust y-axis limit based on the metric
                if metric == 'Top Speed':
                    plt.ylim(10, 24)  # Set y-axis limit for Top Speed
                else:
                    plt.ylim(0, week_data_avg[metric].max() * 1.5)  # Set y-axis limit based on maximum weekly average multiplied by 1.5
                
                #Standard deviation lines
                plt.axhline(y=average_overall[metric] + std_overall[metric], color='black', linestyle='--')
                plt.axhline(y=average_overall[metric] - std_overall[metric], color='black', linestyle='--')
                
                #Solid black line for overall average
                plt.axhline(y=average_overall[metric], color='black', linestyle='-')
            
            plt.legend()
            plt.tight_layout()
        
       
        if not week_data_avg.empty:
            pdf.savefig()
            plt.close()

