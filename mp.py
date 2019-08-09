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
        valves = ["V{}".format(i) for i in range(1,21)]
        res = "\n**Current SE3 Valve State:**\n"
        for valve in valves:
            path = "{}/{}".format("mpd-se3-valves/exchange", valve)
            url = self.build_url(path)
            resp = requests.get(url)
            ret = resp.json()
           
            if "Bool" in ret:
                if ret["Bool"] == 1:
                    state = "✓ (open)"
                else:
                    state = "✗ (closed)"
            else:
                    state = "☐ unknown"
            res = res + "**{v}**    {s}\n".format(v=valve, s=state)

        return res
    
    def get_servo_state(self):
        rr = range(1,7)
        servo_no = ["{}".format(i) for i in rr] 
        servo_pos = ["Servo_{}_Pos".format(i) for i in rr]
        servo_velo = ["Servo_{}_Velo".format(i) for i in rr]

        entr = "**Servo Motor {i}:**\n\tVelocity: {v} {vu}\n\tPosition: {p} {pu}\n"
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
                p = "unknown"
                pu = ""

            path = "{}/{}".format("mpd-se3-servo/exchange", servo_velo[i])
            url = self.build_url(path)
            resp = requests.get(url)
            ret_velo = resp.json()
            if "Value" in ret_velo:
                v = ret_velo["Value"]
                vu = ret_velo["Unit"]
            else:
                v = "☐ unknown"
                vu = ""

            res = res + entr.format(
                                    i = servo_no[i], 
                                    v = v, vu = vu, 
                                    p = p, pu = pu, 
                                    )
        res = res + "\n (velo. refresh stops for |v| < 5rpm)"    
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
    #print(mp.get_valve_state())
    #print(mp.get_servo_state())
    #print(mp.get_gn_pressure())