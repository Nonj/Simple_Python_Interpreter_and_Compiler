# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, EOF, MINUS, MUL, DIV = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MULTIPLY', 'DIVIDE'


'''
Extend the calculator to handle multiplication of two integers
Extend the calculator to handle division of two integers
Modify the code to interpret expressions containing an arbitrary number of additions and subtractions, for example “9 - 5 + 3 + 11”

'''


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, EOF
        self.type = type
        # token value: 0 ... 9, '+', or '-' or NONE
        self.value = value

    def __str__(self):
        """ String Representation of the class instance
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """ Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence apart into tokens. One at a time.
        """
        text = self.text

        # is self.pos index past the ned of the self.text?
        # if so, return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the characeter is a digit, then convert it
        # to integer, create an INTEGER token, increment
        # self.pos index to point to the next character
        # after the digit, and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token


        if current_char == '*':
            token = Token(MUL, current_char)
            self.pos += 1
            return token

        if current_char == '/':
            token = Token(DIV, current_char)
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed
        # token type, and if they match, then "eat" the
        # current token and assign the next token to the
        # self.current_token, otherwise raise an exception
        if (self.current_token.type == token_type):
            self.current_token = self.get_next_token()
        else:
            self.error()

    def no_space(self):
        self.text = self.text.replace(" ", "")

    def expr(self):
        """ expression -> INTEGER PLUS INTEGER """
        # set current token to the first token taken
        # from the inputs
        self.no_space()
        self.current_token = self.get_next_token()
        result = Token(INTEGER, 0)
        left = None
        token_eval = 0
        while (self.current_token.type == INTEGER):
            token_eval = (token_eval * 10) + self.current_token.value
            self.eat(INTEGER)

        # current token will be an int
        left = Token(INTEGER, token_eval)

        while(self.current_token.type != EOF):
            # we expect the current token to be either a '+' || '-' token
            op = self.current_token
            if (self.current_token.value == '+'):
                self.eat(PLUS)
            elif(self.current_token.value == '*'):
                self.eat(MUL)
            elif(self.current_token.value == '/'):
                self.eat(DIV)
            else:
                self.eat(MINUS)

                # We expect token to be int as well
            token_eval = 0
            right = None
            while (self.current_token.type == INTEGER):
                token_eval = (token_eval * 10) + self.current_token.value
                self.eat(INTEGER)

            right = Token(INTEGER, token_eval)

            if (op.type == PLUS):
                result.value = left.value + right.value
            elif(op.type == MUL):
                result.value = left.value * right.value
            elif(op.type == DIV):
                result.value = left.value / right.value
            else:
                result.value = left.value - right.value
            left = result

        # after the above call, the self.current token
        # is set to EOF token
        return result.value


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
