import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for thread-safety and web servers
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    
    def __init__(self, colors: list):
        self.colors = colors

    def summary_pie_chart(self, rfmSummary: pd.DataFrame):
        'Plot rfmSummary pie chart for percentage'
        explode = [0]*len(rfmSummary['Segment_count'])
        explode[rfmSummary['Segment_count'].idxmax()] = 0.2

        fig, ax = plt.subplots(figsize=(10, 10))
        
        wedges, texts, autotexts = ax.pie(
            x=rfmSummary['Segment_count'],
            labels=rfmSummary['Segment'],
            autopct='%.2f%%',
            explode=explode,
            shadow=True,
            colors=self.colors
        )

        # Change percentage text color to white
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
            autotext.set_fontsize(12)

        ax.legend(loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
        return fig
        
    def summary_bar_chart(self, rfmSummary: pd.DataFrame):
        'Plot rfmSummary bar chart for count'
        
        fig, ax = plt.subplots(figsize=(11, 7))
        bar_plot = sns.barplot(data=rfmSummary, x='Segment_count', y='Segment', palette='viridis', ax=ax)
        bar_plot.bar_label(bar_plot.containers[0], fmt='%d')
        return fig