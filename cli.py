#!/usr/bin/env python3.6

import argparse
import sys

from pytelemetry.listen import Telemetry
from pytelemetry.inspect import Inspector


class CLI:

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Command line interface for PyTelemetry',
            usage=('python3.6 cli.py <command> [<args>]\n'
                   '\n'
                   'listen      Register session data\n'
                   'inspect     Inspect session data\n'))
        parser.add_argument('command', type=str, help='Sub-command to run',
                            choices=['listen', 'inspect'])

        args = parser.parse_args(sys.argv[1:2])
        command = args.command.replace('-', '_')
        if not hasattr(self, command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, command)()

    @staticmethod
    def listen() -> None:
        telemetry = Telemetry()
        try:
            telemetry.save_data()
        except KeyboardInterrupt:
            telemetry.save_before_exit()

    @staticmethod
    def inspect() -> None:
        parser = argparse.ArgumentParser(description='Inspect session data')
        parser.add_argument('session', type=str, help='Session file to inspect')
        parser.add_argument('action', type=str, help='Possible inspections',
                            choices=['bestlap', 'laptimes', 'lap'])
        parser.add_argument('--lap', type=int, help='Lap to inspect')
        parser.add_argument('--vs-best', type=bool, help='Compare to best lap')

        args = parser.parse_args(sys.argv[2:])
        inspector = Inspector(args.session)
        if args.action == 'laptimes':
            inspector.show_lap_times()
        if args.action == 'lap':
            inspector.show_lap(args.lap, args.vs_best)
        if args.action == 'bestlap':
            inspector.show_best_lap()


if __name__ == '__main__':
    CLI()
