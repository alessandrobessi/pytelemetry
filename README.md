# PyTelemetry

PyTelemetry is a *F1 2018* telemetry data collector and viewer.

## Current Limitations
- works only in Time Trial mode
- all telemetry data get collected, but only a restricted minority (speed, throttle, brake, gear)
 are effectively used
 
## Contributions
I would love to receive pull requests to improve this package.

## Usage

#### Telemetry Collection
While in **Time Trial** mode, run

`python3 cli.py listen`

to start collecting UDP packages containing telemetry data.

At the end of the session, telemetry data get saved in `sessions/session_{datetime}.pickle`.

#### Telemetry View

##### Lap Times
To view lap times, run:

`python3 cli.py view sessions/session_{datetime}.pickle laptimes`
 
###### Example:
 ```bash
python3 cli.py view sessions/session_20180930_0658.pickle laptimes                  
Lap 0: 0:22.108711
Lap 1: 1:37.755325
Lap 2: 1:38.389503
Lap 3: 1:38.205421
Lap 4: 1:35.920578
Lap 5: 1:37.005081
Lap 6: 1:36.220932
Lap 7: 0:45.324715
Lap 8: 1:35.152802
Lap 9: 1:35.920654
Lap 10: 1:52.969131
Lap 11: 1:36.754654

```

##### Best Lap Telemetry


To view the best lap telemetry, run:

`python3 cli.py view sessions/session_{datetime}.pickle bestlap`

###### Example:

By running

`python3 cli.py view sessions/session_20180930_0658.pickle bestlap`
you get the [following image](https://imgur.com/2ONnsSn).

##### Lap Telemetry
To view the telemetry of a specific lap, run:

`python3 cli.py view sessions/session_{datetime}.pickle lap --lap=9`

To view the telemetry of a specific lap, compared with the telemetry of the best lap, run:

`python3 cli.py view sessions/session_{datetime}.pickle lap --lap=9 --vs-best=true`





