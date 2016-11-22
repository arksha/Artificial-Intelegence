import sys

OPERATORS = ['&', '|', '=>', '~']


class KB:
    def __init__(self, sentence=None):
        self.clauses = []
        if sentence:
            self.tell(sentence)

    def tell(self, sentence):
        self.clauses(convert_to_cnf(sentence))

    def ask(self, query):
        resolution(query)


class Clause:

    def __init__(self, operator, arguments=[]):
        self.operator = operator
        self.arguments = map(makeClause, arguments)

    def __hash__(self):
        return hash(self.operator) ^ hash(tuple(self.arguments))

    def __repr__(self):
        if len(self.arguments) == 0:
            return self.operator

        elif self.operator not in OPERATORS:
            arguments = str(self.arguments[0])
            for argument in self.arguments[1:]:
                arguments = arguments + ',' + str(argument)
            return self.operator + '(' + arguments + ')'

        elif self.operator == '~':
            if self.arguments[0].operator not in OPERATORS:
                return '~' + str(self.arguments[0])
            else:
                return '~' + '(' + str(self.arguments[0]) + ')'
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

    def __invert__(self):
        return Clause('~', [self])

    def __and__(self, other):
        return Clause('&', [self, other])

    def __or__(self, other):
        return Clause('|', [self, other])

    def __eq__(self, other):
        return isinstance(other, Clause) and self.operator == other.operator and self.arguments == other.arguments


def isPredicate(expr):
    if expr.op[0] != '~':
        return expr.op not in OPERATORS and expr.op[0].isupper()
    else:
        return expr.op not in OPERATORS and expr.op[1].isupper()


def makeClause(line):

    if isinstance(line, Clause):
        return line

    if '=>' in line:
        pos = line.index('=>')
        leftexp, rightexp = line[:pos], line[pos + 1:]
        clause = Clause('=>', [leftexp, rightexp])
        # print 'clause op, argu', clause.operator, clause.arguments
        return clause
    elif '&' in line:
        pos = line.index('&')
        leftpart,rightpart = line[:pos], line[pos + 1:]
        clause = Clause('&', [leftpart, rightpart])
        # print 'clause op, argu', clause.operator, clause.arguments
        return clause
    elif '|' in line:
        pos = line.index('|')
        leftside, rightside = line[:pos], line[pos + 1:]
        clause = Clause('|', [leftside, rightside])
        # print 'clause op, argu', clause.operator, clause.arguments
        return clause
    elif '~' in line:
        pos = line.index('~')
        arglist = [line[pos + 1:]]
        clause = Clause('~', arglist)
        # print 'clause op, argu', clause.operator, clause.arguments
        return clause
    elif isinstance(line, str):
        return Clause(line)

    if len(line) == 1:
        return makeClause(line[0])

    # for arg in line[1:]:
    #     argumentlist.append(arg[0])

    # argumentlist = [line[1:][0]]
    transedClause = Clause(line[0], line[1:][0])
    # print ">>>>line [1]::::", line[1:][0]
    # print "op and argu",transedClause.operator, transedClause.arguments
    return transedClause


def parse(s):

    s = '(' + s + ')'
    s = s.replace('(', ' ( ')
    s = s.replace(')', ' ) ')
    s = s.replace(',', ' ')
    s = s.replace('|', ' | ')
    s = s.replace('&', ' & ')
    s = s.replace('~', ' ~ ')
    s = s.replace('=>', ' => ')

    tokens = s.split()
    # tokens = handledupparentheses(tokens)
    return getToken(tokens)


def handledupparentheses(string):
    if string[0] == '(' and string[1] == '(' and string[-2] == ')' and string[-1] == ')':
        string = string[1:-1]
        return handledupparentheses(string)
    return string


def getToken(tokenlist):

    top = tokenlist.pop(0)
    if top == '(':
        newSentences = []
        while tokenlist[0] != ')':
            recheck = getToken(tokenlist)
            newSentences.append(recheck)
        tokenlist.pop(0)
        return newSentences
    else:
        return top


def convert_to_cnf(rule):
    rule = remove_implication(rule)
    rule = move_neg_in(rule)
    rule = distribute_and_over_or(rule)
    # print "rule", rule
    return rule


def remove_implication(rule):
    if not rule.arguments or is_symbol(rule.operator):
        return rule
    rule_argument = map(remove_implication, rule.arguments)
    first, second = rule_argument[0], rule_argument[-1]
    if rule.operator == '=>':
        return second | ~first
    else:
        return Clause(rule.operator, rule_argument)


