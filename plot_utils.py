import matplotlib.pyplot as plt

def add_value_labels_outside(ax):
    for rect in ax.patches:
        y_value = rect.get_y() + rect.get_height() / 2
        x_value = rect.get_width()
        label = "{:.1f}".format(x_value)
        ha = 'right' if x_value < 0 else 'left'
        ax.annotate(label + "%", (x_value * 1.01, y_value), va='center', ha=ha)

# Function to plot gamma values
def plot_gamma(df):
    gamma_086 = df[df['Gamma'] == 0.86]
    gamma_170 = df[df['Gamma'] == 1.7]
    gamma_257 = df[df['Gamma'] == 2.57]
    background_color = [14/255, 17/255, 23/255]

    min_percentage = min(df['CO2 Decrease Against Baseline (%)'].min(), df['Time Increase Against Baseline (%)'].min())
    max_percentage = max(df['CO2 Decrease Against Baseline (%)'].max(), df['Time Increase Against Baseline (%)'].max())
    x_limits = (min_percentage * 1.3, max_percentage * 1.3)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 6), facecolor=background_color, sharey=True)
    fig.patch.set_facecolor(background_color)
    #fig.set_facecolor(background_color)

    # Plot for gamma=0.86
    axes[0].barh(gamma_086['Maximum Hubs'], gamma_086['CO2 Decrease Against Baseline (%)'], 0.5, color='darkred', label='CO2')
    axes[0].barh(gamma_086['Maximum Hubs'], gamma_086['Time Increase Against Baseline (%)'], 0.5, color='grey', alpha=0.5, label='Time')
    axes[0].set_xlabel('Percentage Change Against Baseline (%)')
    axes[0].set_title('High Willingness to Trade-off CO2 Longer Travel Times \n for Lower CO2 Emissions (Gamma = 0.86)')
    axes[0].set_yticks(gamma_086['Maximum Hubs'])
    axes[0].set_ylabel('Maximum Number of Hubs')
    axes[0].set_xlim(x_limits)
    axes[0].legend()
    axes[0].set_facecolor(background_color)
    axes[0].grid(True, linewidth=0.4, alpha=0.35)
    axes[0].axvline(x=0, color='white', linewidth=0.5)
    add_value_labels_outside(axes[0])

    
    axes[1].barh(gamma_170['Maximum Hubs'], gamma_170['CO2 Decrease Against Baseline (%)'], 0.5, color='darkred', label='CO2')
    axes[1].barh(gamma_170['Maximum Hubs'], gamma_170['Time Increase Against Baseline (%)'], 0.5, color='grey', alpha=0.5, label='Time')
    axes[1].set_xlabel('Percentage Change Against Baseline (%)')
    axes[1].set_title('Medium Willingness to Trade-off CO2 Longer Travel Times \n for Lower CO2 Emissions (Gamma = 1.7)')
    axes[1].set_yticks(gamma_170['Maximum Hubs'])
    axes[1].set_xlim(x_limits)
    axes[1].legend()
    axes[1].set_facecolor(background_color)
    axes[1].grid(True, linewidth=0.4, alpha=0.35)
    axes[1].axvline(x=0, color='white', linewidth=0.5)
    add_value_labels_outside(axes[1])

    # Plot for gamma=2.57
    axes[2].barh(gamma_257['Maximum Hubs'], gamma_257['CO2 Decrease Against Baseline (%)'], 0.5, color='darkred', label='CO2')
    axes[2].barh(gamma_257['Maximum Hubs'], gamma_257['Time Increase Against Baseline (%)'], 0.5, color='grey', alpha=0.5, label='Time')
    axes[2].set_xlabel('Percentage Change Against Baseline (%)')
    axes[2].set_title('Low Willingness to Trade-off CO2 Longer Travel Times \n for Lower CO2 Emissions (Gamma = 2.57)')
    axes[2].set_yticks(gamma_257['Maximum Hubs'])
    axes[2].set_xlim(x_limits)
    axes[2].legend()
    axes[2].set_facecolor(background_color)
    axes[2].grid(True, linewidth=0.4, alpha=0.35)
    axes[2].axvline(x=0, color='white', linewidth=0.5)
    add_value_labels_outside(axes[2])

    plt.tight_layout()
    return fig