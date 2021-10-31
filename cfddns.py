import requests
import json


Global_Key = "your Global Key"
auth_email = "your registered Email address"

endpoint_url = "https://api.cloudflare.com/client/v4"

headers = {"X-Auth-Email" : auth_email, "X-Auth-Key" : Global_Key, "Content-Type" : "application/json"}

res = requests.get(endpoint_url + "/zones", headers=headers)

zone_id = json.loads(res.text)["result"][0]["id"]

print("zone id : " + zone_id)

res = requests.get(endpoint_url + "/zones/" + zone_id + "/dns_records", headers=headers)

dns_records = {}
for i in json.loads(res.text)["result"]:
    dns_records[i["name"]] = {}
    dns_records[i["name"]]["id"] = i["id"]
    dns_records[i["name"]]["ip"] = i["content"]
    dns_records[i["name"]]["type"] = i["type"]
    dns_records[i["name"]]["ttl"] = i["ttl"]
    dns_records[i["name"]]["proxied"] = i["proxied"]
    
for i in dns_records:
    if dns_records[i]["type"] == "A":
        params = {"type":dns_records[i]["type"],"name":i,"content":requests.get("http://inet-ip.info/ip").text,"ttl":dns_records[i]["ttl"], "proxied":dns_records[i]["proxied"]}
        res = requests.put(endpoint_url + "/zones/" + zone_id + "/dns_records/" + dns_records[i]["id"], headers=headers, json=params)
        print(i + " : " + str(res))
