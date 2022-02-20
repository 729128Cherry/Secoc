# coding=utf-8
# @Time    : 2022/1/4
# @Author  : Yi Chen
# @comments  : 本脚本暂未实现E2，需要确定E2E，E2E不在开发

from gevent import monkey
monkey.patch_all()
from zlgcan import *
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
import time
import gevent
from SecXML import MSG


# demo
# secret = b'Sixteen byte key'
# message = b'tigerzhou is very handsome'
#
# print(type(secret))
# c = CMAC.new(secret,message,ciphermod=AES)
# print( c.hexdigest())

# # 经过比对的CMAC_ASE128计算
# secret_key = '0102030405060708090A0B0C0D0E0F10'
# messages = '0021E8030000000000FF05498330'
#
# secret_key_new = bytes.fromhex(secret_key)
# messages_new = bytes.fromhex(messages)
#
# c = CMAC.new(secret_key_new,messages_new,ciphermod=AES)
# print(c.hexdigest())

class Secoc_MAC:
	def __init__(self, key):
		"""
		实例化的时候写入的key，需要与TBOX的一致
		:param key: 秘钥
		"""
		self.key = key

	def encryption(self, APDU):
		"""
		加密算法函数，ASE128-CMAC
		:param APDU: 验证数据单元
		:return: 加密结果
		"""
		return CMAC.new(bytes.fromhex(self.key), bytes.fromhex(APDU),
						ciphermod=AES).hexdigest()


