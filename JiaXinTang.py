# coding=utf-8
import operator as op

"""我好想做嘉然小姐的狗啊"""


def reader(content):
    return content.replace('嘉然我真的好喜欢你啊', ' 嘉然我真的好喜欢你啊 ').replace('我的嘉然', ' 我的嘉然 ').split()


def builder(data):
    if len(data) == 0:
        print('<Error> 你再想想')
        return
    word = data.pop(0)
    if word == '嘉然我真的好喜欢你啊':
        exp = []
        while data[0] != '我的嘉然':
            exp.append(builder(data))
        data.pop(0)
        return exp
    elif word == '我的嘉然':
        print('<Error> 你再想想')
        return
    else:
        return atom(word)


def atom(data):
    try:
        return int(data)
    except ValueError:
        try:
            return float(data)
        except ValueError:
            _str = str(data)
            if _str == 'True':
                return True
            elif _str == 'False':
                return False
            return _str


def initial_env():
    env = Env()
    env['圣嘉然说'] = lambda *x: x[-1]
    env['加'] = op.add
    env['减'] = op.sub
    env['乘'] = op.mul
    env['除'] = op.truediv
    env['大于'] = op.gt
    env['小于'] = op.lt
    env['大于等于'] = op.ge
    env['小于等于'] = op.le
    env['等于'] = op.eq
    env['等于？'] = op.is_
    env['鼠鼠说'] = print
    env['夹心糖'] = lambda *x: list(x)
    env['首先'] = lambda x: x[0]
    env['其余'] = lambda x: x[1:]
    env['连接'] = lambda x, y: [x] + y
    return env


class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        super().__init__()
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var: object) -> object:
        if var in self:
            return self
        elif not self.outer is None:
            return self.outer.find(var)
        else:
            print('<Error> 你再想想')
            return self


class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return translator(self.body, Env(self.parms, args, self.env))


environment = initial_env()


def translator(x, env=environment):
    if isinstance(x, list):
        if len(x) == 0:
            print('<Error> 你再想想')
            return

    if isinstance(x, str):
        return env.find(x)[x]

    elif not isinstance(x, list):
        return x
    elif x[0] == '曰':
        _, *args = x
        return args[0]
    elif x[0] == '如果':
        (_, test, conseq, alt) = x
        exp = (conseq if translator(test, env) else alt)
        return translator(exp, env)
    elif x[0] == '为了你我要':
        (_, symbol, exp) = x
        env[symbol] = translator(exp, env)
    elif x[0] == '然然说':
        (_, symbol, exp) = x
        env[symbol] = translator(exp, env)
    elif x[0] == '溜':
        (_, parms, body) = x
        return Procedure(parms, body, env)
    elif x[0] == '设定':
        (_, symbol, exp) = x
        env.find(symbol)[symbol] = translator(exp, env)
    else:
        proc = translator(x[0], env)
        args = [translator(arg, env) for arg in x[1:]]
        return proc(*args)


def JiaXinTang_to_str(exp):
    if isinstance(exp, list):
        return '嘉然我真的好喜欢你啊 ' + ' '.join(map(JiaXinTang_to_str, exp)) + ' 我的嘉然'
    else:
        return str(exp)


def loop(prompt='JiaXinTang> '):
    while True:
        val = translator(builder(reader(input(prompt))))
        if val is not None:
            print(JiaXinTang_to_str(val))


if __name__ == '__main__':
    loop()
