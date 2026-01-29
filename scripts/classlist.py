
class ClassList():
    
    def __init__(self, new_list=None, max_size=0):
        self._list = new_list if new_list else []
        self.max_size = max_size

    def reset(self):
        self._list = []

    def contains(self, element):
        return element in self._list

    def get_length(self):
        return len(self._list)

    def position_is_in_range(self, position):
        return position>=0 and position<len(self._list)

    def can_add_element(self):
        return len(self._list) < self.max_size

    def add(self, element):
        self._list.append(element)

    def get(self, position):
        if self.position_is_in_range(position):
            return self._list[position]

        return None

    def update(self, position, new_element):
        if self.position_is_in_range(position):
            self._list[position] = new_element
            return True

        return False

    def remove(self, position):
        if(self.position_is_in_range(position)):
            self._list.pop(position)
            return True

        return False