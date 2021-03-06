# Name: Alyssa Feutz
# OSU Email: feutza@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment #6 - Open Addressing
# Due Date: June 3rd, 2022
# Description: HashMap Implementation - Open Addressing with Quadratic Probing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method that takes as parameters a key and a value and either updates the value associated with
        the key, or adds the key and value pair to the hash map.
        """
        # resize the table if load factor is greater than or equal to 0.5 before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity()*2)
        initial_index = self._hash_function(key) % self.get_capacity()
        array_index = initial_index
        if self._buckets[initial_index] == None:
            self._buckets[initial_index] = HashEntry(key, value)
            self._size += 1
            return
        else:
            j = 1
            while self._buckets[array_index] != None:
                if self._buckets[array_index].key == key:
                    self._buckets[array_index] = HashEntry(key, value)
                    return
                array_index = (initial_index + j*j) % self.get_capacity()
                if self._buckets[array_index] == None:
                    self._buckets[array_index] = HashEntry(key, value)
                    self._size += 1
                    return

                else:
                    j += 1


    def table_load(self) -> float:
        """
        Method that returns the current hash table load factor
        """
        number_of_elements = self.get_size()
        number_of_buckets = self.get_capacity()
        load_factor = number_of_elements/number_of_buckets
        return load_factor

    def empty_buckets(self) -> int:
        """
        Method that returns the number of empty buckets in the hash table
        """
        empty_buckets = self.get_capacity() - self.get_size()
        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that takes as a parameter the new capacity of the internal hash table, and rehashes all hash table
        links
        """
        # invalid capacity returns nothing
        if new_capacity < 1 or new_capacity < self.get_size():
            return
        old_size = self.get_size()
        old_capacity = self.get_capacity()
        new_da = DynamicArray()
        new_da_index = 0
        # Part one: copy info from self to new_da, which will be a copy
        for hash_entry in range(self.get_capacity()):
            if self._buckets[hash_entry] == None:
                pass
            elif self._buckets[hash_entry].is_tombstone == False:
                new_da.append(self._buckets[hash_entry])
                new_da_index += 1
        # Clear self
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        for item in range(new_capacity):
            self._buckets.append(None)
        self._size = 0
        # Use new_da as a base to rehash into self
        for hash_entry in range(old_capacity):
            self.put(new_da[hash_entry].key, new_da[hash_entry].value)


    def get(self, key: str) -> object:
        """
        Method that takes as a parameter a key and returns the value associated with the given key
        """
        if self._size == 0:
            return None
        for item in range(self.get_capacity()):
            if self._buckets[item] != None:
                if self._buckets[item].key == key and self._buckets[item].is_tombstone == False:
                    return self._buckets[item].value
        return None


    def contains_key(self, key: str) -> bool:
        """
        Method that takes as a parameter a key and returns True if the key is in the hash map and False otherwise
        """
        if self.get_size() == 0:
            return False
        for item in range(self.get_capacity()):
            if self._buckets[item] != None:
                if self._buckets[item].key == key and self._buckets[item].is_tombstone == False:
                    return True
        return False

    def remove(self, key: str) -> None:
        """
        Method that takes as a parameter a key and removes the associated key and value pair from the hash map
        """
        if self.get_size() == 0:
            return None
        for item in range(self.get_capacity()):
            if self._buckets[item] != None:
                if self._buckets[item].key == key and self._buckets[item].is_tombstone == False:
                    self._buckets[item].is_tombstone = True
                    self._size -= 1
                    return
        return

    def clear(self) -> None:
        """
        Method that clears the contents of the hash map
        """
        for item in range(self.get_capacity()):
            self._buckets[item] = None
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Method that returns a dynamic array that contains all of the keys stored in the hash map
        """
        new_da = DynamicArray()
        for item in range(self.get_capacity()):
            if self._buckets[item] != None:
                if self._buckets[item].key != None and self._buckets[item].is_tombstone == False:
                    new_da.append(self._buckets[item].key)
        return new_da


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
