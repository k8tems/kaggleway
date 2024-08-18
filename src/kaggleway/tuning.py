from dataclasses import dataclass


@dataclass
class TuningParam(object):
    name: str
    ctx: str
    method_type = ''

    def __init__(self, *args, **kwargs):
        super(TuningParam, self).__init__(*args, **kwargs)

    def parse_ctx(self, ctx):
        raise NotImplementedError()

    def get_suggest_method(self, trial):
        return getattr(trial, f'suggest_{self.method_type}')


@dataclass
class IntCatParam(TuningParam):
    id_ = 'intcat'
    method_type = 'categorical'

    def parse_ctx(self, ctx):
        return

    def suggest(self, trial, *_):
        return self.get_suggest_method(trial)(self.name, [int(c) for c in self.ctx.split('|')])


@dataclass
class FloatParam(TuningParam):
    id_ = 'float'
    method_type = id_

    def suggest(self, trial, *_):
        ctx = self.ctx.split('|')
        return self.get_suggest_method(trial)(self.name, float(ctx[0]), float(ctx[1]))


def get_param_cls(id_):
    for sub_cls in TuningParam.__subclasses__():
        if sub_cls.id_ == id_:
            return sub_cls
    assert ()


def create_param(row):
    name, ctx, type_ = row.split(',')
    return get_param_cls(type_)(name, ctx)


class TuningParamPool(list):
    @classmethod
    def from_txt(cls, txt):
        return [create_param(row) for row in txt.split('\n')]


def compile_tuning_params(params, trial):
    return dict([(p.name, p.suggest(trial)) for p in params])
