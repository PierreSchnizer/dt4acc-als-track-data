"""
Todo:
    all the grouping code should not be here
    the bpm device should put data into a data model
    then here the data model would only be used ....
"""

import imageio.v2 as imageio
import matplotlib
import logging

from dt4acc_als.managers_input.dt4acc_bootstrap import load_managers
from dt4acc_als_track_data.ophyd_async_devices_setup import setup
from dt4acc_als_track_data.view.plot_bpm_data import plot_bpm_data
from dt4acc_als_track_data.view.preprocess_data import all_data_in_one_dict, group_data

logging.basicConfig(level=logging.WARNING)

import asyncio
import numpy as np

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from dt4acc_lib.model.output.track import ParticleState
from matplotlib import pyplot as plt

# need to use 'macosx' on MAC
# matplotlib.use('qt5cairo')
matplotlib.use("QtAgg")
logger = logging.getLogger("accml_test")

app = QApplication([])

writer = imageio.get_writer("output.mp4", fps=30)


async def main():
    yp, lm, ts, epics_vars = load_managers()
    devices = setup()
    # ON BESSY II machine
    # devices = setup(prefix="")
    # On Twin None ... means default

    devices = setup(prefix=None)
    tbt_bpms = devices.get("tbt_bpms")
    # Need to find out why these don't have data
    excluded_bpms = [
        "SR01C:BPM2",
        "SR01C:BPM6",
        "SR03C:BPM2",
        "SR03C:BPM7",
        "SR04C:BPM1",
        "SR04C:BPM2",
        "SR04C:BPM7",
        "SR04C:BPM8",
        "SR06C:BPM1",
        "SR06C:BPM2",
        "SR06C:BPM7",
        "SR06C:BPM8",
        "SR07C:BPM1",
        "SR07C:BPM2",
        "SR07C:BPM7",
        "SR07C:BPM8",
        "SR11C:BPM1",
        "SR11C:BPM2",
        "SR11C:BPM7",
        "SR11C:BPM8",
    ]

    tbt_bpms = {
        bpm_name: dev
        for bpm_name, dev in tbt_bpms.items()
        if bpm_name not in excluded_bpms
    }
    # Interface to configure how it runs
    turn_by_turn = devices.get("turn_by_turn")
    await turn_by_turn.connect()

    await asyncio.gather(*[bpm.connect() for bpm in tbt_bpms.values()])

    # I should rather check if these are really triggerable
    triggerable_devices = list(tbt_bpms.values())
    all_devices = triggerable_devices + [turn_by_turn]
    d = await asyncio.gather(*[dev.describe() for dev in all_devices])
    r = await asyncio.gather(*[dev.read() for dev in all_devices])

    # NB:
    #   if you want to read back your data with bluesky databroker
    #   only change this value at the beginning!
    await turn_by_turn.n_turns.set(2000)

    # could use the particle state here too
    vecs = [
        ParticleState.from_sequence([16.800e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.809e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8091e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8092e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8093e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8094e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8095e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8096e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8097e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8098e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.8099e-3, 0, 0, 0, 0, 0]),
        ParticleState.from_sequence([16.810e-3, 0, 0, 0, 0, 0]),
        # ParticleState.from_sequence([17.0e-3, 0, 0, 0, 0, 0]),
    ]
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=[16, 8])


    for run_id, vec in enumerate(vecs):
        # Adhering to bluesky protocol: trigger shall be called if
        # one wants to "trigger" for new data (or wait for it)
        await turn_by_turn.start_vec.set(vec.as_array())
        # don't forget to trigger turn by turn data calculation
        # and integer should be good, better to use a meaningful one
        await turn_by_turn.run.set(run_id)
        # need to launch that already ... so it gets the data
        # when they arrive
        future_bpm_tbt_ready = asyncio.gather(*[dev.trigger() for dev in triggerable_devices])
        if run_id > 0:
            # some time for to inspect the data
            # wait here: the twin can calculate in parallel
            for i in range(30 * 5):
                # 30 frames per second ...
                await asyncio.sleep(1/30.)
                # so that one can see for a few seconds what's there
                frame = np.asarray(fig.canvas.buffer_rgba())
                writer.append_data(frame)
        await future_bpm_tbt_ready
        data = await asyncio.gather(*[dev.read() for dev in all_devices])
        data = all_data_in_one_dict(data)
        non_bpm_data, bpm_data = group_data(data)
        future = asyncio.get_running_loop().create_future()

        def on_draw(event):
            if not future.done():
                future.set_result(None)

        cid = fig.canvas.mpl_connect("draw_event", on_draw)

        print(f"Data for {vec=}...", end="")
        await plot_bpm_data(fig, axes, vec, bpm_data, writer)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        await future
        fig.canvas.mpl_disconnect(cid)
        print("done")


if __name__ == "__main__":
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    plt.ion()
    try:
        with loop:
            loop.run_until_complete(main())
        writer.close()
    except Exception as e:
        logger.error(f"Failed to run {__file__}.main: {e}")
        print("Close plot for full backtrace")
        plt.ioff()
        plt.show()
        raise e
    else:
        print("Close plot to stop program")
        plt.ioff()
        plt.show()
