from common.errors.IsFullException import IsFullException

class Stack:

    MAX = 20
    values = []
    sorted = []

    def push(self, item):
        # Check if input is an int
        if(not(isinstance(item, int))):
            raise TypeError("The provided value must be an valid integer")
        # Check if stack is full
        if(self.isFull()):
            raise IsFullException(f"Cannot stack more than {self.MAX} items")
        # Add item to stack and reference arrays
        self.values.append(item)
        self.sorted.append(item)
        # Sort reference array
        self.sorted = self.sort(self.sorted)

    def peek(self):
        if(not(self.isEmpty())):
            return self.values[len(self.values) - 1]

    def pop(self):
        if(not(self.isEmpty())):
            del self.values[len(self.values) - 1]

    def sort(self, toSort):
        for i, e in reversed(list(enumerate(toSort))):
            if(toSort[i] < toSort[i-1] and i > 0):
                toSort[i], toSort[i-1] = toSort[i-1], toSort[i]
        return toSort

    def max(self):
        if(not(self.isEmpty())):
            return self.sorted[len(self.values) - 1]

    def min(self):
        if(not(self.isEmpty())):
            return self.sorted[0]

    def isEmpty(self):
        if(len(self.values)):
            return False
        return True

    def isFull(self):
        if(len(self.values) == self.MAX + 1):
            return True
        return False

    def __str__(self):
        for idx, value in list(enumerate(self.values)):
            print(f"[{idx}] : {value}")
