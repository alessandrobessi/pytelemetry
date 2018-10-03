import datetime
import pickle

import matplotlib.pyplot as plt

from pytelemetry.helpers import get_lap_time


class Viewer:

    def __init__(self, session: str):
        self.session = session
        with open(self.session, 'rb') as f:
            self.data = pickle.load(f)

        self.best_lap = self._get_best_lap()

    def _get_best_lap(self) -> int:
        best_k = 0
        best_lap = 9999
        for k, v in self.data.items():
            lap_time = get_lap_time(v, return_float=True)
            if 60 < lap_time < best_lap:
                best_lap = lap_time
                best_k = k
        return best_k

    def show_lap_times(self) -> None:
        for k, v in self.data.items():
            print("Lap {}: {}".format(k, get_lap_time(v)))

    def show_lap(self, lap: int, vs_best: bool = False) -> None:
        time, speed, throttle, _, brake, _, gear, _, _ = zip(*self.data[lap])

        if vs_best:
            b_time, b_speed, b_throttle, _, b_brake, _, b_gear, _, _ = zip(*self.data[
                self.best_lap])

        lap_time = get_lap_time(self.data[lap])
        best_lap_time = get_lap_time(self.data[self.best_lap])

        ticks = [time[i] for i in range(0, len(time), len(time) // 10)]

        plt.subplot(4, 1, 1)
        if vs_best:
            plt.title("Lap {}: {} (Best Lap: {})".format(lap, lap_time, best_lap_time), fontsize=20)
        else:
            plt.title("Lap {}: {}".format(lap, lap_time), fontsize=20)

        plt.plot(time, speed, color='b', label='Lap {}'.format(lap))
        if vs_best:
            plt.plot(b_time, b_speed, color='k', label='Best Lap')
        plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])
        plt.ylabel('speed (km/h)')
        plt.legend(loc='upper left')

        plt.subplot(4, 1, 2)
        plt.plot(time, throttle, color='b', label='Lap {}'.format(lap))
        if vs_best:
            plt.plot(b_time, b_throttle, color='k', label='Best Lap')
        plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])
        plt.ylabel('throttle (0-100)')
        plt.legend(loc='upper left')

        plt.subplot(4, 1, 3)
        plt.plot(time, brake, color='b', label='Lap {}'.format(lap))
        if vs_best:
            plt.plot(b_time, b_brake, color='k', label='Best Lap')
        plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])
        plt.ylabel('brake (0-100)')
        plt.legend(loc='upper left')

        plt.subplot(4, 1, 4)
        plt.plot(time, gear, color='b', label='Lap {}'.format(lap))
        if vs_best:
            plt.plot(b_time, b_gear, color='k', label='Best Lap')
        plt.xlabel('time')
        plt.ylabel('gear (1-8)')
        plt.yticks(range(1, 9), range(1, 9))
        plt.legend(loc='upper left')

        plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])

        plt.show()

    def show_best_lap(self) -> None:
        self.show_lap(lap=self.best_lap)
