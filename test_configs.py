import os
import json
import unittest

ROOT_PATH = "/root/script/config/"
DEVICE_ID=""

def read_json(filepath):
    try:
        with open(filepath) as json_file:
            return json.load(json_file)
    except JSONError as err:
        print(f"Error loading {filepath}")
        return False

class TestStringMethods(unittest.TestCase):
    def test_settings(self):
        missing_field = 0
        fields = ['device_id', 'broker', 'port', 'user', 'pass', 'period_of_message', 'client_name', 'hash']
        settings = read_json(ROOT_PATH+"settings.json")
        for field in fields:
            if field not in settings:
                missing_field = 1
        self.assertEqual(missing_field, 0)

    def test_topics(self):
        pass

    def test_config(self):
        settings = read_json(ROOT_PATH+"config.json")
        self.assertEqual(settings['Device_Id']==DEVICE_ID, True)

    def test_map(self):
        pass

    def test_mpu(self):
        missing_field = 0
        settings = read_json(ROOT_PATH+"mpu-config.json")
        for id in settings['identifiers']:
            if ('unit' not in id) or ('parametr' not in id):
                missing_field = 1
        self.assertEqual(missing_field, 0)

    def test_certs(self):
        command = "openssl x509 -enddate -noout -in "
        ca_test = os.system(command + ROOT_PATH + "ca.crt >> tmp_date")
        cert_test = os.system(command + ROOT_PATH + "clientcert.crt >> tmp_date")
        key_test = os.system(command + ROOT_PATH + "clientkey.pem >> tmp_date")
        self.assertEqual(ca_test, 0)
        self.assertEqual(cert_test, 0)
        self.assertEqual(key_test, 0)

        file = open(ROOT_PATH+"tmp_date", "r")
        for line in file.readlines():
            line.replace('notAfter=', '')

    def test_network(self):
        settings = read_json("/root/script/config/network.json")
        response_easy = os.system("ping -c 1 "+ settings["ip_adresses"]["easycon"])
        response_google = os.system("ping -c 1 "+ settings["ip_adresses"]["google"])
        self.assertEqual(response_easy, 0)
        self.assertEqual(response_google, 0)

if __name__ == '__main__':
    unittest.main()