class ZLG:
	def __init__(self):
		self.device = ZCAN()
		self.MAC = Secoc_MAC("0102030405060708090A0B0C0D0E0F10")
		self.flag_transform = False
		self.flag_receive = False

	def open_device(self, type_devcie, channel_num):
		"""
		打开周立功设备的函数
		:param type_devcie: ZLG设备类型
		:param channel_num: 开启的设备通道号
		:return: 设备通道句柄
		"""
		handle = self.device.OpenDevice(type_devcie, 0, 0)
		if handle == INVALID_DEVICE_HANDLE:
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ","Open Device failed!")
			exit(0)
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ","device handle:%d." % handle)
		info = self.device.GetDeviceInf(handle)
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ","Device Information:\n%s" % info)
		chn_handle = can_start(self.device, handle, channel_num)
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ","channel handle:%d." % chn_handle)
		return handle, chn_handle

	def transform_device_cycle(self, chn_handle, dict):
		"""
		发送函数，循环报文
		:param chn_handle: 设备句柄
		:param dict: xml文件中的字典列表
		:return: None
		"""
		while not self.flag_transform:
			global MSG
			time.sleep(dict["period"]/1000)
			canfd_msgs = (ZCAN_TransmitFD_Data * 1)()
			canfd_msgs[0].transmit_type = 1
			canfd_msgs[0].frame.eff = 0
			canfd_msgs[0].frame.rtr = 0
			canfd_msgs[0].frame.brs = 1
			canfd_msgs[0].frame.can_id = int(dict["data_id"][1:], 16)
			canfd_msgs[0].frame.len = len(dict["data"])
			# 取最后1个字节的freshness
			dict["data"][-4] = int(hex(dict["freshness"]).replace("0x", "").zfill(16)[-2:], 16)
			# 加密PDU
			APDU = dict["data_id"]+"".join([hex(i).replace("0x", "").zfill(2) for i in dict["data"][0:len(dict["data"])-4]])+hex(dict["freshness"]).replace("0x", "").zfill(16)
			# 计算MAC
			full_mac = demo.MAC.encryption(APDU)
			# 截取MAC
			dict["data"][-3] = int(full_mac[0:2], 16)
			dict["data"][-2] = int(full_mac[2:4], 16)
			dict["data"][-1] = int(full_mac[4:6], 16)
			for signal_seq in range(canfd_msgs[0].frame.len):
				canfd_msgs[0].frame.data[signal_seq] = dict["data"][signal_seq]
			# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " TX: ", dict)
			self.device.TransmitFD(chn_handle, canfd_msgs, 1)
			dict["freshness"] += 1

	def sync_event_req(self, chn_handle, dict, freshness_ID):
		"""
		:param chn_handle: 设备句柄
		:param dict: 请求同步的信号字典
		:param freshness_ID: 请求同步的FV ID
		:return: None
		"""
		global MSG
		time.sleep(dict["period"]/1000)
		canfd_msgs = (ZCAN_TransmitFD_Data * 1)()
		canfd_msgs[0].transmit_type = 1
		canfd_msgs[0].frame.eff = 0
		canfd_msgs[0].frame.rtr = 0
		canfd_msgs[0].frame.brs = 1
		canfd_msgs[0].frame.can_id = int(dict["data_id"][1:], 16)
		canfd_msgs[0].frame.len = len(dict["data"])
		dict["data"][0] = int(freshness_ID[0:2], 16)
		dict["data"][1] = int(freshness_ID[2:4], 16)
		# 取最后1个字节的freshness
		dict["data"][-4] = 0
		# 加密PDU
		APDU = dict["data_id"]+"".join([hex(i).replace("0x", "").zfill(2) for i in dict["data"][0:len(dict["data"])-4]])+"0000000000000000"
		# 计算MAC
		full_mac = demo.MAC.encryption(APDU)
		# 截取MAC
		dict["data"][-3] = int(full_mac[0:2], 16)
		dict["data"][-2] = int(full_mac[2:4], 16)
		dict["data"][-1] = int(full_mac[4:6], 16)
		for signal_seq in range(canfd_msgs[0].frame.len):
			canfd_msgs[0].frame.data[signal_seq] = dict["data"][signal_seq]
		# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " Sync_Req_TX: ", dict)
		self.device.TransmitFD(chn_handle, canfd_msgs, 1)

	def sync_event_rsp(self, chn_handle, dict, RPDU):
		"""
		响应同步的请求
		:param chn_handle:设备句柄
		:param dict: 响应的信号字典
		:param RPDU: 收到的PDU
		:return: None
		"""
		global MSG
		time.sleep(dict["period"]/1000)
		canfd_msgs = (ZCAN_TransmitFD_Data * 1)()
		canfd_msgs[0].transmit_type = 1
		canfd_msgs[0].frame.eff = 0
		canfd_msgs[0].frame.rtr = 0
		canfd_msgs[0].frame.brs = 1
		canfd_msgs[0].frame.can_id = int(dict["data_id"][1:], 16)
		canfd_msgs[0].frame.len = len(dict["data"])
		dict["data"][0] = RPDU["data"][0]
		dict["data"][1] = RPDU["data"][1]
		full_freshness = hex(MSG["".join(hex(i).replace("0x", "").zfill(2) for i in RPDU["data"][0:2])[1:].upper()]["freshness"]).replace("0x", "").zfill(16)
		dict["data"][2] = int(full_freshness[0:2], 16)
		dict["data"][3] = int(full_freshness[2:4], 16)
		dict["data"][4] = int(full_freshness[4:6], 16)
		dict["data"][5] = int(full_freshness[6:8], 16)
		dict["data"][6] = int(full_freshness[8:10], 16)
		dict["data"][7] = int(full_freshness[10:12], 16)
		dict["data"][8] = int(full_freshness[12:14], 16)
		dict["data"][9] = int(full_freshness[14:16], 16)
		# 取最后1个字节的freshness
		dict["data"][-4] = int(hex(dict["freshness"]).replace("0x", "").zfill(16)[-2:], 16)
		# 加密PDU
		APDU = dict["data_id"]+"".join([hex(i).replace("0x", "").zfill(2) for i in dict["data"][0:len(dict["data"])-4]])+"0000000000000000"
		# 计算MAC
		full_mac = demo.MAC.encryption(APDU)
		# 截取MAC
		dict["data"][-3] = int(full_mac[0:2], 16)
		dict["data"][-2] = int(full_mac[2:4], 16)
		dict["data"][-1] = int(full_mac[4:6], 16)
		for signal_seq in range(canfd_msgs[0].frame.len):
			canfd_msgs[0].frame.data[signal_seq] = dict["data"][signal_seq]
		# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " Sync_Rsq_TX: ", dict)
		self.device.TransmitFD(chn_handle, canfd_msgs, 1)


	def recive_device(self, chn_handle, ECU):
		"""
		:param chn_handle: 设备句柄
		:return: 无返回值
		"""
		while not self.flag_receive:
			time.sleep(0.01)
			global MSG
			rcv_canfd_num = self.device.GetReceiveNum(chn_handle, ZCAN_TYPE_CANFD)
			if rcv_canfd_num > 0:
				# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ", "Receive CANFD message number:%d" % rcv_canfd_num)
				rcv_canfd_msgs, rcv_canfd_num = self.device.ReceiveFD(chn_handle, rcv_canfd_num, 1000)
				rcv_cfd_data = []
				for i in range(rcv_canfd_num):
					rcv_cfd_data.append(dict(
						{"No.": i,
						 "timestamp": rcv_canfd_msgs[i].timestamp,
						 "can_id": rcv_canfd_msgs[i].frame.can_id,
						 "len": rcv_canfd_msgs[i].frame.len,
						 "eff": rcv_canfd_msgs[i].frame.eff,
						 "rtr": rcv_canfd_msgs[i].frame.rtr,
						 "esi": rcv_canfd_msgs[i].frame.esi,
						 "brs": rcv_canfd_msgs[i].frame.brs,
						 "data": [rcv_canfd_msgs[i].frame.data[j] for j in range(rcv_canfd_msgs[i].frame.len)]}))
				for i in range(rcv_canfd_num):
					if rcv_cfd_data[i]["can_id"] in [259, 396, 555, 1157]:
						# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " RX: ", rcv_cfd_data)
						truncation_freshness = rcv_cfd_data[i]["data"][-4]
						truncation_mac = rcv_cfd_data[i]["data"][-3:]
						if truncation_freshness > int(hex(MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness"]).replace("0x", "").zfill(16)[-2:], 16):
							NAPDU = MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["data_id"] + "".join([hex(j).replace("0x", "").zfill(2) for j in rcv_cfd_data[i]["data"][0:rcv_cfd_data[i]["len"] - 4]]) + hex(MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness"]).replace("0x", "").zfill(16)[:14] + hex(truncation_freshness).replace("0x", "").zfill(2)
							if self.MAC.encryption(NAPDU)[:6] == ''.join([hex(i).replace("0x", "").zfill(2) for i in truncation_mac]):
								print('\033[032m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " RX:数据{}校验成功".format(hex(rcv_cfd_data[i]["can_id"]).replace("0x", "")), '\033[0m')
								MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness"] += 1
								#此处需要对xml文件进行操作,已修改，1道锁行不行
							else:
								print('\033[031m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " RX:数据{}校验失败".format(hex(rcv_cfd_data[i]["can_id"]).replace("0x", "")), '\033[0m')
								# gevent.spawn(self.sync_event_req, chn_handle, MSG["4A2"], MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness_id"])
								self.sync_event_req(chn_handle, MSG[ECU],MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness_id"])
								# 需要发起同步报文请求,已添加，需要验证
						elif truncation_freshness <= int(hex(MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness"]).replace("0x", "").zfill(16)[-2:], 16):
							NAPDU = MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["data_id"] + "".join([hex(j).replace("0x", "").zfill(2) for j in rcv_cfd_data[i]["data"][0:rcv_cfd_data[i]["len"] - 4]]) + hex(MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness"]+255).replace("0x", "").zfill(16)[:14] + hex(truncation_freshness).replace("0x", "").zfill(2)
							if self.MAC.encryption(NAPDU)[:6] == ''.join([hex(i).replace("0x", "").zfill(2) for i in truncation_mac]):
								print('\033[032m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " RX:数据{}校验成功".format(hex(rcv_cfd_data[i]["can_id"]).replace("0x", "")), '\033[0m')
								MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness"] += 1
							else:
								pass
								print('\033[031m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " RX:数据{}校验失败".format(hex(rcv_cfd_data[i]["can_id"]).replace("0x", "")), '\033[0m')
								# gevent.spawn(self.sync_event_req, chn_handle, MSG["4A2"], MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness_id"])
								self.sync_event_req(chn_handle, MSG[ECU], MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["freshness_id"])
								# 需要发起同步报文请求，已添加，需要验证
						else:
							pass
					elif rcv_cfd_data[i]["can_id"] in [1187, 1203]:
						print(rcv_cfd_data[i])
						truncation_mac = rcv_cfd_data[i]["data"][-3:]
						NAPDU = MSG[hex(rcv_cfd_data[i]["can_id"]).replace("0x", "").upper()]["data_id"] + "".join([hex(j).replace("0x", "").zfill(2) for j in rcv_cfd_data[i]["data"][0:rcv_cfd_data[i]["len"] - 4]]) + "0000000000000000"
						if self.MAC.encryption(NAPDU)[:6] == ''.join([hex(i).replace("0x", "").zfill(2) for i in truncation_mac]):
							if rcv_cfd_data[i]["can_id"] == 1187:
								Req_Fid = (hex(rcv_cfd_data[i]["data"][0]) + hex(rcv_cfd_data[i]["data"][1])).replace("0x", "")
								print('\033[033m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" RX: TBOX发送同步{Req_Fid}请求。", '\033[0m')
								# gevent.spawn(self.sync_event_rsp, chn_handle, MSG["4B2"], rcv_cfd_data[i])
								if Req_Fid == "F080":
									self.sync_event_rsp(chn_handle, MSG["4B0"], rcv_cfd_data[i])
								else:
									self.sync_event_rsp(chn_handle, MSG["4B2"], rcv_cfd_data[i])
							elif rcv_cfd_data[i]["can_id"] == 1203:
								Rsp_Fid = (hex(rcv_cfd_data[i]["data"][0]) + hex(rcv_cfd_data[i]["data"][1])).replace("0x", "")
								print('\033[034m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" RX: TBOX发送同步{Rsp_Fid}反馈。", '\033[0m')
								if int("".join([hex(i).replace("0x", "").zfill(2) for i in rcv_cfd_data[i]["data"][2:10]]), 16) == 0:
									MSG[''.join(hex(i).replace("0x", "").zfill(2) for i in rcv_cfd_data[i]["data"][0:2])[1:].upper()]["freshness"] = 255
								else:
									MSG[''.join(hex(i).replace("0x", "").zfill(2) for i in rcv_cfd_data[i]["data"][0:2])[1:].upper()]["freshness"] = int("".join([hex(i).replace("0x", "").zfill(2) for i in rcv_cfd_data[i]["data"][2:10]]), 16) - 1
							else:
								pass
						else:
							print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " RX: TBOX发送的同步请求无效。")
					else:
						pass
						# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ", "收到非Secoc数据。")
			else:
				pass
				# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ","收到非CANFD数据！！！")


	def stop_thread(self, action_timer):
		"""
		停止ECU动作的函数
		:param action_timer: 希望执行RT的时间
		:return: None
		"""
		time.sleep(action_timer)
		self.flag_receive = True
		self.flag_transform = True
		# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ", "修改标志位！！！")
		time.sleep(1)
		self.flag_receive = False
		self.flag_transform = False

	def close_device(self, handle, chn_handle):
		# Close CAN
		self.device.ResetCAN(chn_handle)
		# Close Device
		self.device.CloseDevice(handle)



if __name__ == "__main__":
	demo = ZLG()
	handle, chn_handle = demo.open_device(ZCAN_USBCANFD_200U, 0)
	try:
		TX15C = gevent.spawn(demo.transform_device_cycle, chn_handle, MSG["15C"])
		TX176 = gevent.spawn(demo.transform_device_cycle, chn_handle, MSG["176"])
		TX80 = gevent.spawn(demo.transform_device_cycle, chn_handle, MSG["080"])
		RX = gevent.spawn(demo.recive_device, chn_handle, "4A6")
		Stop = gevent.spawn(demo.stop_thread, 30)
		gevent.joinall([TX15C, TX176, TX80, RX, Stop])
	except Exception as e:
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ", str(e))
		exit(0)
	finally:
		demo.close_device(handle, chn_handle)
		exit(0)



# class FVM:
# 	def __init__(self, TripCounter, ResetCounter, MessagesCounter, ResetFlag):
# 		"""
# 		:param TripCounter: 同步计数器，3字节
# 		:param ResetCounter: 重置计数器，2字节
# 		:param MessagesCounter: 消息计数器，14bit高位，8bit低位
# 		:param ResetFlag: 重置低位，2bit
# 		total：8bytes
# 		"""
# 		self.TripCounter = TripCounter
# 		self.ResetCounter = ResetCounter
# 		self.MessagesCounter = MessagesCounter
# 		self.ResetFlag = ResetFlag

