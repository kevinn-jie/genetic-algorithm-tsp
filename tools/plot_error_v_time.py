import pathlib
import matplotlib.axes
import matplotlib.collections
import matplotlib.colors
import matplotlib.figure
import matplotlib.legend
import matplotlib.pyplot
import numpy

import load_runs


PNG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "error_v_time.png"
SVG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "error_v_time.svg"
PNG_DPI: int = 300


# instances without a known optimum have no percent error; skipped
# medians of each instance's runs; matches plot_error_v_dimension.py and plot_time_v_dimension.py
def collect_errors_and_times(runs_by_instance: dict[str, list[load_runs.Run]]) -> tuple[list[int], list[float], list[float]]:
    dimensions: list[int] = []
    median_times: list[float] = []
    median_errors: list[float] = []

    for runs in runs_by_instance.values():
        errors: list[float] = [
            run.percent_error for run in runs
            if run.percent_error is not None
        ]

        if not errors:
            continue

        dimensions.append(runs[0].dimension)
        median_times.append(float(numpy.median([run.compute_time for run in runs])))
        median_errors.append(float(numpy.median(errors)))

    return dimensions, median_times, median_errors


def plot_errors_and_times(dimensions: list[int], median_times: list[float], median_errors: list[float]) -> matplotlib.figure.Figure:
    fig: matplotlib.figure.Figure
    ax: matplotlib.axes.Axes
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 5))

    # colour = number of nodes on a log scale; links this plot back to the two dimension plots
    points: matplotlib.collections.PathCollection = ax.scatter(
        median_times,
        median_errors,
        s=20,
        c=dimensions,
        cmap="viridis",
        norm=matplotlib.colors.LogNorm(),
        label="Median of 10 runs",
    )

    fig.colorbar(points, ax=ax, label="Number of nodes")

    # log x-axis; times span 0.001 s to over 100 s
    ax.set_xscale("log")
    ax.margins(load_runs.AXIS_MARGIN)
    ax.set_xlabel("Compute time (seconds)")
    ax.set_ylabel("Percent error (%)")
    ax.set_title("Percent Error vs. Compute Time")
    ax.grid(True, which="major", alpha=0.3)
    legend: matplotlib.legend.Legend = ax.legend(loc="upper left")

    # legend marker would otherwise take the colormap's lowest colour; neutral grey implies no particular size
    # handle keeps the colormap mapping; clear it first or the fill colour is overridden
    legend_marker: matplotlib.collections.PathCollection = legend.legend_handles[0]
    legend_marker.set_array(None)
    legend_marker.set_color("tab:gray")
    
    fig.tight_layout()
    return fig


def save_plot(fig: matplotlib.figure.Figure) -> None:
    load_runs.PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_FILE, dpi=PNG_DPI)
    fig.savefig(SVG_FILE)


if __name__ == "__main__":
    dimensions, median_times, median_errors = collect_errors_and_times(load_runs.load_runs())
    save_plot(plot_errors_and_times(dimensions, median_times, median_errors))
    print(f"plotted {len(dimensions)} instances -> {load_runs.PLOTS_DIR}")
