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

        plt.figure(figsize=(10, 10))
        wedges, texts, autotexts = plt.pie(
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

        plt.legend(loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.tight_layout()
        plt.show()
        
    def summary_bar_chart(self, rfmSummary: pd.DataFrame):
        'Plot rfmSummary bar chat for count'
        plt.figure(figsize=(11, 7))
        bar_plot = sns.barplot(data=rfmSummary, x='Segment_count', y='Segment', palette='viridis')
        bar_plot.bar_label(bar_plot.containers[0], fmt='%d')
        plt.show()