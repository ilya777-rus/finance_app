import unittest
from datetime import date
from unittest.mock import patch

from main import PersonalTracker, Record, ConsoleInterface


class TestConsoleInterface(unittest.TestCase):
    def setUp(self):
        self.tracker = PersonalTracker()
        self.record1 = Record(1, date(2024, 5, 10), "Доход", 50, "зарплата")
        self.record2 = Record(2, date(2024, 5, 11), "Расход", 30, "трата")
        self.tracker.add_record(self.record1)
        self.tracker.add_record(self.record2)
        self.interface = ConsoleInterface(self.tracker)

    def test_check_id(self):
        # Проверяем, корректно ли проверяется id
        self.assertEqual(self.interface.check_id(1), 1)

    def test_check_amount(self):
        # Проверяем, корректно ли проверяется amount
        self.assertEqual(self.interface.check_amount("100"), 100)

    def test_check_date(self):
        # Проверяем, корректно ли проверяется date
        self.assertEqual(self.interface.check_date("2024-05-10"), date(2024, 5, 10))

    @patch('builtins.input', side_effect=['2024-1-1','Доход', '110', 'description'])
    def test_add_record(self, mock_input):
        count = len(self.tracker.records)
        self.interface.add_record(None)
        self.assertEqual(len(self.tracker.records),count+1)

    @patch('builtins.input', side_effect=['1','2024-5-10','Доход', '50', 'update_description'])
    def test_edit_record(self, mock_input):
        self.interface.edit_record(None)
        updated_description=self.tracker.records[0].description
        self.assertEqual(updated_description, 'update_description')

class TestPersonalTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = PersonalTracker()
        self.record1 = Record(1, date(2024, 5, 10), "Доход", 50, "зарплата")
        self.record2 = Record(2, date(2024, 5, 11), "Расход", 30, "трата")
        self.tracker.add_record(self.record1)
        self.tracker.add_record(self.record2)

    def tearDown(self):
        del self.tracker

    def test_add_record(self):
        self.assertEqual(len(self.tracker.records),2)
        new_record = Record(3, date(2024, 5, 12), "Доход", 20, "описание")
        self.tracker.add_record(new_record)
        self.assertEqual(len(self.tracker.records),3)
        self.assertIn(new_record, self.tracker.records)

    def test_save_and_load_records(self):
        self.assertTrue(self.tracker.save_records_to_file())

        new_tracker = PersonalTracker()
        new_tracker.load_records_from_file()

        self.assertEqual(len(self.tracker.records),len(new_tracker.records))
        for rec1,rec2 in zip(self.tracker.records, new_tracker.records):
            self.assertEqual(rec1.id,rec2.id)
            self.assertEqual(rec1.date,rec2.date)
            self.assertEqual(rec1.category, rec2.category)
            self.assertEqual(rec1.amount, rec2.amount)
            self.assertEqual(rec1.description, rec2.description)

    def test_add_record_and_save_file(self):
        new_record = Record(3, date(2024, 5, 12), "Доход", 20, "описание")
        self.assertTrue(self.tracker.add_record_and_save_file(new_record.date, new_record.category, new_record.amount,
                                                              new_record.description))
        self.assertEqual(len(self.tracker.records), 3)
        for rec1,rec2 in zip([new_record], [self.tracker.records[2]]):
            self.assertEqual(rec1.id,rec2.id)
            self.assertEqual(rec1.date, rec2.date)
            self.assertEqual(rec1.category, rec2.category)
            self.assertEqual(rec1.amount, rec2.amount)
            self.assertEqual(rec1.description, rec2.description)

    def test_edit_record_in_file(self):
        # Тестирование редактирования записи в файле
        # Тестирование изменения даты записи
        self.assertTrue(self.tracker.edit_record_in_file(1, date(2024, 5, 11), None, None, None))
        self.assertEqual(self.tracker.records[0].date, date(2024, 5, 11))

        # Тестирование изменения категории записи
        self.assertTrue(self.tracker.edit_record_in_file(1, None, "Расход", None, None))
        self.assertEqual(self.tracker.records[0].category, "Расход")

        # Тестирование изменения суммы записи
        self.assertTrue(self.tracker.edit_record_in_file(1, None, None, 100, None))
        self.assertEqual(self.tracker.records[0].amount, 100)

        # Тестирование изменения описания записи
        self.assertTrue(self.tracker.edit_record_in_file(1, None, None, None, "New description"))
        self.assertEqual(self.tracker.records[0].description, "New description")

        # Тестирование изменения несуществующей записи
        self.assertFalse(self.tracker.edit_record_in_file(100, None, None, None, None))

    def test_find_records(self):
        # Тестирование поиска записей
        # Тестирование поиска записей по категории
        self.assertEqual(len(self.tracker.find_records(category="Доход")), 1)
        self.assertEqual(self.tracker.find_records(category="Доход")[0], self.record1)

        # Тестирование поиска записей по дате
        self.assertEqual(len(self.tracker.find_records(date=date(2024, 5, 11))), 1)
        self.assertEqual(self.tracker.find_records(date=date(2024, 5, 11))[0], self.record2)

        # Тестирование поиска записей с недопустимыми критериями
        self.assertIsNone(self.tracker.find_records(category="выаыва"))

    def test_balance(self):
        # Тестирование расчета баланса
        self.assertEqual(self.tracker.balance(), (50, 30, 20))

if __name__ == "__main__":
    unittest.main()