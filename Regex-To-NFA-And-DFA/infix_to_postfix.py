
def infix_to_postfix(infix:str):
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
    #checks operators and are at the beginning or end of the infix expression
    if infix[0] in ['*','+','?','|'] or infix[-1] in ['|']:
        return False,"Operator at the beginning or end of the expression"

    for i in range(len(infix)-1):
        # checks that an | operator is followed by a quantifier
        if infix[j] in ['*','+','?'] and infix[j+1] in ['*','+','?']:
            return False,"Quantifier Overwrite"
        if infix[j] == '|' and infix[j+1] in ['*','+','?',')',']']:
            return False,"| followed by a quantifier or a closing bracket"

        if infix[j] == '[':
            classes = True
        if infix[j] == ']':
            classes = False
        if (infix[j].isalnum() or infix[j] in [')',']','.','+','*','?']) and (infix[j+1].isalnum() or infix[j+1] == '(' or infix[j+1] == '[' or infix[j+1] == '.') and not classes:
            infix.insert(j+1, '#')
            j += 1

        j += 1

    stack = []
    postfix = []
    classes = False


    i = -1
    skip = False                # is used to skip the next character in the infix expression if it was handeled in the previous iteration like the '-' character
    for c in infix:
        i += 1
        if skip:
            skip = False
            continue

        if c == '(':
            stack.append(c)
            if infix[i+1] == ')':
                return False,"Empty parenthesis"            # Empty parenthesis
            if classes:
                return False,"'(' inside a square bracket"  # '(' inside a square bracket

        elif c == '[':
            stack.append(c)
            if infix[i+1] == ']':
                return False,"Empty square bracket"         # Empty square bracket
            classes = True

        elif c == ')':
            if classes:
                return False,"')' inside a square bracket"
            if len(stack) == 0:
                return False,"Unmatched parenthesis"        # Unmatched parenthesis
            while stack[-1] != '(':
                postfix.append(stack.pop())
                if len(stack) == 0:
                    return False,"Unmatched parenthesis"    # Unmatched parenthesis
            stack.pop()

        elif c == ']':
            if len(stack) == 0:
                return False,"Unmatched square bracket"     # Unmatched square bracket
            while stack[-1] != '[':
                postfix.append(stack.pop())
                if len(stack) == 0:
                    return False,"Unmatched square bracket" # Unmatched square bracket
            classes = False
            stack.pop()

        elif c in precedence:
            if classes:
                return False,"Operator inside a square bracket"         # Operator inside a square bracket # review this
            while len(stack) > 0 and precedence[stack[-1]] >= precedence[c]:
                postfix.append(stack.pop())
            stack.append(c)
        elif c == '-':
            if not classes:
                return False,"- not in square brackets"                # '-' is not in a square bracket
            prev_char = postfix[-1]
            take_prev = True
            if prev_char == '|':
                prev_char = postfix[-2]                                 # if the previous character is '|' then the character before it is the one we want
                take_prev = False
            next_char = infix[i+1]
            upper = (prev_char in upper_alphabet and next_char in upper_alphabet)
            lower = (prev_char in lower_alphabet and next_char in lower_alphabet)
            digit = (prev_char in digits and next_char in digits)
            if not (upper or lower or digit) or ord(next_char) < ord(prev_char): # next_char is before prev_char
                return False,"Pattern Error"                                    # '-' is not between two same type of characters or characters are not in order
            if take_prev:
                postfix[-1] = prev_char + '-' + next_char
            else:
                postfix[-2] = prev_char + '-' + next_char

            skip = True
        elif c.isalnum() or c == '.':
            postfix.append(c)
            if classes and (infix[i-1].isalnum() or infix[i-1] == '.'):
                postfix.append('|')

        else:
            return False,"Invalid character"# Invalid character
    while len(stack) > 0:
        postfix.append(stack.pop())
    if '(' in postfix or ')' in postfix:
        return False,"Unmatched parenthesis"# Unmatched parenthesis
    if '[' in postfix or ']' in postfix:
        return False,"Unmatched square bracket"# Unmatched square bracket
    return True,postfix


if __name__ == "__main__":
    infix = "ab|cd(ef|d)[ghlma][a-z]"
    print(infix_to_postfix(infix))
