# Реверсування, сортування вставками та обʼєднання в один відсортований список на прикладі реализації списку з конспекту
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # ---------- ВСТАВКИ ----------
    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    # ---------- ДРУК ----------
    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data)
            cur = cur.next

    # ---------- РЕВЕРС ----------
    def reverse(self):
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    # ---------- СОРТУВАННЯ ВСТАВКАМИ ----------
    def insertion_sort(self):
        if not self.head or not self.head.next:
            return

        sorted_head = None
        current = self.head

        while current:
            next_node = current.next

            if sorted_head is None or current.data < sorted_head.data:
                current.next = sorted_head
                sorted_head = current
            else:
                search = sorted_head
                while search.next and search.next.data < current.data:
                    search = search.next

                current.next = search.next
                search.next = current

            current = next_node

        self.head = sorted_head

    # ---------- MERGE ДВОХ ВІДСОРТОВАНИХ СПИСКІВ ----------
    def merge_sorted(self, other: "LinkedList"):
        self.head = merge_sorted_nodes(self.head, other.head)


# ---------- ФУНКЦІЯ MERGE ДЛЯ ВУЗЛІВ ----------
def merge_sorted_nodes(l1, l2):
    if not l1:
        return l2
    if not l2:
        return l1

    if l1.data <= l2.data:
        head = l1
        l1 = l1.next
    else:
        head = l2
        l2 = l2.next

    current = head

    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2
    return head


# =======================
# ПРИКЛАД ВИКОРИСТАННЯ
# =======================

# --- Перший список: 15 → 10 → 5 → 20 → 25
list1 = LinkedList()
list1.insert_at_beginning(5)
list1.insert_at_beginning(10)
list1.insert_at_beginning(15)
list1.insert_at_end(20)
list1.insert_at_end(25)

print("Перший список:")
list1.print_list()

list1.reverse()
print("\nПісля реверсування:")
list1.print_list()

list1.insertion_sort()
print("\nПісля сортування вставками:")
list1.print_list()

# --- Другий відсортований список
list2 = LinkedList()
for x in [2, 12, 30]:
    list2.insert_at_end(x)

print("\nДругий відсортований список:")
list2.print_list()

# --- Обʼєднання
list1.merge_sorted(list2)
print("\nПісля обʼєднання двох відсортованих списків:")
list1.print_list()
