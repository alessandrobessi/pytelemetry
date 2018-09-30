import logging
import socket
import netifaces as ni
import pickle
import datetime

from pytelemetry.f1_2018_struct import *
from pytelemetry.helpers import get_lap_time

logging.basicConfig(level=logging.INFO)


class Telemetry:

    @staticmethod
    def parse_lap_data(packet):
        data = list()
        data.append(packet.laps_data[0].m_currentLapTime)
        return data

    @staticmethod
    def parse_car_telemetry_packet(packet):
        data = list()
        data.append(packet.cars_telemetry_data[0].m_speed)
        data.append(packet.cars_telemetry_data[0].m_throttle)
        data.append(packet.cars_telemetry_data[0].m_steer)
        data.append(packet.cars_telemetry_data[0].m_brake)
        data.append(packet.cars_telemetry_data[0].m_clutch)
        data.append(packet.cars_telemetry_data[0].m_gear)
        data.append(packet.cars_telemetry_data[0].m_engineRPM)
        data.append(packet.cars_telemetry_data[0].m_drs)
        return data

    def __init__(self, port: int = 20777):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ni.ifaddresses('wlp58s0')[ni.AF_INET][0]['addr']
        self.socket.bind((self.ip, port))
        self.buffer_size = 1341

        self.laps_dict = dict()
        self.lap_count = 0
        self.laps_dict[self.lap_count] = list()

        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    def listen(self) -> None:
        logging.info("{} is listening on port {} ... ".format(
            self.ip, self.port))

        while True:
            data, _ = self.socket.recvfrom(self.buffer_size)
            header = Header.from_buffer_copy(data[0:21])
            if int(header.m_packetId) == 0:
                packet = PacketMotionData.from_buffer_copy(data[0:1341])

            elif int(header.m_packetId) == 1:
                packet = PacketSessionData.from_buffer_copy(data[0:147])

            elif int(header.m_packetId) == 2:
                packet = PacketLapData.from_buffer_copy(data[0:841])
                yield 'lap_data', Telemetry.parse_lap_data(packet)

            elif int(header.m_packetId) == 3:
                packet = PacketEventData.from_buffer_copy(data[0:25])

            elif int(header.m_packetId) == 4:
                packet = PacketParticipantsData.from_buffer_copy(data[0:1082])

            elif int(header.m_packetId) == 5:
                packet = PacketCarSetupData.from_buffer_copy(data[0:841])

            elif int(header.m_packetId) == 6:
                packet = PacketCarTelemetryData.from_buffer_copy(data[0:1085])
                yield 'telemetry', Telemetry.parse_car_telemetry_packet(packet)

            elif int(header.m_packetId) == 7:
                packet = PacketCarStatusData.from_buffer_copy(data[0:1061])

    def save_data(self) -> None:
        file_path = '../sessions/session_{}.pickle'.format(self.now)

        for packet_type, packet_data in self.listen():
            if packet_type == 'lap_data' and packet_data[0] < 0.01:
                if self.lap_count > 0:
                    logging.info("Saving Lap {} data".format(self.lap_count))
                    with open(file_path, 'wb') as f:
                        pickle.dump(self.laps_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
                self.lap_count += 1
                self.laps_dict[self.lap_count] = list()

            if packet_type == 'lap_data':
                buffer = list()
                buffer.append(packet_data[0])

            if packet_type == 'telemetry':
                buffer.extend(packet_data)
                self.laps_dict[self.lap_count].append(tuple(buffer))

    def save_before_exit(self) -> None:
        file_path = '../sessions/session_{}_lap_times.txt'.format(self.now)
        if len(self.laps_dict.keys()) > 1:
            with open(file_path, 'w') as f:
                for k, v in self.laps_dict.items():
                    f.write("Lap {}: {}\n".format(k, get_lap_time(v)))

            logging.info("Session lap times saved in {}".format(file_path))
