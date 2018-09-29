import pickle
import datetime
import matplotlib.pyplot as plt

with open('session_1538229902.pickle', 'rb') as f:
    data = pickle.load(f)

time, speed, throttle, steer, brake, clutch, gear, engine, drs = zip(*data[3])

lap_time = str(datetime.timedelta(seconds=time[-1]))[3:]
ticks = [time[i] for i in range(0, len(time), len(time) // 10)]

plt.subplot(4, 1, 1)
plt.title("Lap time: {}".format(lap_time), fontsize=20)
plt.plot(time, speed)
plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])
plt.ylabel('speed (km/h)')

plt.subplot(4, 1, 2)
plt.plot(time, throttle, color='g')
plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])
plt.ylabel('throttle (0-100)')

plt.subplot(4, 1, 3)
plt.plot(time, brake, color='r')
plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])
plt.ylabel('brake (0-100)')

plt.subplot(4, 1, 4)
plt.plot(time, gear, color='b')
plt.xlabel('time (sec)')
plt.ylabel('gear (1-8)')
plt.yticks(range(1, 9), range(1, 9))

plt.xticks(ticks, [str(datetime.timedelta(seconds=t))[3:7] for t in ticks])

plt.show()
