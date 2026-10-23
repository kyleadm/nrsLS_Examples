from cycler import cycler
import time

import matplotlib as mpl
mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def plotnow(
    filename,
    xlabel,
    ylabel,
    x,
    y,
    label,
    ptype="semilogy",
    linestyle="-",
    marker="",
    ylim=None,
    xlim=None,
):
    default_cycler = cycler(
        color=[
            "#0072B2",
            "#D55E00",
            "#009E73",
            "#CC79A7",
            "#6A3D9A",
            "#E7298A",
            "#A6761D",
            "#000000",
        ]
    )

    plt.rc("lines", linewidth=1)
    plt.rc("axes", prop_cycle=default_cycler)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlabel(xlabel, fontsize=15)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.tick_params(axis="both", labelsize=12)

    if ylim is not None:
        ax.set_ylim(ylim)

    if xlim is not None:
        ax.set_xlim(xlim)

    plot_options = {
        "label": label,
        "linestyle": linestyle,
        "marker": marker,
        "linewidth": 2.0,
    }

    if ptype == "line":
        ax.plot(x, y, **plot_options)
    elif ptype == "semilogx":
        ax.semilogx(x, y, **plot_options)
    elif ptype == "semilogy":
        ax.semilogy(x, y, **plot_options)
    elif ptype == "loglog":
        ax.loglog(x, y, **plot_options)
    else:
        raise ValueError(
            "ptype must be 'line', 'semilogx', 'semilogy', or 'loglog'"
        )

    ax.grid(which="both", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.legend(loc="best", fontsize=12)

    fig.savefig(
        filename + ".png",
        bbox_inches="tight",
        dpi=400,
    )

    plt.close(fig)


def extract_data(filename):
    data = np.loadtxt(filename)

    if data.ndim == 1:
        data = data.reshape(1, -1)

    if data.shape[1] < 4:
        raise ValueError(
            f"{filename} must contain at least four columns. "
            f"Found {data.shape[1]} columns."
        )

    simulation_time = data[:, 0]
    velocity_norm = data[:, 2]
    divergence_error = data[:, 3]

    return simulation_time, velocity_norm, divergence_error


def main():
    input_file = "errors-frozen.dat"

    simulation_time, velocity_norm, divergence_error = extract_data(
        input_file
    )

    plotnow(
        filename="velocity_norm",
        xlabel=r"$t$",
        ylabel=r"$\|V\|_{L_2}$",
        x=simulation_time,
        y=velocity_norm,
        label="Velocity norm",
        ptype="semilogy",
        ylim=(1e-4, 1),
    )

    plotnow(
        filename="divergence_error",
        xlabel=r"$t$",
        ylabel=r"$\|\nabla \cdot V\|_{L_2}$",
        x=simulation_time,
        y=divergence_error,
        label="Divergence error",
        ptype="semilogy",
        ylim=(1e-4, 1),
    )


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- Code ran in {time.time() - start_time:.3f} seconds ---")
