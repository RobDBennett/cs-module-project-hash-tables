class HashTableEntry:
    """
    Treating this like a Linked_List.
    Added several methods so that the nodes themselves could recall relevant data.
    get_key, get_value, get_next, set_next, set_value are all important in changing
    different values in the HashTable class.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_next(self):
        return self.next
    
    def set_next(self, entry):
        self.next = entry
    
    def set_value(self, value):
        self.value = value


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8

class HashTable:
    """
    Requires a min_capacity to function- set default to what is presented
    as default in this document.
    Also created a number of 'buckets' for the array.
    Added counter object to track the number of items in the array for searching.
    """

    def __init__(self, capacity=MIN_CAPACITY):
        self.capacity= capacity
        self.array = [None] * capacity
        self.number_of_items = 0


    def get_num_slots(self):
        """
        Returns the length of the array. 
        Effectively the number of buckets we have generated.
        """
        return len(self.array)


    def get_load_factor(self):
        """
        The load factor is the number of items currently stored in the array
        divided by the maximum number of buckets. This gives you the current
        load factor for the hashtable
        """
        return self.number_of_items / self.capacity        


    def fnv1(self, key):
        """
        This formula was lifted directly from the pseudo code presented
        on Wikipedia.
        """
        fnv_offset = 14695981039346656037 #offset_basis- from Wikipedia
        fnv_prime = 1099511628211 #FNV_prime- from Wikipedia
        hash = fnv_offset
        key_utf8 = key.encode()

        for byte in key_utf8:
            hash = hash ^ byte
            hash = hash ^ fnv_prime
        return hash
        

    def djb2(self, key):
        """
        Formula taken from brilliant.org/wiki/hash-tables
        """
        hash = 5381
        byte_array = key.encode()
        for byte in byte_array:
            hash = ((hash * 33) ^ byte) % 0x100000000
        return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        Changed pointer to fnv
        """
        return self.fnv1(key) % self.capacity
        #return self.djb2(key) % self.capacity


    def put(self, key, value):
        """
        Checks the current load_factor against a static value of 70%. If current capacity is 70+% filled,
        resizes the capacity.
        Sets index, new entry, and increases counts.
        Places items into linked_list format.
        Checks for collision 
        """
        if self.get_load_factor() > .7:
            self.resize(self.capacity * 2)

        index = self.hash_index(key)
        entry = HashTableEntry(key, value)
        self.number_of_items += 1

        if self.array[index] == None:
            self.array[index] = entry
        else:
            current_node = self.array[index]
            while current_node != None:
                if current_node.get_key() == key:
                    current_node.set_value(value)
                    return
                elif current_node.get_next() == None:
                    current_node.set_next(entry)
                current_node = current_node.get_next()


    def delete(self, key):
        """
        Removes item as linked_list removal. 
        Shifts pointers along the nodes.
        Gives a warning if the key to delete isn't present.
        """
        #index = self.hash_index(key)
        #current_node = self.array[index]
        #prev_entry = None
        if self.get(key):
            index = self.hash_index(key)
            current_node = self.array[index]
            prev_entry = None 
        else:
            print(f"Warning: Tried to delete a value from HashTable but no value exists for key: '{key}'")

        while current_node != None:
            if current_node.get_key() == key:
                self.number_of_items -= 1
                if prev_entry == None:
                    current_node.set_value(None)
                else:
                    prev_entry.set_next(current_node.get_next())
            
            prev_entry = current_node
            current_node = current_node.get_next()
        
        if self.get_load_factor() < 0.2:
            new_capacity = self.capacity // 2
            if new_capacity < MIN_CAPACITY:
                self.resize(MIN_CAPACITY)
            else:
                self.resize(new_capacity)


    def get(self, key):
        """
        Generates hash key. Checks array at the index.
        If that entry is still None, returns None. Otherwise moves along the 
        linked_list to find entry.
        """
        index = self.hash_index(key)
        entry = self.array[index]
        if entry is None:
            return None
        while entry != None:
            if entry.get_key() == key:
                return entry.get_value()
            entry = entry.get_next()
        return None


    def resize(self, new_capacity):
        """
        Creates an object for the old array. Resets array to a new capacity.
        Runs through the old array to input values into new array.
        """
        old_array = self.array
        self.array = [None] * new_capacity
        self.capacity = new_capacity

        for index in range(len(old_array)):
            current_node = old_array[index]
            while current_node != None:
                self.put(current_node.get_key(), current_node.get_value())
                current_node = current_node.get_next()



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
