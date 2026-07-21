import asyncio

import numpy as np


async def plot_bpm_data(fig, axes, vec, data, writer):
    ax_x, ax_y, ax_sum = axes
    for ax in axes:
        ax.clear()
    for bpm_name, d_for_bpm in data.items():
        ax_x.set_title(f"start vec {vec}")
        turns = np.arange(len(d_for_bpm["x"]["value"]))
        ax_x.plot(turns, d_for_bpm["x"]["value"], label=bpm_name)
        ax_y.plot(turns, d_for_bpm["y"]["value"], label=bpm_name)
        ax_sum.plot(turns, d_for_bpm["sum"]["value"], label=bpm_name)
        # give everything else a chance to run
        fig.canvas.draw()
        frame = np.asarray(fig.canvas.buffer_rgba())
        writer.append_data(frame)
        await asyncio.sleep(0)
    ax_x, ax_y, ax_sum = axes
    ax_x.set_ylabel("x [m]")
    ax_y.set_ylabel("y [m]")
    ax_sum.set_ylabel("sum [rel]")
    ax_sum.set_xlabel("turn")
    del ax_x, ax_y, ax_sum
    # ax_x.legend()
    # ax_y.legend()
    # ax_sum.legend()
