from __future__ import annotations
import utils
from dataclasses import dataclass


@dataclass
class Node:
    val: int
    prev: Node
    next: Node


def parse_input(path):
    lines = utils.read_lines(path)

    return [int(l) for l in lines]


def to_linked_nodes(data):
    cur: Node = None
    head: Node = None

    all_nodes = set()

    for n in data:
        new_node = Node(n, cur, None)
        if cur:
            cur.next = new_node
        cur = new_node
        if not head:
            head = cur

    head.prev = cur
    cur.next = head

    return head


def get_node_list(node: Node):
    result = []
    cur = node

    while True:
        result.append(cur)
        cur = cur.next
        if cur == node:
            return result


def to_normal_list(node: Node):
    result = []
    cur = node

    while True:
        result.append(cur.val)
        cur = cur.next
        if cur == node:
            return result


def rearrange_nodes(head, node_list):
    num_nodes = len(node_list)

    for cur in node_list:
        n = cur.val
        insert_after = cur
        if n > 0:
            n = n % (num_nodes - 1)
            insert_after = cur
            for i in range(n):
                insert_after = insert_after.next

        if n < 0:
            n = (-n + 1) % (num_nodes - 1)
            insert_after = cur
            for i in range(n):
                insert_after = insert_after.prev

        if insert_after != cur:
            prev = cur.prev
            next = cur.next

            prev.next = next
            next.prev = prev

            insert_before = insert_after.next

            insert_after.next = cur
            insert_before.prev = cur
            cur.prev = insert_after
            cur.next = insert_before

    while cur.val != 0:
        cur = cur.next

    return cur


def part1(path):
    data = parse_input(path)

    head = to_linked_nodes(data)
    node_list = get_node_list(head)
    head = rearrange_nodes(head, node_list)

    cur = head
    for i in range(1000):
        cur = cur.next
    a = cur.val
    for i in range(1000):
        cur = cur.next
    b = cur.val
    for i in range(1000):
        cur = cur.next
    c = cur.val

    print(a + b + c)


def part2(path):
    data = parse_input(path)

    data = [n * 811589153 for n in data]

    head = to_linked_nodes(data)
    node_list = get_node_list(head)

    cur = head
    for i in range(10):
        cur = rearrange_nodes(cur, node_list)

    for i in range(1000):
        cur = cur.next
    a = cur.val
    for i in range(1000):
        cur = cur.next
    b = cur.val
    for i in range(1000):
        cur = cur.next
    c = cur.val

    print(a + b + c)