def is_symbol(string):
    return isinstance(string, str) and string[:1].isalpha()


def move_neg_in(rule):
    if is_symbol(rule.operator) or not rule.arguments:
        return rule
    elif rule.operator == '~':
        NOT = lambda l: move_neg_in(~l)
        a = rule.arguments[0]
        # print 'oper is !!!'
        # print a.operator
        if a.operator == '~':
            # print 'oper is ~'
            return move_neg_in(a.arguments[0])
        if a.operator == '&':
            # print 'oper is  & '
            return associate('|', map(NOT, a.arguments))
        if a.operator == '|':
            # print 'oper is | '
            return associate('&', map(NOT, a.arguments))
        return rule

    else:
        return Clause(rule.operator, map(move_neg_in, rule.arguments))

op_table = {'&': True, '|': False}


def conjuncts(sentence):
    return dissociate('&', [sentence])


def disjuncts(sentence):
    return dissociate('|', [sentence])


def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return op_table[op]
    elif len(args) == 1:
        return args[0]
    else:
        return Clause(op, args)


def dissociate(op, args):
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.operator == op:
                collect(arg.arguments)
            else:
                result.append(arg)
    collect(args)
    return result


def find_if(predicate, seq):
    """find if there exist an element in seq and return it"""
    for x in seq:
        if predicate(x): return x
    return None


def distribute_and_over_or(rule):
    if rule.operator == '|':
        rule = associate('|', rule.arguments)
        if len(rule.arguments) == 0:
            return False
        if len(rule.arguments) == 1:
            return distribute_and_over_or(rule.arguments[0])
        conjunct = find_if((lambda d: d.operator == '&'), rule.arguments)
        if not conjunct:
            return rule
        others = [a for a in rule.arguments if a is not conjunct]
        rest = associate('|', others)
        return associate('&', [distribute_and_over_or(c | rest) for c in conjunct.arguments])
    elif rule.operator == '&':
        return associate('&', map(distribute_and_over_or, rule.arguments))
    else:
        return rule


def resolution(KB,query):
    clauses = KB.clause + conjuncts(convert_to_cnf(~query))
    new = set()
    while True:
        n = len(clauses)
        print 'n', n
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        print 'pairs', len(pairs)
        pairs_count = 0

        for (ci, cj) in pairs:
            pairs_count += 1
            if pairs_count % 100000 == 0:
                print 'pairs count', pairs_count
            resolvents = resolve(ci, cj)
            if False in resolvents:
                return True
            new = new.union(set(resolvents))
        if new.issubset(set(clauses)):
            return False
        print 'new :', len(new)
        for c in new:
            if c not in clauses:
                clauses.append(c)


def resolve(ci, cj):
    clauses = []
    for di in disjuncts(ci):
        for dj in disjuncts(cj):
            if di == ~dj or ~di == dj:
                dnew = unique(removeall(di, disjuncts(ci)) + removeall(dj, disjuncts(cj)))
                clauses.append(associate('|', dnew))
    return clauses


def unique(sequence):
    #remove dup
    return list(set(sequence))


def removeall(ele, sequence):
    #return copy of list removed all appeared
    if isinstance(sequence, str):
        return sequence.replace(ele, '')
    else:
        return [x for x in sequence if x != ele]

'''read input file'''


inputfile = open('input.txt', 'r')

#get intput queries
queriesnum = eval(inputfile.readline().strip())
querylist = list()
for i in range(queriesnum):
    queryline = inputfile.readline().rstrip('\n')
    queryline = queryline.replace(" ", "")
    # print queryline
    querylist.append(queryline)

# get input sentences
sentencenum = eval(inputfile.readline().strip())
sentencelist = list()
for i in range(sentencenum):
    sentenceline = inputfile.readline().rstrip('\n')
    sentenceline = sentenceline.replace(' ', '')
    sentencelist.append(sentenceline)

inputfile.close()
queries = []
rules = []
for q in querylist:
    query = makeClause(parse(q))
    queries.append(query)
    # print query
    # print '>>>>>>querys clause op, argu', query.operator, query.arguments
    # print parse(q)
for sentence in sentencelist:
    # print parse(sentence)
    rule = makeClause(parse(sentence))
    # print '>>>rule op, argu',rule, rule.operator, rule.arguments
    # rules.append(convert_to_cnf(rule))
    KB.tell(rule)
# print ">>>", rules


for query in queries:
    KB.ask(query)
    
outputFile = open('output.txt','w')
outputFile.close()
