#!/usr/bin/env python

import argparse
import json
import sys
import xml.etree.ElementTree as ET
import http.client

HOST = "hargharbijli.bsphcl.co.in"

def main():
    parser = argparse.ArgumentParser(description="Get smart meter balance")

    parser.add_argument(
        "con_num",
        metavar="Consumer-Number",
        type=int,
        help="enter your consumer number",
    )
    parser.add_argument(
        "-i", "--info", action="store_true", help="show other information"
    )

    args = parser.parse_args()

    con_num = args.con_num

    if len(str(con_num)) != 9:
        sys.exit("Invalid Consumer-Number!")

    if args.info:
        res = fetch_consumer_details(con_num)
    else:
        res = fetch_balance(con_num)

    print(json.dumps(res, indent=2))


def fetch_balance(con_num: str):
    URL = f"/WebService/WebServiceGIS.asmx/GetSMPaymentDetails?StrCANumber={con_num}"
    try:
        res_xml = request_get(HOST, URL)
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit()

    try:
        balance_dict = parse_xml(res_xml)
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit()
    return balance_dict


def fetch_consumer_details(con_num: str):
    URL = f"/WebService/WebServiceGIS.asmx/GetConsumerDtls?ConId={con_num}"
    try:
        res_xml = request_get(HOST, URL)
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit()

    try:
        details_dict = parse_xml(res_xml)[0]
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit()
    return details_dict


def request_get(host: str, url: str):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode()


def parse_xml(xml_string: str):
    try:
        root = ET.fromstring(xml_string)
    except Exception as e:
        raise Exception(f"Failed to parse xml\n{xml_string}\n{e}")
    json_string = root.text
    if not json_string:
        raise Exception(f"Failed to parse xml\n{xml_string}")
    json_object = json.loads(json_string)
    return json_object


if __name__ == "__main__":
    main()
