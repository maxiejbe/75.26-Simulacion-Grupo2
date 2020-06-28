import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


def percentage(percentage, total):
    return total / 100 * percentage


def draw(S, I, R, N, t, health_system_capacity):
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, facecolor="#dddddd", axisbelow=True)
    ax.plot(t, S / N * 100, "b", alpha=0.5, lw=2, label="Susceptible")
    ax.plot(t, I / N * 100, "r", alpha=0.5, lw=2, label="Infected")
    ax.plot(t, R / N * 100, "g", alpha=0.5, lw=2, label="Recovered with immunity")
    ax.plot(
        t,
        health_system_capacity,
        "black",
        alpha=0.5,
        lw=2,
        label="Health system capacity",
    )
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Population percentage")
    ax.set_ylim(0, 120)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which="major", c="w", lw=2, ls="-")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)
    plt.show()


def main():
    # N: Total population.
    N = 40000000
    # 1 year
    days = 160
    # I0: 3% of the population. R0: 0 recovered.
    I0, R0 = percentage(3, N), 0
    # All the population (but the infected) is susceptible initially.
    S0 = N - I0 - R0
    # Contact rate (beta), Recovery rate (gamma).
    beta, gamma = 0.27, 0.043
    # Elapsed time in days
    t = np.linspace(0, days, days)
    health_system_capacity = [30] * days

    # Initial conditions vector
    y0 = S0, I0, R0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    draw(S, I, R, N, t, health_system_capacity)


if __name__ == "__main__":
    main()
