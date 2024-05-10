# import argparse
from datetime import datetime,date
import os
import argparse
from typing import List, Optional, Tuple, Union

class Record:
    def __init__(self,id:int,date:Optional[date],category:Optional[str],amount:Optional[int],description:Optional[str])->None:
        self.id = id
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def __setattr__(self, key, value):
        if key=='id' and  not isinstance(value, int):
            raise ValueError("id неверного типа данных")
        elif  key=='date' and not isinstance(value, date):
            raise ValueError("date неверного типа данных")
        elif  key=='category' and value not in ('Доход','Расход'):
            raise ValueError("category неверного типа данных",value, type(value))
        elif  key=='amount' and not isinstance(value, (int,float)) and value <=0:
            raise ValueError("amount неверного типа данных")
        elif  key=='description' and not isinstance(value, str):
            raise ValueError("description неверного типа данных")
        return super().__setattr__(key, value)

    def get_info(self)->None:
        print(f"Дата: {self.date}")
        print(f"Категория: {self.category}")
        print(f"Сумма: {self.amount}")
        print(f"Описание: {self.description}\n")




class PersonalTracker:
    def __init__(self)->None:
        self.records=[]

    def add_record(self, record: Record)->None:
        """
        Добавляет новую запись в список records.
        """
        self.records.append(record)

    def save_records_to_file(self)->Optional[bool]:
        """
        - Сохраняет все записи из списка records в файл "data.txt".
        - Перезаписывает временный файл "data_temp.txt" с обновленными данными.
        - Возвращает True, если операция выполнена успешно, иначе обрабатывает исключение FileExistsError.
        """
        try:
            flag = False
            with open('data_temp.txt', 'w', encoding='utf8') as f:
                for obj in self.records:
                    id,date,category,amount,description = obj.id, obj.date, obj.category, obj.amount, obj.description
                    f.write(f"id: {id}\n")
                    f.write(f"Дата: {str(date)}\n")
                    f.write(f"Категория: {category}\n")
                    f.write(f"Сумма: {amount}\n")
                    f.write(f"Описание: {description}\n")
                    f.write("\n")
            flag=True
            if flag:
                os.remove('data.txt')
                os.rename('data_temp.txt', 'data.txt')
            return True
        except FileExistsError as e:
            print("Ошибка с открытием файла:",str(e))

    def load_records_from_file(self)->Optional[str]:
        """
        - Загружает записи из файла "data.txt" и добавляет их в список records.
        - Обрабатывает исключение FileExistsError и возвращает сообщение об ошибке.
        """
        try:
            with open("data.txt", 'r', encoding='utf8' ) as file:
                cur = {}
                for line in file:
                    line = line.strip()
                    if line:
                        key, value = line.split(':')
                        key = key.strip().lower()
                        value = value.strip()
                        cur[key]=value
                    else:
                        if cur:
                            id = int(cur['id'])
                            date = datetime.strptime(cur['дата'],"%Y-%m-%d").date()
                            category = cur['категория']
                            amount = int(cur['сумма'])
                            description = cur['описание']
                            self.add_record(Record(id,date,category,amount,description))
                            cur={}
                        else:
                            break
        except FileExistsError as e:
            return f"Ошибка с открытием файла - {str(e)}"

    def add_record_and_save_file(self, date:date, category:str, amount:int, description:str)->Optional[bool]:
        """
        Принимает дату, категорию, сумму и описание, создает новую запись и сохраняет ее в файл "data.txt".
        Возвращает True, если операция выполнена успешно.
        """
        last_id = self.records[-1].id
        id = last_id + 1
        self.add_record(Record(id, date, category, amount, description))
        try:
            with open("data.txt", 'a', encoding='utf8') as file:
                file.write(f"id: {id}\n")
                file.write(f"Дата: {date}\n")
                file.write(f"Категория: {category}\n")
                file.write(f"Сумма: {amount}\n")
                file.write(f"Описание: {description}\n")
                file.write("\n")
                file.seek(0)
            return True
        except FileExistsError as e:
            print(str(e))

    def edit_record_in_file(self, id:int, date:Optional[date],category:Optional[str],amount:Optional[int],description:Optional[str])->Optional[bool]:
        """
         Редактирует существующую запись по заданному id.
         Если указаны новые значения для даты, категории, суммы или описания, обновляет их и сохраняет изменения в файл.
         Возвращает True, если операция выполнена успешно.
        """
        for obj in self.records:
            if obj.id==id:
                flag=False
                if date:
                    flag=True
                    obj.date = date
                if category:
                    flag = True
                    obj.category = category
                if amount:
                    flag = True
                    obj.amount = amount
                if description:
                    flag = True
                    obj.description = description
                if flag:
                    return self.save_records_to_file()
                else:
                    return False

    def find_records(self, **kwargs)->Optional[List[Record]]:
        """
       Поиск записей по заданным параметрам, переданным как ключевые аргументы.
       Возвращает список записей, удовлетворяющих условиям поиска.
        """
        results:List[Record] = []
        print('kwargsssssssssssss',kwargs)
        for record in self.records:
            flag = True
            for key, value in kwargs.items():
                value = None if value=='' else value
                if value is not None and getattr(record, key)!=value:
                    flag=False
                    break
            if flag:
                results.append(record)
        if results:
            return results
        else:
            return None

    def balance(self)->Tuple[int,int,int]:
        """
         Вычисляет баланс доходов и расходов на основе всех записей.
        """
        sum_dox:int=0
        sum_ras:int=0

        for record in self.records:
            if record.category=="Доход":
                sum_dox+=record.amount
            else:
                sum_ras+=record.amount
        sum_pr=sum_dox-sum_ras
        return sum_dox,sum_ras,sum_pr

    def get_records(self)->List[Record]:
        """
         Возвращает все имеющиеся записи.
        """
        return  self.records

    def get_record_by_id(self,id:int)->None:
        """
        Выводит информацию о записи по заданному id.
        """
        for obj in self.records:
            if obj.id==id:
                print(obj.id)
                print(obj.date)
                print(obj.category)
                print(obj.amount)
                print(obj.description)

