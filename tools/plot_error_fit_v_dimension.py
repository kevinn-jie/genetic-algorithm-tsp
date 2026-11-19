import pathlib
import matplotlib.axes
import matplotlib.figure
import matplotlib.legend
import matplotlib.pyplot
import numpy

import load_runs
import plot_error_v_dimension


PNG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "error_fit_v_dimension.png"
SVG_FILE: pathlib.Path = load_runs.PLOTS_DIR / "error_fit_v_dimension.svg"
PNG_DPI: int = 300


# least-squares line through (ln n, error); returns (slope, intercept) of error = intercept + slope * ln n
# every instance used, 0% included; unlike a power law, no logarithm of the error is taken
def fit_log_linear(dimensions: numpy.ndarray, medians: numpy.ndarray) -> tuple[float, float]:
    slope, intercept = numpy.polyfit(numpy.log(dimensions), medians, 1)
    return float(slope), float(intercept)


def plot_errors_fit(dimensions: list[int], medians: list[float]) -> matplotlib.figure.Figure:
    dimensions_array: numpy.ndarray = numpy.array(dimensions)
    medians_array: numpy.ndarray = numpy.array(medians)

    # Pearson r between percent error and ln n; r^2 is the fit's R^2
    r: float = float(numpy.corrcoef(numpy.log(dimensions_array), medians_array)[0, 1])
    slope, intercept = fit_log_linear(dimensions_array, medians_array)

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
        intercept + slope * numpy.log(fit_dimensions),
        color="black",
        linestyle="-",
        linewidth=1.5,
        label=f"Linear fit: error = {intercept:.2f} + {slope:.3f} ln n (r = {r:.2f}, R² = {r ** 2:.2f})",
    )

    # log x-axis, linear y-axis; the ln n fit appears as a straight line
    ax.set_xscale("log")
    ax.margins(load_runs.AXIS_MARGIN)
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Percent error (%)")
    ax.set_title("Percent Error vs. Number of Nodes")
    ax.grid(True, which="major", alpha=0.3)
    
    legend: matplotlib.legend.Legend = ax.legend(loc="upper left")
    fig.tight_layout()
    fit_legend_above_data(fig, ax, legend, medians_array)
    return fig


# y-limits from the data, not the fit; the fit dips below 0% at small n and would otherwise stretch the axis down
# margin below the data, and between the data and the legend, matches the other plots' AXIS_MARGIN as a fraction of the axis height; ax.margins gives AXIS_MARGIN / (1 + 2 * AXIS_MARGIN) of the axis on each side
def fit_legend_above_data(fig: matplotlib.figure.Figure, ax: matplotlib.axes.Axes, legend: matplotlib.legend.Legend, medians: numpy.ndarray) -> None:
    fig.canvas.draw()
    legend_height: float = 1.0 - legend.get_window_extent().transformed(ax.transAxes.inverted()).y0
    margin: float = load_runs.AXIS_MARGIN / (1.0 + 2.0 * load_runs.AXIS_MARGIN)

    data_range: float = float(medians.max() - medians.min())
    span: float = data_range / (1.0 - 2.0 * margin - legend_height)
    bottom: float = float(medians.min()) - margin * span
    ax.set_ylim(bottom, bottom + span)


def save_plot(fig: matplotlib.figure.Figure) -> None:
    load_runs.PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_FILE, dpi=PNG_DPI)
    fig.savefig(SVG_FILE)


if __name__ == "__main__":
    dimensions, medians = plot_error_v_dimension.collect_errors(load_runs.load_runs())
    save_plot(plot_errors_fit(dimensions, medians))
    print(f"plotted {len(dimensions)} instances -> {load_runs.PLOTS_DIR}")
