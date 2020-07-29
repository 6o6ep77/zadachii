import sqlite3
import csv
import json
from openpyxl import Workbook


def main():
    class Facility():
        def __init__(self, name):
            self.name = name
            self.input_streams = {1:potok1.stream_name()}
            self.output_streams = {2:potok2.stream_name()}
            print("Создание установки")

    class AVT(Facility):
        def display_info(self):
            print("Данные установки:", self.name, self.__load_max, self.input_streams, self.output_streams)

        @property
        def load_max(self):
            return self.__load_max

        @load_max.setter
        def load_max(self, load_max):
            self.__load_max = load_max

    class Secondary(Facility):
        def display_info(self):
            print("Данные установки:", self.name, self.__load_max)

        @property
        def load_max(self):
            return self.__load_max

        @load_max.setter
        def load_max(self, load_max):
            self.__load_max = load_max


#Задача №2
    class Streams:
        def __init__(self, name):
            self.name = name
            self.start_place = ['1','2']
            self.end_place = ['3','4']

        def display_info(self):
            print("Потоки:", self.name, self.start_place, self.end_place)

        def stream_name(self):
            return (self.name)

    potok1 = Streams("Perviy")
    potok1.display_info()  # инфа о потоке

    potok2 = Streams("Vtoroy")
    potok2.display_info()  # инфа о потоке

    ustanovka1 = AVT("АУФ-19")
    ustanovka1.load_max = "Максимальная загрузка1"
    ustanovka1.display_info() # инфа о установке

    ustanovka2 = Secondary("Т-34")
    ustanovka2.load_max = "Максимальная загрузка2"
    ustanovka2.display_info()  # инфа о установке


#Задача №3:
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT unit.name, stream.name 
                    FROM unit_material
					LEFT JOIN unit ON unit_material.unit_id = unit.id
					LEFT JOIN stream ON unit_material.stream_id = stream.id
                    WHERE unit_material.feed_flag = 1""")
    unit_list = cursor.fetchall()
    print("Задача №3 Ответ:", unit_list)
#Задача №4
    cursor.execute("""SELECT *
                        FROM stream
                        WHERE stream.id 
                        NOT IN 
						(SELECT stream_id
						FROM unit_material) """)
    unit_list2 = cursor.fetchall()
    print("Задача №4 Ответ:", unit_list2)

    csvfile = "data4.csv"
    with open(csvfile, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(unit_list2)

# Задача №5
    cursor.execute("""SELECT name
                        FROM stream""")
    stream_list = cursor.fetchall()
    resultdict = {}
    for row in stream_list:
        srez_stream = str(row)
        srez_stream = srez_stream[1:len(srez_stream)-2] # я сдаюсь, не знаю как получить из БД строку нормально
        cursor.execute("""SELECT unit.name 
                            FROM unit_material
                            LEFT JOIN unit ON unit_material.unit_id = unit.id
                            LEFT JOIN stream ON unit_material.stream_id = stream.id
                            WHERE unit_material.feed_flag = 1 
                            AND stream.name = """+ srez_stream)
        streams_kazdiy = cursor.fetchall()
        resultdict[srez_stream] = streams_kazdiy
    print("Задача №5 Ответ:", resultdict)

    with open('data5.json', 'w', encoding='utf-8') as fh: # кусок про json
        fh.write(
            json.dumps(resultdict, ensure_ascii=False))  # словарь в unicode-строку

    # Задача №6
    wb = Workbook()
    cursor.execute("""SELECT name
                            FROM unit""")
    ustanov_list = cursor.fetchall()
    print("Задача №6 Ответ:")
    for ust in ustanov_list:
        srez_ust = str(ust)
        srez_ust = srez_ust[1:len(srez_ust) - 2] # название установки
        srez_ust_excel = srez_ust[1:len(srez_ust) - 1] #минус кавычки
        cursor.execute("""SELECT stream.name 
                                    FROM unit_material
                                    LEFT JOIN unit ON unit_material.unit_id = unit.id
                                    LEFT JOIN stream ON unit_material.stream_id = stream.id
                                    WHERE unit_material.feed_flag = 1 
                                    AND unit.name = """ + srez_ust)
        ust_vhod = cursor.fetchall()
        print("Вход", srez_ust_excel, ust_vhod)
        cursor.execute("""SELECT stream.name 
                                            FROM unit_material
                                            LEFT JOIN unit ON unit_material.unit_id = unit.id
                                            LEFT JOIN stream ON unit_material.stream_id = stream.id
                                            WHERE unit_material.feed_flag = 0 
                                            AND unit.name = """ + srez_ust)
        ust_vihod = cursor.fetchall()
        print("Выход", srez_ust_excel, ust_vihod)
        ws1 = wb.create_sheet(srez_ust_excel)
        ws1['A1']="Вход"
        ws1['B1'] = "Выход"
        for x in range(1, len(ust_vhod)):
            znach1 = str(ust_vhod[x-1])
            znach1 = znach1[2:len(znach1) - 3]
            ws1.cell(row=x+1, column=1, value=znach1)
        for x in range(1, len(ust_vihod)):
            znach2 = str(ust_vihod[x-1])
            znach2 = znach2[2:len(znach2) - 3]
            ws1.cell(row=x+1, column=2, value=znach2)
    wb.remove(wb['Sheet'])
    wb.save('data6.xlsx')
    conn.close()

if __name__ == "__main__":
    main()