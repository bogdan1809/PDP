from node import Node
from threading import Thread, Lock
import random

nodes_list = []
nodes_list.append(Node(27, 1, None))
nodes_list.append(Node(27, 2, 1))
nodes_list.append(Node(12, 3, 2))
nodes_list.append(Node(15, 4, 2))
nodes_list.append(Node(3, 5, 3))
nodes_list.append(Node(7, 6, 3))
nodes_list.append(Node(2, 7, 3))
nodes_list.append(Node(1, 8, 4))
nodes_list.append(Node(14, 9, 4))

leaf_nodes=[]
leaf_nodes.append(Node(3, 5, 3))
leaf_nodes.append(Node(7, 6, 3))
leaf_nodes.append(Node(2, 7, 3))
leaf_nodes.append(Node(1, 8, 4))
leaf_nodes.append(Node(14, 9, 4))


class InputThread(Thread):
    def run(self):
        leaf=random.choice(leaf_nodes)
        new_value=random.randint(1,50)


if __name__ == '__main__':
