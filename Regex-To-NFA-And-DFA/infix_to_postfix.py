
def infix_to_postfix(infix:str)->str:
    precedence = dict()
    precedence['*'] = 5
    precedence['+'] = 4
    precedence['?'] = 3
    precedence['#'] = 2     # Concatenation
    precedence['|'] = 1
    precedence['['] = 0
    precedence['('] = 0

    upper_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    # add concatenation operator
    infix = list(infix)
    j = 0
    classes = False
    for i in range(len(infix)-1):
        if infix[j] == '[':
            classes = True
        if infix[j] == ']':
            classes = False
        if (infix[j].isalnum() or infix[j] == ')' or infix[j] == ']') and (infix[j+1].isalnum() or infix[j+1] == '(' or infix[j+1] == '[') and not classes:
            infix.insert(j+1, '#')
            j += 1

        j += 1

    stack = []
    postfix = []
    classes = False

    #unhandled cases for infix to postfix conversion
    # ( ) empty parenthesis
    # [ ] empty square bracket
    i = -1
    skip = False                # is used to skip the next character in the infix expression if it was handeled in the previous iteration like the '-' character
    for c in infix:
        i += 1
        if skip:
            skip = False
            continue

        if c == '(':
            # TODO: might need to fix the case where '(' is inside a square bracket
            stack.append(c)
        elif c == '[':
            stack.append(c)
            classes = True

        elif c == ')':
            while stack[-1] != '(':
                postfix.append(stack.pop())
                if len(stack) == 0:
                    return False            # Unmatched parenthesis
            stack.pop()

        elif c == ']':
            while stack[-1] != '[':
                postfix.append(stack.pop())
                if len(stack) == 0:
                    return False            # Unmatched square bracket
            classes = False
            stack.pop()

        elif c in precedence:
            while len(stack) > 0 and precedence[stack[-1]] >= precedence[c]:
                postfix.append(stack.pop())
            stack.append(c)
        elif c == '-':
            if not classes:
                return False                # '-' is not in a square bracket
            prev_char = postfix[-1]
            next_char = infix[i+1]
            upper = (prev_char in upper_alphabet and next_char in upper_alphabet)
            lower = (prev_char in lower_alphabet and next_char in lower_alphabet)
            digit = (prev_char in digits and next_char in digits)
            if not (upper or lower or digit):
                return False                # '-' is not between two same type of characters
            postfix[-1] = prev_char + '-' + next_char
            i += 1
            skip = True
        elif c.isalnum() or c == '.':
            postfix.append(c)
            if classes and (infix[i-1].isalnum() or infix[i-1] == '.'):
                postfix.append('|')

        else:
            return False                    # Invalid character
    while len(stack) > 0:
        postfix.append(stack.pop())
    if '(' in postfix or ')' in postfix:
        return False                        # Unmatched parenthesis
    if '[' in postfix or ']' in postfix:
        return False                        # Unmatched square bracket
    return postfix


if __name__ == "__main__":
    infix = "ab|cd(ef|d)[ghlma][a-z]"
    print(infix_to_postfix(infix))
