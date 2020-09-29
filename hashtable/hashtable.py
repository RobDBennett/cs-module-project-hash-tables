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

    def __repr__(self):
        return f"HashTableEntry({repr(self.key)}, {repr(self.value)})"

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

    def __repr__(self):
        return f"HashTable({repr(self.capacity)}, {repr(len(self.array))}, {repr(self.number_of_items)})"

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
        This is a somewhat black box to me. A large number generator.
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
        if self.get_load_factor() > .7: #Checks load factor. If its too high, it resizes the capacity.
            self.resize(self.capacity * 2) #Standard convention is doubling the size of the hashtable.

        index = self.hash_index(key) #Generates hash 'address'
        entry = HashTableEntry(key, value) #Creates a node for the given key/value pair
        self.number_of_items += 1 #Iterates up the number of items

        if self.array[index] == None: #Checks if the given array 'address' is empty
            self.array[index] = entry #If so, puts the new node there.
        else:
            current_node = self.array[index]
            while current_node != None:
                if current_node.get_key() == key: #Otherwise it checks to see if the key is already present.
                    current_node.set_value(value) #If so, it updates the value to the new values.
                    return
                elif current_node.get_next() == None: #Checks if the current nodes at address is the 'head'.
                    current_node.set_next(entry) #If so, adds new node to the end of the node chain
                current_node = current_node.get_next() #Otherwise, moves down the node-list, checking if the key exists, and adding to the tail.


    def delete(self, key):
        """
        Removes item as linked_list removal. 
        Shifts pointers along the nodes.
        Gives a warning if the key to delete isn't present.
        """
        if self.get(key): #Starts by finding if the key currently exists
            index = self.hash_index(key) #Set hash 'address'
            current_node = self.array[index] #Set current node we are looking at to the addressed node
            prev_entry = None  #Create a second pointer.
        else: #If key can't be found, raise a warning.
            return print(f"Warning: Tried to delete a value from HashTable but no value exists for key: '{key}'")

        while current_node != None: #Start a loop for as long as there is a current_node pointer
            if current_node.get_key() == key: #Checks if the current node is the key to delete.
                self.number_of_items -= 1 #Lowers the items in storage by one.
                if prev_entry == None: #Checks if the second pointer has moved.
                    current_node.set_value(None) #Deletes the current node if second pointer hasn't moved.
                else:
                    prev_entry.set_next(current_node.get_next()) #sets second pointer down the track from current pointer.
            
            prev_entry = current_node #If key wasn't found, set second pointer to first pointer
            current_node = current_node.get_next() #And first pointer to next linked list item. This will repeat until current_node becomes None.
        
        if self.get_load_factor() < 0.2: #After deleting item, checks load size against a 20% full capacity.
            new_capacity = self.capacity // 2 #If list is less than 20% full, it will set a new capacity as half of the current list
            if new_capacity < MIN_CAPACITY: #Checks if half of the current list is lower than the minimum capacity.
                self.resize(MIN_CAPACITY) #If so, resize to minimum capacity.
            else:
                self.resize(new_capacity) #Otherwise, resizes the hashtable to half of the previous capacity.


    def get(self, key):
        """
        Generates hash key. Checks array at the index.
        If that entry is still None, returns None. Otherwise moves along the 
        linked_list to find entry.
        """
        index = self.hash_index(key) #Generates hash address
        entry = self.array[index] #Points to the array at hash address
        if entry is None: #If there isn't a value stored at that address, return None
            return None
        while entry != None: #Otherwise run through the list
            if entry.get_key() == key: #Check if the key of the current node at that array address is the key.
                return entry.get_value() #If so, return the value.
            entry = entry.get_next() #If not, move the current node down a position in the linked list.
        return None


    def resize(self, new_capacity):
        """
        Creates an object for the old array. Resets array to a new capacity.
        Runs through the old array to input values into new array.
        """
        old_array = self.array #Move the data currently stored in the hashtable into a new variable
        self.array = [None] * new_capacity #Reset everything previously stored in the table to a number of buckets equal to the new capacity
        self.capacity = new_capacity #Set capacity to the new capacity
        self.number_of_items = 0 #Reset the counter to 0

        for index in range(len(old_array)): #Iterate over the storage array 
            current_node = old_array[index] #Set the pointer to the first point in that array
            while current_node != None: #If that node isn't empty, 'put' that key/value pair into a new node via 'put'
                self.put(current_node.get_key(), current_node.get_value())
                current_node = current_node.get_next() #Shift pointer down node.


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
