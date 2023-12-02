from collections import UserDict
from datetime import date, datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):

    @Field.value.setter
    def value(self, value: str):
        if value == "1900.01.01":
            Field.value.fset(self, value)
        else:
            Field.value.fset(self, datetime.strptime(value, '%Y.%m.%d').date())
    
class Phone(Field):
    
    @Field.value.setter
    def value(self, value: str):
        if not self.validate(value):
            raise ValueError("Invalid phone number")
        Field.value.fset(self, value)
    
    def validate(self, value):
        return isinstance(value, str) and len(value) == 10 and value.isdigit()

class Record:
    def __init__(self, name, birthday = "1900.01.01"): 
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def days_to_birthday(self, name):
        if name == self.name.value:
            if self.birthday.value == "1900.01.01":
               return "В контакта не вказано дату народження"
            elif self.birthday != "1900.01.01":
                now = date.today()
                birth_this_year = self.birthday.value.replace(year=now.year)
                if birth_this_year < now:
                    next_birthday = self.birthday.value.replace(year=now.year+1)
                    result = next_birthday - now
                    return result.days
                else:
                    result = birth_this_year - now
                    return result.days
        else:
            print("Даного контакту не існує")
    
    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None    
            
    def edit_phone (self, old_phone, new_phone):
        count = 0
        for phone in self.phones:
            count += 1
            if phone.value == old_phone:
                next_number = Phone(new_phone)
                next_number.validate(new_phone)
                self.phones[self.phones.index(phone)] = next_number
                break
            if count == len(self.phones):
                raise ValueError
        
    
    def remove_phone (self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
