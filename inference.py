import sys

OPERATORS = ['&', '|', '=>', '~']


class Clause:

    def __init__(self, operator, arguments=[]):
        self.operator = operator
        self.arguments = arguments

    def __hash__(self):
        return hash(self.operator) ^ hash(tuple(self.arguments))

    def __repr__(self):
        if len(self.arguments) == 0:
            return self.operator

        elif self.operator not in OPERATORS:
            arguments = str(self.arguments[0])
            for argument in arguments[1:]:
                arguments = arguments + ',' + str(argument)
            return self.operator + '(' + arguments + ')'

        elif self.operator == '~':
            if self.arguments[0].operator not in OPERATORS:
                return '~' + str(self.arguments[0])
            else:
                return '~ ' + '(' + str(self.arguments[0]) + ')'
        else:
            if self.arguments[0].operator in OPERATORS:
                stringrepr = '(' + str(self.arguments[0]) + ')'
            else:
                stringrepr = str(self.arguments[0])
            stringrepr += ' ' + self.operator + ' '

            if self.arguments[1].operator in OPERATORS:
                stringrepr += '(' + str(self.arguments[1]) + ')'
            else:
                stringrepr += str(self.arguments[1])
            return stringrepr


def convert_cnf(clauseslist):

    return clauseslist


'''read input file'''

inputfile = open('input.txt', 'r')

#get intput queries
queriesnum = eval(inputfile.readline().strip())
querylist = list()
for i in range(queriesnum):
    queryline = inputfile.readline().rstrip('\n')
    queryline = queryline.replace(" ", "")
    print queryline
    querylist.append(queryline)

print querylist

#get input sentences
sentencenum = eval(inputfile.readline().strip())
sentencelist = list()
for i in range(sentencenum):
    sentenceline = inputfile.readline().rstrip('\n')
    sentenceline = sentenceline.replace(' ', '')
    sentencelist.append(sentenceline)

print sentencelist


inputfile.close()

clauselist = []
clauselist = convert_cnf(sentencelist)

