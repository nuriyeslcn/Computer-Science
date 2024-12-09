class Node(object):
    # Doubly linked node
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev


class doubly_linked_list(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def insert_item(self, data, i):

        new_item = Node(data, None, None)

        # If list is empty
        if self.head is None:
            self.head = new_item
            self.tail = self.head

        # If list list is not empty
        else:
            # If appending at the end
            if i >= self.count:
                new_item.prev = self.tail
                self.tail.next = new_item
                self.tail = new_item

            elif i < 0:
                raise ValueError(
                    "{} is invalid index value for a list of size {}.".format(
                        i, self.count
                    )
                )

            else:  # Insert the item at index i
                # ToDo : replace pass with appropriate script
                pass

        self.count += 1

    def print_foward(self):
        for node in self.iter():
            print(node)

    def print_backward(self):
        current = self.tail
        while current:
            print(current.data)
            current = current.prev

    def iter(self):
        # Iterate the list
        current = self.head
        while current:
            item_val = current.data
            current = current.next
            yield item_val


# Example to test if the insert_item is working properly
# When you run this code, the forward print must print the items in this order:
# Java
# PHP
# Assembly
# Python
# C#
# C++

items = doubly_linked_list()
items.insert_item("PHP", 0)
items.insert_item("Python", 1)
items.insert_item("C#", 2)
items.insert_item("C++", 3)

items.insert_item("Java", 0)
items.insert_item("Assembly", 2)

print("Print Items in the Doubly linked forwad:")
items.print_foward()

print()
print("Print Items in the Doubly linked backwards:")
items.print_backward()