class ConsoleInterface:
    def __init__(self, wallet:PersonalTracker)->None:
        self.wallet = wallet

    def check_id(self, id:int)->Optional[bool]:
        """
        - Проверяет наличие заданного id в записях объекта wallet.
        - Возвращает id, если он найден, иначе выводит сообщение "нет подходящего id" и возвращает None.
        - Обрабатывает исключение ValueError, если ввод не является числом.
        """
        try:
            id = int(id)
            for obj in self.wallet.records:
                if obj.id==id:
                    return id
            # return id
            print("нет id поддходящего")
        except ValueError as e:
            print('Введите число!!!!')
            return False

    def check_amount(self, value:Optional[str], flag:bool=False)->Union[int, bool]:
        """
        - Проверяет корректность значения value, преобразуя его в целое число.
        - Проверяет диапазон значения от 1 до 999999999.
        - Возвращает значение, если оно корректно, иначе выводит сообщения об ошибке и возвращает False.
        """
        if value=='' and flag:
            return None
        try:
            value=int(value)
            if value<=0 or value>=10**9:
                print(f"значение {value} не входит в диапозон от 1 до 999999999 !!!")
                return False
            return value
        except ValueError as e:
            print("Необходимо ввести число !!!")
            return False
    def check_date(self, date:Optional[str], flag=False)->Union[date, bool]:
        """
        - Проверяет корректность формата даты и ее соответствие текущей дате.
        - Возвращает объект даты, если ввод корректен, иначе выводит сообщения об ошибке и возвращает False.
        """
        if date=='' and flag:
            return None
        try:
            add_date = datetime.strptime(date.strip(), "%Y-%m-%d")
            if add_date.date() > datetime.now().date():
                print(f"Вводимая дата {add_date} больше текущей")
                return False
            return add_date.date()
        except ValueError as e:
            print('Неправильный формат даты: YYYY-MM-DD')
            return False

    def start(self):
        """
        - Инициализирует парсер аргументов командной строки с описанием приложения.
        - Добавляет подпарсеры для различных команд: "add_record", "edit_record", "search", "balance".
        - Выполняет соответствующую функцию в зависимости от выбранной команды.

        """
        parser = argparse.ArgumentParser(description="my first cli appp")
        subparser = parser.add_subparsers()

        parser_add = subparser.add_parser("add_record", help="добавляет запись")
        parser_add.set_defaults(func=self.add_record)

        parser_edit = subparser.add_parser("edit_record",  help="редактирует запись")
        parser_edit.set_defaults(func=self.edit_record)

        parser_search = subparser.add_parser("search", help='поиск записей')
        parser_search.set_defaults(func=self.search_records)

        parser_balance = subparser.add_parser("balance")
        parser_balance.set_defaults(func=self.display_balance)

        args = parser.parse_args()

        args.func(args)

    def display_balance(self,args)->None:
        dox,ras,pr = self.wallet.balance()
        print('Баланс нашего финансового учета:', pr)
        print('Количество доходов:', dox)
        print("Количество расходов:", ras)

    def add_record(self,args)->None:
        """
        Добавляет новую запись в финансовый учет.
        """
        while True:
            print("======================")
            date = input("Введите дату для добавления в формате YYYY-MM-DD или нажмите Enter без изменения: ").strip()
            date = self.check_date(date)
            if date or date==None:
                break

        while True:
            category = input("Введите category(Доход/Расход) для добавления или нажмите Enter без изменения: ").strip()
            if category in ('Доход','Расход'):
                break
            else:
                print("Выберете правильно категорию(Регистр имеет значение!): Доход или Расход")
        while True:
            amount = input("Введите amount для добавления или нажмите Enter без изменения: ").strip()
            amount = self.check_amount(amount)
            if amount or amount==None:
                break
        while True:
            description = input("Введите description для добавления или нажмите Enter без изменения: ").strip()
            if len(description)>60 and len(description)>0:
                print("длина описания не больше 60 символов !!!")
            else:
                break
        r=self.wallet.add_record_and_save_file(date, category, amount, description)
        if r:
            print('Запись успешно добавлена !')
        else:
            print("Запись не удалось добавить (((")

    def edit_record(self, args):
        """
        Редактирует определенную запись по id.
        """
        print('welcome\n')
        while True:
            id_input = input("Введите id для редактирования или нажмите Enter без изменения: ").strip()
            id = self.check_id(id_input)
            if id:
                break

        while True:
            date = input("Введите дату для редактирования в формате YYYY-MM-DD или нажмите Enter без изменения: ").strip()
            date = self.check_date(date, flag=True)

            if date or date==None:
                break

        while True:
            category = input("Введите category(Доход/Расход) для редактирования или нажмите Enter без изменения: ").strip()
            if category in ('Доход','Расход',''):
                break
            else:
                print("Выберете правильно категорию(Регистр имеет значение!): Доход или Расход")
        while True:
            amount = input("Введите amount для редактирования или нажмите Enter без изменения: ").strip()
            amount = self.check_amount(amount, flag=True)
            if amount or amount==None:
                break
        while True:
            description = input("Введите description для редактирования или нажмите Enter без изменения: ").strip()
            if len(description)>60 and len(description)>0:
                print("длина описания не больше 60 символов !!!")
            else:
                break

        if self.wallet.edit_record_in_file(id,date,category,amount,description):
            print('Запись успешно отредактирована!')
        else:
            print("Запись отредактировать не удалось (((")

    def search_records(self,args=None)->None:
        """
        Производит поиск записей по одному из параметров дата, категория или сумма.

        """
        while True:
            print("======================")
            date = input("Введите дату для поиска в формате YYYY-MM-DD или нажмите Enter без изменения: ").strip()
            date = self.check_date(date, flag=True)
            if date or date==None:
                print('whileeeeeeeeeeeeeeeeeeee')
                break
        while True:
            category = input("Введите category(Доход/Расход) для поиска или нажмите Enter без изменения: ").strip()
            if category in ('Доход','Расход',''):
                break
            else:
                print("Выберете правильно категорию(Регистр имеет значение!): Доход или Расход")
        while True:
            amount = input("Введите amount для поиска  записей или нажмите Enter без изменения: ").strip()
            amount = self.check_amount(amount, flag=True)
            if amount or amount==None:
                break

        find_records = self.wallet.find_records(date=date, category=category, amount=amount)
        if find_records:
            for r in find_records:
                r.get_info()
        else:
            print("Записи не были найдены (((")

if __name__ == "__main__":
    wallet = PersonalTracker()
    wallet.load_records_from_file()
    interface = ConsoleInterface(wallet)
    interface.start()



