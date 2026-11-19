import pathlib
import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot
import numpy

import load_runs


PNG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "error_v_dimension.png"
SVG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "error_v_dimension.svg"
PNG_DPI: int = 300


# instances without a known optimum have no percent error; skipped
# median instead of mean; one or two bad runs (fl3795) don't drag the summary
# spread between runs is left to plot_variability_v_dimension.py
def collect_errors(runs_by_instance: dict[str, list[load_runs.Run]]) -> tuple[list[int], list[float]]:
    dimensions: list[int] = []
    medians: list[float] = []

    for runs in runs_by_instance.values():
        errors: list[float] = [
            run.percent_error for run in runs
            if run.percent_error is not None
        ]

        if not errors:
            continue

        dimensions.append(runs[0].dimension)
        medians.append(float(numpy.median(errors)))

    return dimensions, medians


def plot_errors(dimensions: list[int], medians: list[float]) -> matplotlib.figure.Figure:
    fig: matplotlib.figure.Figure
    ax: matplotlib.axes.Axes
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 5))
    ax.scatter(
        dimensions,
        medians,
        s=20,
        color="tab:blue",
        label="Median of 10 runs",
    )

    # log x-axis; dimensions span 51 to 18512, linear axis would crowd most instances on the left
    ax.set_xscale("log")
    ax.margins(load_runs.AXIS_MARGIN)
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Percent error (%)")
    ax.set_title("Percent Error vs. Number of Nodes")
    ax.grid(True, which="major", alpha=0.3)
    ax.legend(loc="upper left")
    
    fig.tight_layout()
    return fig


def save_plot(fig: matplotlib.figure.Figure) -> None:
    load_runs.PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_FILE, dpi=PNG_DPI)
    fig.savefig(SVG_FILE)


if __name__ == "__main__":
    dimensions, medians = collect_errors(load_runs.load_runs())
    save_plot(plot_errors(dimensions, medians))
    print(f"plotted {len(dimensions)} instances -> {load_runs.PLOTS_DIR}")
