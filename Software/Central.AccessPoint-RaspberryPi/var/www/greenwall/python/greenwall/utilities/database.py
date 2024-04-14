import os
import sqlite3
import logging
from threading import Lock
from sqlite3 import Error
from greenwall.exceptions.not_existing_table import NotExistingTable

class SqlDatabase:

    TABLE_REPORT = "Report"
    TABLE_STATION = "Station"

    def __init__(self, db_path):
        self.db_path = db_path
        self.lock = Lock()
        self.conn = None

        self.table_list = [
            SqlDatabase.TABLE_REPORT,
            SqlDatabase.TABLE_STATION
        ]

        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=20)
            logging.debug( "Connection to {0} SQLite was successful".format(self.db_path))
            self.conn.row_factory = sqlite3.Row 
        except Error as e:
            logging.error( "Connection to {0} SQLite failed. Error: {1}".format(self.db_path, e))

            # TODO: handle this case
            exit()

        # check if the databases are correct
        if not self.is_dbs_ok():
            logging.debug( "Re-create DBs")
            self.recreate_dbs()

    def is_dbs_ok(self):
        error_code = 1001
        cur = self.conn.cursor()
        cur.execute("begin")

        try:
            for table in self.table_list:
                query ="SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{0}' ".format(table)
                records = cur.execute(query).fetchone()
                if records[0] != 1:
                    raise NotExistingTable("{0} table does not exist. All tables must be recreated".format(table), error_code)

        except NotExistingTable as e:
            logging.debug(e.message)
            return False

        finally:
            cur.execute("commit")
        return True

    def recreate_dbs(self):
        self.drop_all_existing_tables()
        logging.debug("All tables are dropped")
        self.create_tables()
        logging.debug("All tables are recreated")


    def drop_all_existing_tables(self):
        cur = self.conn.cursor()
        cur.execute("begin")
        tables = list(cur.execute("SELECT name FROM sqlite_master WHERE type is 'table'"))
        cur.execute("commit")

        for table in tables:
            try:
                self.conn.execute("DROP TABLE {0}".format(table[0]))
            except sqlite3.OperationalError as e:
                print(e)


    def drop_tables(self):
        for table in self.table_list:
            try:
                self.conn.execute("DROP TABLE {0};".format(table))
            except sqlite3.OperationalError as e:
                logging.error("Wanted to Drop '{0}' table, but error happened: {1}".format(table, e))


    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE ''' + SqlDatabase.TABLE_STATION + '''(
                id INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                name  TEXT  NOT NULL,
                ip    TEXT  NOT NULL,
                UNIQUE(name,ip)
            );
        ''')


        self.conn.execute('''
            CREATE TABLE ''' + SqlDatabase.TABLE_REPORT + '''(
                id                  INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                id_station          INTEGER         NOT NULL,
                date                TEXT,
                pressure            DECIMAL(8,2),
                humidity            DECIMAL(4,2),
                level               DECIMAL(3,2),
                temperature         DECIMAL(3,2),
                FOREIGN KEY (id_station) REFERENCES ''' + SqlDatabase.TABLE_STATION + ''' (id)
            );
        ''')

    def append_report(self, station_name, station_ip, date, pressure=None, humidity=None, level=None, temperature=None):

        report_id = None

        with self.lock:

            cur = self.conn.cursor()
            cur.execute("begin")

            try:

                query = '''SELECT id FROM ''' + SqlDatabase.TABLE_STATION + '''
                       WHERE
                       name = :name
                       AND ip = :ip;
                    '''
                record=cur.execute(query, {'name': station_name, 'ip': station_ip}).fetchone()
                (station_id, ) = record if record else (None,)
                if not station_id:

                    query = '''INSERT INTO ''' + SqlDatabase.TABLE_STATION + ''' 
                        (name, ip) 
                        VALUES (:name, :ip);'''
                    res = cur.execute(query, {'name': station_name, 'ip': station_ip})
                    station_id = res.lastrowid

                query = '''INSERT INTO ''' + SqlDatabase.TABLE_REPORT + ''' 
                    (id_station, date, pressure, humidity, level, temperature) 
                    VALUES (:station_id, :date, :pressure, :humidity, :level, :temperature);'''
                res = cur.execute(query, {'station_id': station_id, 'date': date, 'pressure': pressure, 'humidity': humidity, 'level': level, 'temperature': temperature})
                report_id = res.lastrowid

            except sqlite3.Error as e:
                logging.error("To append report failed: {0}".format(e))
                cur.execute("rollback")

            cur.execute("commit")

        return report_id


    def selectRecordsByTimeRange(self, startDateStamp, endDateStamp):

        reportCopy = {}

        with self.lock:

            cur = self.conn.cursor()
            cur.execute("begin")

            records = {}

            # Get Card list
            query = '''
                SELECT 
                    station.name,
                    station.ip,
                    CAST(strftime('%s', report.date) AS INT),
                    report.level,
                    report.temperature,
                    report.humidity,
                    report.pressure
                FROM
                    Report report,
                    Station station
                WHERE
                    report.id_station = station.id
                    AND CAST(strftime('%s', report.date) AS INT) >= :startDateStamp
                    AND CAST(strftime('%s', report.date) AS INT) <= :endDateStamp
                '''
            query_parameters = {'startDateStamp': startDateStamp, 'endDateStamp': endDateStamp}
            logging.debug("selectRecordsByTimeRange query: '{0} / {1}'".format(query, query_parameters))
            report_list=cur.execute(query, query_parameters).fetchall()
            cur.execute("commit")


            for report in report_list:
                stationId = report[0]
                ip = report[1]
                timestamp = report[2]
                level = report[3]
                temperature = report[4]
                humidity = report[5]
                pressure = report[6]    
                record = {"timeStamp": timestamp, "levelValue": level, "temperatureValue": temperature, "humidityValue": humidity, "pressureValue": pressure}

                if reportCopy.get(stationId) is None:
                    reportCopy[stationId] = {"record": []}

                reportCopy[stationId]["ip"] = ip
                reportCopy[stationId]["record"].append(record)

            logging.debug("selectRecordsByTimeRange response: '{0}'".format(reportCopy))

        return reportCopy


    def get_latest_values(self, station_id=None):

        reportCopy = []

        with self.lock:

            cur = self.conn.cursor()
            cur.execute("begin")

            records = {}

            # Get Card list
            query = '''

                SELECT
                    station.name,
                    station.ip,
                    CAST(strftime('%s', MAX(report.date)) AS INT),
                    report.level,
                    report.temperature,
                    report.humidity,
                    report.pressure
                FROM
                    Report report,
                    Station station
                WHERE
                    report.id_station=station.id
                GROUP BY station.name
                '''
            query_parameters = {}
            logging.debug("get_latest_values query: '{0} / {1}'".format(query, query_parameters))
            report_list=cur.execute(query, query_parameters).fetchall()
            cur.execute("commit")

            for report in report_list:

                if not station_id or (station_id==report[0]):

                    stationId = report[0]
                    ip = report[1]
                    timestamp = report[2]
                    level = report[3]
                    temperature = report[4]
                    humidity = report[5]
                    pressure = report[6]

                    record = {"stationId": stationId, "ip": ip, "timeStamp": timestamp, "levelValue": level, "temperatureValue": temperature, "humidityValue": humidity, "pressureValue": pressure}
                    reportCopy.append(record)

            logging.debug("get_latest_values response: '{0}'".format(reportCopy))

        return reportCopy
