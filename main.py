import time
import logging
import socket
import netifaces as ni
import pickle

from f1_2018_struct import *

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

    def listen(self):
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


if __name__ == '__main__':
    telemetry = Telemetry()
    laps_dict = dict()
    lap_count = 0
    laps_dict[lap_count] = list()

    for packet_type, packet_data in telemetry.listen():
        if packet_type == 'lap_data' and packet_data[0] < 0.01:
            if lap_count > 0:
                logging.info("Saving Lap {} data".format(lap_count))
                with open('session_{}.pickle'.format(int(time.time())), 'wb') as f:
                    pickle.dump(laps_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
            lap_count += 1
            laps_dict[lap_count] = list()

        if packet_type == 'lap_data':
            buffer = list()
            buffer.append(packet_data[0])

        if packet_type == 'telemetry':
            buffer.extend(packet_data)
            laps_dict[lap_count].append(tuple(buffer))



