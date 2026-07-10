#!/usr/bin/env python3

import matplotlib.pyplot as plt

FILES = [
    ("errors_jump.dat", r"Cifani $\rho_{\mathrm{ratio}} = 1000$"),
    ("errors.dat", r"Baseline $\rho_{\mathrm{ratio}} = 1000$"),
]

def main():
    fig, axes = plt.subplots(2, 1, sharex=True)

    for filename, label in FILES:
        with open(filename) as file:
            data = [
                list(map(float, line.split()))
                for line in file
                if line.strip()
            ]

        time = [row[0] for row in data]
        velocity = [row[2] for row in data]
        divergence = [row[3] for row in data]

        axes[0].plot(time, velocity, label=label)
        axes[1].plot(time, divergence, label=label)

    axes[0].set_ylabel(r"$\|V_{\mathrm{rms}}\|_2$")
    axes[1].set_ylabel(r"$\|\mathrm{div}\,V\|_2$")
    axes[1].set_xlabel("Time")
    axes[1].set_yscale("log")

    for axis in axes:
        axis.grid(True, which="both")
        axis.legend()

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
