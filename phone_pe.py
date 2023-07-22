import pandas as pd
import json
import os
import mysql.connector
from pathlib import Path

agg_tranc_path = 'C:\\Users\\SHIVA\\Documents\\data\\aggregated\\transaction\\country\\india\\state\\'
agg_user_path = 'C:\\Users\\SHIVA\\Documents\\data\\aggregated\\user\\country\\india\\state\\'
map_tranc_path = 'C:\\Users\\SHIVA\\Documents\\data\\map\\transaction\\hover\\country\\india\\state\\'
map_user_path = 'C:\\Users\\SHIVA\\Documents\\data\\map\\user\\hover\\country\\india\\state\\'
top_user_path = 'C:\\Users\\SHIVA\\Documents\\data\\top\\user\\country\\india\\state'
top_tranc_path = 'C:\\Users\\SHIVA\\Documents\\data\\top\\transaction\\country\\india\\state'

#extraction of aggregate transaction data
class agg_tran:
    def __init__(self, agg_tran_path):
        self.state_aggregated_transaction = pd.DataFrame({})
        self.agg_tran_path = agg_tran_path

    def aggregated_transaction(self, state, year, quarter, path):
        agg_df = pd.read_json(path)
        trans_df = agg_df.data.transactionData
        if trans_df:
            for i in trans_df:
                all_rows = {"Transaction_method": i['name'], "Transaction_Counts": i['paymentInstruments'][0]['count'],
                            "Transaction_amounts": i['paymentInstruments'][0]['amount'], "state": state, "year": year,
                            "quarter": quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_aggregated_transaction = pd.concat([self.state_aggregated_transaction, all_rows_df])
                self.state_aggregated_transaction['Transaction_amounts'] = self.state_aggregated_transaction[
                    'Transaction_amounts'].apply(lambda x: int(x))
            self.state_aggregated_transaction.reset_index(drop=True, inplace=True)

    def get(self):
        for state in os.listdir(self.agg_tran_path):
            state_path = os.path.join(self.agg_tran_path, state)
            for year in range(2018, 2023):
                year_path = os.path.join(state_path, str(year))
                files = []

                for (dirpath, dirnames, filenames) in os.walk(year_path):
                    files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                    break

                for file_path in files:
                    quarter = Path(file_path).stem
                    self.aggregated_transaction(state, year, quarter, file_path)
        return self.state_aggregated_transaction

agg_tran_object = agg_tran(agg_tranc_path)
aggregated_transaction = agg_tran_object.get()

#extraction of aggregate user data

class agg_user:
    def __init__(self, agg_user_path):
        self.state_aggregated_user = pd.DataFrame({})
        self.agg_user_path = agg_user_path

    def aggregated_user(self, state, year, quarter, path):
        u_df = pd.read_json(path)
        reg_users = u_df['data']['aggregated']['registeredUsers']
        app_opens = u_df['data']['aggregated']['appOpens']
        user_df = u_df.data.usersByDevice
        if user_df:
            for i in user_df:
                all_rows = {"brand": i['brand'], "Count": i['count'], "percentage": i['percentage'], "state": state,
                            "year": year, "quarter": quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_aggregated_user = pd.concat([self.state_aggregated_user, all_rows_df])
            self.state_aggregated_user.reset_index(drop=True, inplace=True)

    def get(self):
        for state in os.listdir(self.agg_user_path):
            state_path = os.path.join(self.agg_user_path, state)
            for year in range(2018, 2023):
                year_path = os.path.join(state_path, str(year))
                files = []

                for (dirpath, dirnames, filenames) in os.walk(year_path):
                    files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                    break

                for file_path in files:
                    quarter = Path(file_path).stem
                    self.aggregated_user(state, year, quarter, file_path)
        return self.state_aggregated_user

agg_user_object = agg_user(agg_user_path)
aggregated_users = agg_user_object.get()

#extraction of map transaction data

class map_tran:
    def __init__(self, map_tran_path):
        self.state_map_transaction = pd.DataFrame({})
        self.map_tran_path = map_tran_path

    def map_transaction(self, state, year, quarter, path):
        map_df = pd.read_json(path)
        trans_df = map_df.data.hoverDataList
        if trans_df:
            for i in trans_df:
                all_rows = {"district_name": i['name'], "Transaction_Count": i['metric'][0]['count'],
                            "Transaction_amount": i['metric'][0]['amount'], "state": state, "year": year,
                            "quarter": quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_map_transaction = pd.concat([self.state_map_transaction, all_rows_df])
                self.state_map_transaction['Transaction_amount'] = self.state_map_transaction[
                    'Transaction_amount'].apply(lambda x: int(x))
            self.state_map_transaction.reset_index(drop=True, inplace=True)

    def get(self):
        for state in os.listdir(self.map_tran_path):
            state_path = os.path.join(self.map_tran_path, state)
            for year in range(2018, 2023):
                year_path = os.path.join(state_path, str(year))
                files = []

                for (dirpath, dirnames, filenames) in os.walk(year_path):
                    files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                    break

                for file_path in files:
                    quarter = Path(file_path).stem
                    self.map_transaction(state, year, quarter, file_path)
        return self.state_map_transaction\

map_tran_object = map_tran(map_tranc_path)
map_transaction = map_tran_object.get()

#extraction of map user data
class map_user:
    def __init__(self, map_user_path):
        self.state_map_user = pd.DataFrame({})
        self.map_user_path = map_user_path

    def map_user(self, state, year, quarter, path):
        map_df = pd.read_json(path)
        user_df = map_df.data.hoverData
        if user_df:
            for i in user_df:
                all_rows = {"district_name": i, "registeredUsers": user_df[i]['registeredUsers'],
                            "appOpens": user_df[i]['appOpens'], "state": state, "year": year, "quarter": quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_map_user = pd.concat([self.state_map_user, all_rows_df])
            self.state_map_user.reset_index(drop=True, inplace=True)

    def get(self):
        for state in os.listdir(self.map_user_path):
            state_path = os.path.join(self.map_user_path, state)
            for year in range(2018, 2023):
                year_path = os.path.join(state_path, str(year))
                files = []

                for (dirpath, dirnames, filenames) in os.walk(year_path):
                    files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                    break

                for file_path in files:
                    quarter = Path(file_path).stem
                    self.map_user(state, year, quarter, file_path)
        return self.state_map_user

map_user_object = map_user(map_user_path)
map_user = map_user_object.get()

#extraction of top user data

class pin_users:
    def __init__(self, usr_pin_path):
        self.state_pin_users = pd.DataFrame({})
        self.usr_pin_path = usr_pin_path

    def agg_pin_users(self, state, year, quarter, path):

        p_dft = pd.read_json(path)  # dataframe
        # data sorting
        pincodes = p_dft['data']['pincodes']
        districts = p_dft['data']['districts']

        if not p_dft.empty:
            for i in pincodes:
                all_rows = {"Pincodes": i['name'], "Total_Registered_users": i['registeredUsers'], "state": state,
                            "year": year, "quarter": quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_pin_users = pd.concat([self.state_pin_users, all_rows_df])
            self.state_pin_users.reset_index(drop=True, inplace=True)

    def get(self):
        for state in os.listdir(self.usr_pin_path):
            state_path = os.path.join(self.usr_pin_path, state)

            for year in range(2018, 2023):
                year_path = os.path.join(state_path, str(year))
                qfiles = []

                for (dirpath, dirnames, filenames) in os.walk(year_path):
                    qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                    break

                for qfile_path in qfiles:
                    quarter = Path(qfile_path).stem
                    self.agg_pin_users(state, year, quarter, qfile_path)
        return self.state_pin_users

pin_users_object = pin_users(top_user_path)
pin_users = pin_users_object.get()

#extraction of top transaction

class pin_tranc:
    def __init__(self, tran_pin_path):
        self.state_pin_tran = pd.DataFrame({})
        self.tran_pin_path = tran_pin_path

    def agg_pin_tran(self, state, year, quarter, path):

        p_dft = pd.read_json(path)  # dataframe
        # data sorting
        pincodes = p_dft['data']['pincodes']
        districts = p_dft['data']['districts']

        if not p_dft.empty:
            for i in pincodes:
                all_rows = {"Pincodes": i['entityName'], "count": i['metric']['count'], 'amount': i['metric']['amount'],
                            "state": state, "year": year, "quarter": quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_pin_tran = pd.concat([self.state_pin_tran, all_rows_df])
            self.state_pin_tran.reset_index(drop=True, inplace=True)

    def get(self):
        for state in os.listdir(self.tran_pin_path):
            state_path = os.path.join(self.tran_pin_path, state)

            for year in range(2018, 2023):
                year_path = os.path.join(state_path, str(year))
                qfiles = []

                for (dirpath, dirnames, filenames) in os.walk(year_path):
                    qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                    break

                for qfile_path in qfiles:
                    quarter = Path(qfile_path).stem
                    self.agg_pin_tran(state, year, quarter, qfile_path)
        return self.state_pin_tran


object_pin_tranc = pin_tranc(top_tranc_path)
pin_tran = object_pin_tranc.get()