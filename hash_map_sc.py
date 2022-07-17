# Name: Alyssa Feutz
# OSU Email: feutza@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment #6 - Chaining for Collision Resolution
# Due Date: June 3rd, 2022
# Description: HashMap Implementation - Chaining Using Singly Linked List


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        Method that takes as a parameter a key/value pair, and updates the hash map by either adding the
        key/value or replacing the value for an already present key
        """
        # Hash the key
        array_index = self._hash_function(key) % self.get_capacity()
        # Go to relevant linked list based on hash value
        linked_list = self._buckets[array_index]
        # If linked list is empty, establish new one
        if linked_list.length() == None:
            new_linked_list = LinkedList()
            new_linked_list.insert(key, value)
            self._buckets[array_index] = new_linked_list
            self._size += 1
        # Otherwise, check if key already exists and either update or add key value pair
        else:
            contains_key = linked_list.contains(key)
            if contains_key is None:
                linked_list.insert(key, value)
                self._size += 1
            else:
                linked_list.remove(key)
                linked_list.insert(key, value)

    def empty_buckets(self) -> int:
        """
        Method that returns the number of empty buckets in the hash map
        """
        number_of_buckets = 0
        number_of_empty_buckets = 0
        for item in range(self.get_capacity()):
            if self._buckets[item] == None:
                number_of_buckets += 1
            elif self._buckets[item]._head == None: #todo
                number_of_empty_buckets += 1
            else:
                number_of_buckets += 1
        return number_of_empty_buckets


    def table_load(self) -> float:
        """
        Method that returns the current hash table load factor
        """
        number_of_elements = self.get_size()
        number_of_buckets = self.get_capacity()
        load_factor = number_of_elements/number_of_buckets
        return load_factor

    def clear(self) -> None:
        """
        Method that clears the contents of a hash map
        """
        for item in range(self.get_capacity()):
            self._buckets[item] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that changes the capacity of the hash map.
        """
        if new_capacity < 1:
            return
        new_da = DynamicArray()
        new_da_index = 0
        for array_index in range(self.get_capacity()):
            for node in self._buckets[array_index]:
                key_value_tuple = (node.key, node.value)
                new_da.append(key_value_tuple)
                new_da_index += 1
                # new_da.self._data += 1
        new_hash_map = HashMap(new_capacity, self._hash_function)
        for array_index in range(new_da.length()):
            new_hash_map.put(new_da[array_index][0], new_da[array_index][1])
        self._capacity = new_capacity
        self._buckets = new_hash_map._buckets



    def get(self, key: str) -> object:
        """
        Method that returns the value associated with the given parameter, which is a key,
        and returns None if the key is not in the hash map.
        """
        array_index = self._hash_function(key) % self.get_capacity()
        linked_list = self._buckets[array_index]
        value_of_key = None
        # Scenario for empty linked list
        if linked_list.length() == None:
            return None
        else:
            key_contents = linked_list.contains(key)
            # If linked list doesn't contain key
            if key_contents is None:
                return None
            else:
                return key_contents.value


    def contains_key(self, key: str) -> bool:
        """
        Method that takes as a parameter a key and returns True if the key is in
        the hash map and False otherwise
        """
        array_index = self._hash_function(key) % self.get_capacity()
        linked_list = self._buckets[array_index]
        value_of_key = None
        # Scenario for empty linked list
        if linked_list.length() == None:
            return False
        else:
            key_contents = linked_list.contains(key)
            # If linked list doesn't contain key
            if key_contents is None:
                return False
            else:
                return True

    def remove(self, key: str) -> None:
        """
        Method that takes as a parameter a key and removes the key and associated value
        from hash map.
        """
        array_index = self._hash_function(key) % self.get_capacity()
        linked_list = self._buckets[array_index]
        if linked_list.length() == None:
            return None
        else:
            contains_key = linked_list.contains(key)
            if contains_key is None:
                return None
            else:
                linked_list.remove(key)
                self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Method that returns a dynamic array that contains all of the keys stored in the hash map
        """
        new_da = DynamicArray()
        new_da_index = 0
        for array_index in range(self.get_capacity()):
            for node in self._buckets[array_index]:
                key_value = (node.key)
                new_da.append(key_value)
                new_da_index += 1
        return new_da


    def put_mode(self, key: str, value: object) -> None:
        """
        Method that takes as a parameter a key/value pair, and updates the hash map by either adding the
        key/value or replacing the value for an already present key, to be used by mode function
        """
        # Hash the key
        array_index = self._hash_function(key) % self.get_capacity()
        # Go to relevant linked list based on hash value
        linked_list = self._buckets[array_index]
        # If linked list is empty, establish new one
        if linked_list.length() == None:
            new_linked_list = LinkedList()
            new_linked_list.insert(key, value)
            self._buckets[array_index] = new_linked_list
            self._size += 1
        # Otherwise, check if key already exists and either update or add key value pair
        else:
            contains_key = linked_list.contains(key)
            if contains_key is None:
                linked_list.insert(key, value)
                self._size += 1
            else:
                for item in linked_list:
                    if item.key == key:
                        current_value = item.value
                linked_list.remove(key)
                linked_list.insert(key, current_value + 1)


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function that takes as a parameter a dynamic array and returns a tuple containing a dynamic array comprising
    the mode value(s) of the array and an integer that represents the highest frequency
    """
    # Pre-work: establish variables
    map = HashMap(da.length() // 3, hash_function_1)
    map_capacity = map.get_capacity()
    most_occurrences = 0
    dynamic_array_of_modes = DynamicArray()

    # Step 1: Add items from dynamic array to hash map.  Value is the number of occurrences
    for item in range(da.length()):
        map.put_mode(da[item], 1)
    # Step 2: Iterate through hash map and find greatest value, which is greatest number of occurrences
    for array_index in range(map_capacity):
        if map._buckets[array_index]:
            linked_list = map._buckets[array_index]
            for item in linked_list:
                if item.value > most_occurrences:
                    most_occurrences = item.value
    # Step 3: Iterate through hash map, if value is greatest number of occurrences, add key to dynamic array of modes
    for array_index in range(map_capacity):
        if map._buckets[array_index]:
            linked_list = map._buckets[array_index]
            for item in linked_list:
                if item.value == most_occurrences:
                    dynamic_array_of_modes.append(item.key)
    return (dynamic_array_of_modes, most_occurrences)





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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
