"""Optional matplotlib visualizations."""

def plot_temperature(records, output_path=None, show=True):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Matplotlib is not installed. Install requirements.txt to enable charts.")
    if not records:
        raise ValueError("There are no records to plot.")
    labels = [f"{r.get('city','?')}\n{r.get('observed_at','')[:10]}" for r in records]
    temps = [float(r.get("temperature_c", 0)) for r in records]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(len(records)), temps, marker="o", linewidth=1.7)
    ax.set_xticks(range(len(records)))
    ax.set_xticklabels(labels, rotation=50, ha="right", fontsize=8)
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Weather Record Temperature Trend")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=140)
    if show:
        plt.show()
    plt.close(fig)
    return output_path


def plot_distribution(records, output_path=None, show=True):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Matplotlib is not installed. Install requirements.txt to enable charts.")
    if not records:
        raise ValueError("There are no records to plot.")
    values = [float(r["temperature_c"]) for r in records if r.get("temperature_c") is not None]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(values, bins=min(10, max(3, len(values)//2)), edgecolor="black")
    ax.set_title("Temperature Distribution")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Number of records")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    if output_path: fig.savefig(output_path, dpi=140)
    if show: plt.show()
    plt.close(fig)
    return output_path
