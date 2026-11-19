import argparse
import pathlib
import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot
import numpy

import load_runs


PNG_DPI: int = 300


# one file pair per run, e.g. single_convergence_berlin52_run1.png
def output_files(run: load_runs.Run) -> tuple[pathlib.Path, pathlib.Path]:
    stem: str = f"single_convergence_{run.instance}_run{run.number}"
    return load_runs.PLOTS_DIR / f"{stem}.png", load_runs.PLOTS_DIR / f"{stem}.svg"


def plot_convergence(run: load_runs.Run) -> matplotlib.figure.Figure:
    fig: matplotlib.figure.Figure
    ax: matplotlib.axes.Axes
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 5))

    generations: numpy.ndarray = numpy.array([generation.number for generation in run.generations])
    fitnesses: numpy.ndarray = numpy.array([generation.elite_fitness for generation in run.generations])

    # steps, not a line; the elite only changes when a better tour is found
    ax.step(
        generations,
        fitnesses,
        where="post",
        linewidth=1.5,
        color="tab:blue",
        label="Elite tour fitness",
    )

    # optimum line and percent error axis only when the optimum is known
    if run.optimal is not None:
        optimal: int = run.optimal
        ax.axhline(
            optimal,
            linestyle="--",
            linewidth=1,
            color="black",
            label=f"Optimal ({optimal})",
        )

        secondary: matplotlib.axes.Axes = ax.secondary_yaxis(
            "right",
            functions=(
                lambda length: (length - optimal) * 100.0 / optimal,
                lambda error: optimal * (1 + error / 100.0),
            ),
        )

        secondary.set_ylabel("Percent error (%)")

    error_text: str = "" if run.percent_error is None else f", {run.percent_error:.2f}% Error"

    ax.margins(load_runs.AXIS_MARGIN)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Tour fitness")
    ax.set_title(f"{run.instance} Run {run.number} Convergence ({run.dimension} Nodes{error_text})")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right")
    
    fig.tight_layout()
    return fig


def save_plot(fig: matplotlib.figure.Figure, run: load_runs.Run) -> pathlib.Path:
    png_file, svg_file = output_files(run)
    load_runs.PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_file, dpi=PNG_DPI)
    fig.savefig(svg_file)
    return png_file


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Plot the convergence of a single GA run.")
    parser.add_argument(
        "run_file",
        type=pathlib.Path,
        help="path to a run file, e.g. stdout/runs/berlin52/run1.txt",
    )

    args: argparse.Namespace = parser.parse_args()
    run: load_runs.Run = load_runs.load_run(args.run_file, load_runs.load_optimal_values())
    png_file: pathlib.Path = save_plot(plot_convergence(run), run)
    print(f"plotted {run.instance} run {run.number} ({len(run.generations)} generations) -> {png_file}")
