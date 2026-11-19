import pathlib
import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot
import numpy

import load_runs
import plot_time_v_dimension


PNG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "time_fit_v_dimension.png"
SVG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "time_fit_v_dimension.svg"
PNG_DPI: int = 300


# least-squares line through (ln n, ln time); returns (exponent, coefficient) of time = coefficient * n^exponent
def fit_power_law(dimensions: numpy.ndarray, medians: numpy.ndarray) -> tuple[float, float]:
    exponent, intercept = numpy.polyfit(numpy.log(dimensions), numpy.log(medians), 1)
    return float(exponent), float(numpy.exp(intercept))


def plot_times_fit(dimensions: list[int], medians: list[float]) -> matplotlib.figure.Figure:
    dimensions_array: numpy.ndarray = numpy.array(dimensions)
    medians_array: numpy.ndarray = numpy.array(medians)
    exponent, coefficient = fit_power_law(dimensions_array, medians_array)

    fig: matplotlib.figure.Figure
    ax: matplotlib.axes.Axes
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 5))
    ax.scatter(
        dimensions_array,
        medians_array,
        s=20,
        color="tab:blue",
        label="Median of 10 runs",
    )

    fit_dimensions: numpy.ndarray = numpy.geomspace(dimensions_array.min(), dimensions_array.max(), 200)
    ax.plot(
        fit_dimensions,
        coefficient * fit_dimensions ** exponent,
        color="black",
        linestyle="-",
        linewidth=1.5,
        label=f"Power-law fit: time ∝ n^{exponent:.2f}",
    )

    # log-log axes; a power law appears as a straight line whose slope is the exponent
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.margins(load_runs.AXIS_MARGIN)
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Compute time (seconds)")
    ax.set_title("Compute Time vs. Number of Nodes")
    ax.grid(True, which="major", alpha=0.3)
    ax.legend(loc="upper left")
    
    fig.tight_layout()
    return fig


def save_plot(fig: matplotlib.figure.Figure) -> None:
    load_runs.PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_FILE, dpi=PNG_DPI)
    fig.savefig(SVG_FILE)


if __name__ == "__main__":
    dimensions, medians = plot_time_v_dimension.collect_times(load_runs.load_runs())
    save_plot(plot_times_fit(dimensions, medians))
    print(f"plotted {len(dimensions)} instances -> {load_runs.PLOTS_DIR}")
