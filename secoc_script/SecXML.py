# coding=utf-8
# @Time    : 2022/1/4
# @Author  : Yi Chen

MSG = {
	# ESC，该控制器不含有sync_req报文，只需要测试TBOX发出请求，收到响应即可
	"080": {"encryption": "secoc", "name": "ESC_SecOC0", "can_id": "080", "period": 10, "type": "cycle", "freshness_id": "F080", "data_id": "5080",
		   				"data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"4B0": {"encryption": "secoc", "name": "ESC_CntrSynRsp", "can_id": "4B0", "period": 50, "type": "event", "freshness_id": "F4B0", "data_id": "54B0",
		   				"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	#VCU,该控制器不含sync_rsp报文,只需要测试发出请求,请求报文修改为4A8即可，TBOX响应即可
	"4A8": {"encryption": "secoc", "name": "VCU_CntrSynReq", "can_id": "4A8", "period": 50, "type": "event", "freshness_id": "F4A8", "data_id": "54A8",
		   				"data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	#BCM,该控制器不含sync_rsp报文,只需要测试发出请求，请求报文修改为4A6即可，TBOX响应即可
	"4A6": {"encryption": "Secoc", "name": "BCM_CntrSynReq", "can_id": "4A6", "period": 50, "type": "event", "freshness_id": "F4A6", "data_id": "54A6",
						"data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	#ANRC
	"15C": {"encryption": "E2E|Secoc", "name": "ANRC_RPAAuthReq_SecOC0", "can_id": "15C", "period": 50, "type": "cycle", "freshness_id": "F15C", "data_id": "515C",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0, "alive_counter": 0},
	"176": {"encryption": "Secoc", "name": "ANRC_PASInfo_SecOC1", "can_id": "176", "period": 100, "type": "cycle", "freshness_id": "F176", "data_id": "5176",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"4A2": {"encryption": "Secoc", "name": "ANRC_CntrSynReq", "can_id": "4A2", "period": 50, "type": "event", "freshness_id": "F4A2", "data_id": "54A2",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"4B2": {"encryption": "Secoc", "name": "ANRC_CntrSynRsp", "can_id": "4B2", "period": 50, "type": "event", "freshness_id": "F4B2", "data_id": "54B2",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	#TBOX
	"103": {"encryption": "E2E|Secoc", "name": "TBOX_AVPReq_SecOC3", "can_id": "103", "period": 10, "type": "cycle", "freshness_id": "F103", "data_id": "5103",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0, "alive_counter": 0},
	"18C": {"encryption": "Secoc", "name": "TBOX_RemVehCtrlAssist_SecOC2", "can_id": "18C", "period": 20, "type": "cycle", "freshness_id": "F18C", "data_id": "518C",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"22B": {"encryption": "Secoc", "name": "TBOX_RemVehCtrl_SecOC1", "can_id": "22B", "period": 100, "type": "cycle", "freshness_id": "F22B", "data_id": "522B",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"485": {"encryption": "E2E|Secoc", "name": "TBox_RemVehCtrlAssist_SecOC3", "can_id": "485", "period": "50", "type": "event", "freshness_id": "F485", "data_id": "5485",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0, "alive_counter": 0},
	"4A3": {"encryption": "Secoc", "name": "Tbox_CntrSynReq", "can_id": "4A3", "period": 50, "type": "event", "freshness_id": "F4A3", "data_id": "54A3",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
	"4B3": {"encryption": "Secoc", "name": "Tbox_CntrSynRsp", "can_id": "4B3", "period": 50, "type": "event", "freshness_id": "F4B3", "data_id": "54B3",
					   "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "freshness": 0},
}