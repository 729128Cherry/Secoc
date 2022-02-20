# import threading
#
# def With_ReceiveThread(f):
# 	def Threads(*args):
# 		t = threading.Thread(target=f, args=(*args,))
# 		t.daemon = True
# 		t.start()
#
# 	return Threads
#
#
# def h():
# 	print("111")
#
#
# def m():
# 	print("222")
#
# @With_ReceiveThread
# def mm():
# 	while 1:
# 		m()
#
# @With_ReceiveThread
# def hh():
# 	while 1:
# 		h()
#
# while 1:
# 	hh()
# 	mm()

#

# ANRC = {
# 	"ANRC_RPAAuthReq_SecOC0": {"can_id": "15C", "period": 50, "type": "cycle", "freshness_id": "F15C", "data_id": "515C",
# 					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
# 	"ANRC_PASInfo_SecOC1": {"can_id": "176", "period": 100, "type": "cycle", "freshness_id": "F176", "data_id": "5176",
# 					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
# 	"ANRC_CntrSynReq": {"can_id": "4A2", "period": 50, "type": "event", "freshness_id": "F4A2", "data_id": "54A2",
# 					   "data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
# 	"ANRC_CntrSynRsp": {"can_id": "4B2", "period": 50, "type": "event", "freshness_id": "F4B2", "data_id": "54B2",
# 					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
#
# }
# for i in ANRC.items():
# 	for j in i[1].items():
# 		if "15C" in j:
# 			x = i[0]
#
# print(x)
# print([i[0] for i in ANRC.items() for j in i[1].items() if "15C" in j])

# x = [1,2,3,4,5,6,7]
# print(x[-4])

MSG = {
	# ANRC
	"15C": {"name": "ANRC_RPAAuthReq_SecOC0", "period": 50, "type": "cycle", "freshness_id": "F15C", "data_id": "515C",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			"freshness": 0},
	"176": {"name": "ANRC_PASInfo_SecOC1", "period": 100, "type": "cycle", "freshness_id": "F176", "data_id": "5176",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			"freshness": 0},
	"4A2": {"name": "ANRC_CntrSynReq", "period": 50, "type": "event", "freshness_id": "F4A2", "data_id": "54A2",
			"data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"4B2": {"name": "ANRC_CntrSynRsp", "period": 50, "type": "event", "freshness_id": "F4B2", "data_id": "54B2",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	# TBOX
	"103": {"name": "TBOX_AVPReq_SecOC3", "can_id": "103", "period": 10, "type": "cycle", "freshness_id": "F103",
			"data_id": "5103",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"18C": {"name": "TBOX_RemVehCtrlAssist_SecOC2", "can_id": "18C", "period": 20, "type": "cycle",
			"freshness_id": "F18C", "data_id": "518C",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			"freshness": 0},
	"22B": {"name": "TBOX_RemVehCtrl_SecOC1", "can_id": "22B", "period": 100, "type": "cycle", "freshness_id": "F22B",
			"data_id": "522B",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"485": {"name": "TBox_RemVehCtrlAssist_SecOC3", "can_id": "485", "period": "?", "type": "event",
			"freshness_id": "F485", "data_id": "5485",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			"freshness": 0},
	"4A3": {"name": "Tbox_CntrSynReq", "can_id": "4A3", "period": 50, "type": "event", "freshness_id": "F4A3",
			"data_id": "54A3",
			"data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"4B3": {"name": "Tbox_CntrSynRsp", "can_id": "4B3", "period": 50, "type": "event", "freshness_id": "F4B3",
			"data_id": "54B3",
			"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
}

#
#
# x = [1,2,3,4,5,6]
# print(x[1])


# # , 1187, 1203
#
# from gevent import monkey
# monkey.patch_all()
# import gevent
# import time
#
#
# falg = True
# i = 0
# class a:
# 	def hh(self):
# 		while falg:
# 			global i
# 			time.sleep(0.05)
# 			i +=1
# 			print("hh", i)
#
#
# 	def hehe(self):
# 		global i
# 		while falg:
# 			time.sleep(0.01)
# 			i += 2
# 			print("hehe", i)
#
#
# 	def flag_1(self):
# 		time.sleep(10)
# 		global falg
# 		falg = False
#
# if __name__ == '__main__':
# 	start = time.time()
# 	demo = a()
# 	g1 = gevent.spawn(demo.hh)
# 	g2 = gevent.spawn(demo.hehe)
# 	g3 = gevent.spawn(demo.flag_1)
# 	gevent.joinall([g1, g2, g3])
# 	print(time.time()-start)
# 	print("主")
#
# from gevent import monkey
# monkey.patch_all()
# from zlgcan import *
# from Crypto.Hash import CMAC
# from Crypto.Cipher import AES
# import time
# import gevent
# from SecXML import MSG
#
#
# # 经过比对的CMAC_ASE128计算
# # secret_key = '0102030405060708090A0B0C0D0E0F10'
# # messages = 'F22B000000000000CA00000000000000000000000014'
# #
# # secret_key = '0102030405060708090A0B0C0D0E0F10'
# # messages = '522B000000000000CA00000000000000000000000001'
# #
# # secret_key_new = bytes.fromhex(secret_key)
# # messages_new = bytes.fromhex(messages)
# #
# # c = CMAC.new(secret_key_new, messages_new, ciphermod=AES)
# # print(c.hexdigest())
#
#
# # x = "a95adc397dc549a7ba9a1112c36c9a06"
# # print(x[:6])
# #
# # x = "3456"
# # print(x[-2:])

# 本地 远程
# 0	1
# 255 0
# e = 1
# print('\033[032m', e, '\033[0m')

#
# x = [1,2,3,4,5,6,7,8]
# print(x[:len(x)-4])

