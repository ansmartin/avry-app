
class ClassList():
    
    def __init__(self, max_size:int = 0, new_list:list = []):
        self.max_size = max_size
        self._list = new_list

    def reset(self):
        self._list = []

    def contains(self, element) -> bool:
        return element in self._list

    def get_length(self) -> int:
        return len(self._list)

    def position_is_in_range(self, position:int) -> bool:
        return position>=0 and position<len(self._list)

    def can_add_element(self) -> bool:
        if self.max_size==0: # sin limite
            return True
        
        return len(self._list) < self.max_size

    def add(self, element):
        self._list.append(element)

    def get(self, position:int):
        if self.position_is_in_range(position):
            return self._list[position]

        return None

    def update(self, position:int, new_element) -> bool:
        if self.position_is_in_range(position):
            self._list[position] = new_element
            return True

        return False

    def remove(self, position:int) -> bool:
        if(self.position_is_in_range(position)):
            self._list.pop(position)
            return True

        return False