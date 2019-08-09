import logging
import requests
import sys
import os
import json
sys.path.append(os.environ["VIRTUAL_ENV"])
#from mp import MP
#m = MP()
class MP:
    def __init__(self):
       
        self.mp_base_url = "http://localhost:8001/"

        logging.info('initialization complete') 

    def build_url(self, path):
        return "{base}/{path}".format(base=self.mp_base_url, path=path)

    def get_valve_state(self):
        descr = [ 
                "V1 (gate valve)",
                "V2 (gas inlet)",
                "V3 (100T)",
                "V4 (10T)",
                "V5 (1T)",
                "V6 (detour pipe)",
                "V7 (vessel)",
                "V8 (volume 5)",
                "V11 (dut-c)",
                "V10 (dut-b)",
                "V9 (dut-a)",
                "V12 (1T PN)",
                "V13 (500T)",
                "V14 (50T)",
                "V15 (5T)",
                "-",
                "V17 (scroll vessel)",
                "V18 (TMP outlet)",
                "V19 (TMP inlet)",
                "V20 (PPC4 to scroll)"]

        valves = ["V{}".format(i) for i in range(1,21)]
        res = "\n**Current SE3 Valve State:**\n"
        for i, valve in enumerate(valves):
            path = "{}/{}".format("mpd-se3-valves/exchange", valve)
            url = self.build_url(path)
            resp = requests.get(url)
            ret = resp.json()
           
            if "Bool" in ret:
                if ret["Bool"] == 1:
                    state = ":white_check_mark:"
                else:
                    state = ":red_circle:"
            else:
                    state = "☐ unknown"
            res = res + "{s}\t\t\t**{d}**\n".format(d=descr[i], s=state)

        return res
    
    def get_servo_state(self):
        rr = range(1,7)
        descr = [
                "Vs inlet", "Vs outlet",
                "Vm inlet", "Vm outlet",
                "Vl inlet", "Vl outlet",
                ]
        servo_no = ["{}".format(i) for i in rr] 
        servo_pos = ["Servo_{}_Pos".format(i) for i in rr]
        servo_velo = ["Servo_{}_Velo".format(i) for i in rr]
        servo_move = ["Servo_{}_Move".format(i) for i in rr]
        
        entr = "* **Servo Motor {i} _({d})_:**\n\t* Velocity: {v} {vu}\n\t* Position: {p} {pu}\n\t* Moving:{m}\n"
        res = "\n**Current SE3 Servo State:**\n\n"
        for i, _ in enumerate(servo_no):
            
            path = "{}/{}".format("mpd-se3-servo/exchange", servo_pos[i])
            url = self.build_url(path)
            resp = requests.get(url)
            ret_pos = resp.json()

            if "Value" in ret_pos:
                p = ret_pos["Value"].replace("\n", "").replace("\r", "")
                pu = ret_pos["Unit"]
            else:
                p = "◌͍"
                pu = ""

            path = "{}/{}".format("mpd-se3-servo/exchange", servo_velo[i])
            url = self.build_url(path)
            resp = requests.get(url)
            ret_velo = resp.json()
            if "Value" in ret_velo:
                v = ret_velo["Value"]
                vu = ret_velo["Unit"]
            else:
                v = "◌͍"
                vu = ""

            path = "{}/{}".format("mpd-se3-servo/exchange", servo_move[i])
            url = self.build_url(path)
            resp = requests.get(url)
            ret_move = resp.json()
            if "Bool" in ret_move:
                m = ret_move["Bool"]
            else:
                m = "◌͍"

            res = res + entr.format(
                                    i = servo_no[i],
                                    d = descr[i],
                                    m = m,
                                    v = v, vu = vu, 
                                    p = p, pu = pu, 
                                    )
        res = res + "\n→ velo. refresh stops for |v| < 5rpm"
        res = res + "\n→  ◌͍ ... not changed since last init"    
        return res

    def get_gn_pressure(self):
        task_url = "http://localhost:5984/vl_db/_design/dbmp/_view/tasks?key=%22Inficon_Modbus_CDG-read_out%22"
        relay_url = "http://localhost:55555"
        resp = requests.get(task_url)
        task = resp.json()
        
        if not "rows" in task:
            return "no task found at {}".format(task_url)

        str_task = json.dumps(task)
        str_task = str_task.replace("@acc", "MODBUS")
        str_task = str_task.replace("@host", "e75480")
        str_task = str_task.replace("@repeat", "5")
        str_task = str_task.replace("@repeat", "5")
        str_task = str_task.replace("@token", "state")
        task = json.loads(str_task)
        task = task['rows'][0]['value']

        resp =  requests.post(relay_url, data=json.dumps(task))
        data  = resp.json()
        if not "Result" in data:
            return "No result for task\n```json\n{}\n```".format(task)
        entr = "(**{v:.4E}** ± {s:.4E}) {u} (N={n})\t↣ **{t}**\n"
        res = "\n**Current SE3 GroupNormal State:**\n\n"
        for d in data["Result"]:
            res = res + entr.format(
                                    t = d["Type"],
                                    v = d["Value"],
                                    s = d["SdValue"],
                                    u = d["Unit"],
                                    n = d["N"]
                                    )
        return res

if __name__ == "__main__":
    mp = MP()
    #print( open("help.md").read())
    print(mp.get_valve_state())
    #print(mp.get_servo_state())
    #print(mp.get_gn_pressure())