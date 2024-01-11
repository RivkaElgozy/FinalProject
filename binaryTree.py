class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_operator(token):
    return token in ['+', '-', '*', '/', '^']


def precedence(operator):
    if operator == '+' or operator == '-':
        return 1
    elif operator == '*' or operator == '/':
        return 2
    elif operator == '^':
        return 3
    return 0


def infix_to_postfix(infix):
    postfix = []
    stack = []

    for token in infix:
        if token.isalnum():
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Pop '('
        elif is_operator(token):
            while stack and precedence(stack[-1]) >= precedence(token):
                postfix.append(stack.pop())
            stack.append(token)

    while stack:
        postfix.append(stack.pop())

    return postfix


def construct_binary_tree(postfix):
    stack = []

    for token in postfix:
        if token.isalnum():
            stack.append(Node(token))
        elif is_operator(token):
            right = stack.pop()
            left = stack.pop()
            operator_node = Node(token)
            operator_node.left = left
            operator_node.right = right
            stack.append(operator_node)

    return stack[0]  # The root of the binary tree


def equation_to_binary_tree(equation):
    infix_tokens = equation.replace(" ", "")
    infix_tokens = [char for char in infix_tokens]

    postfix_tokens = infix_to_postfix(infix_tokens)
    root = construct_binary_tree(postfix_tokens)

    return root