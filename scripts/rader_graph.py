import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data for the radar chart
data_models = {
    "Model": [
        "GPT-3.5",
        "GPT-4o-mini",
        "Llama3.1-70B",
        "Llama3.1-8B",
        "Llama3.3-70B"
    ],
    "Communication Score": [3.942982456, 4.2, 4.5, 3.913043478, 4.5625],
    "Planning Score": [4.267730496, 4.369047619, 4.29, 4.14, 4.39],
    "KPI Average": [0.650927501, 0.754936697, 0.810828267, 0.646348262, 0.744687566],
    "Average Total Milestones": [4.833333333, 5.904761905, 4.893617021, 3.895833333, 4.6],
    "Average Innovation": [4.680851064, 4.880952381, 4.72, 4.64, 4.7],
    "Average Safety": [3.914893617, 3.928571429, 3.76, 3.88, 3.92],
    "Average Feasibility": [3.808510638, 3.904761905, 3.94, 3.86, 3.86],
    "Average Task Score": [4.134751773, 4.238095238, 4.14, 4.126666667, 4.16],
    "Token Usage (/10,000)": [
        113625.3404 / 10000,
        86983.45238 / 10000,
        94608.24 / 10000,
        91297.94 / 10000,
        157659.68 / 10000
    ]
}
# Function to plot radar chart with independent scales and labeled radial ticks for each category
def plot_radar_with_individual_scales(data, title, key_label="Model"):
    df = pd.DataFrame(data)
    categories = list(data.keys())[1:]  # Exclude the first column
    num_vars = len(categories)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Calculate the maximum value for each category
    max_values = [df[cat].max() for cat in categories]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Plot each model
    for idx, row in df.iterrows():
        values = row[categories].tolist()
        normalized_values = [v / max_val for v, max_val in zip(values, max_values)]
        normalized_values += normalized_values[:1]  # Repeat the first value to close the circular graph
        ax.plot(angles, normalized_values, label=row[key_label])
        ax.fill(angles, normalized_values, alpha=0.25)

    # Add axis labels and radial ticks
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        [f"{cat}\n(0-{max_val:.1f})" for cat, max_val in zip(categories, max_values)],
        fontsize=10,
    )

    # Add radial ticks for each category
    for i, (angle, max_val) in enumerate(zip(angles[:-1], max_values)):
        ticks = [0.2, 0.4, 0.6, 0.8, 1.0]  # Radial tick positions (normalized)
        tick_values = [tick * max_val for tick in ticks]  # Scale to max value
        for tick, tick_value in zip(ticks, tick_values):
            ax.text(
                angle,
                tick,  # Radial position (normalized)
                f"{tick_value:.1f}",  # Tick value
                fontsize=8,
                ha="center",
                va="center",
                color="gray",
            )

    # Remove default radial labels and set y-limits
    ax.set_yticks([])  # Hide y-axis labels
    ax.set_ylim(0, 1)

    # Add legend
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=10)

    # Title
    plt.title(title, size=14, weight="bold")

    return fig


# Plot the radar chart
plot_radar_with_individual_scales(
    data_models,
    title="Comparison of Models Using Graph Protocol"
)

# Show the plot
plt.show()
