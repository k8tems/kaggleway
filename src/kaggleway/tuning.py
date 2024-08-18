from dataclasses import dataclass


@dataclass
class TuningParam(object):
    """
    csv形式で定義されたチューニング対象パラメータのリストを格納するクラス
    ctorのパラメータ：
      - `name`: trial.suggest_param(name, *args)の`name`に渡すパラメータ名
      - `ctx`: csvから抽出した生のパラメータ範囲、parseするのは親クラスの責任
    スーパークラスで定義するもの：
      - `id_`: 該当パラメータがどの親クラスのパラメータに相当するかを示す識別子(e.g. intcat)
      - `method_type`: optunaのsuggest_の後に付く識別子。合成した文字列を直接getattrにぶち込む
    """
    name: str
    ctx: str
    id_ = ''
    method_type = ''

    def __init__(self, *args, **kwargs):
        super(TuningParam, self).__init__(*args, **kwargs)

    def parse_ctx(self, ctx):
        raise NotImplementedError()

    def get_suggest_method(self, trial):
        return getattr(trial, f'suggest_{self.method_type}')

    def suggest_(self, trial, *args):
        return self.get_suggest_method(trial)(self.name, *args)


@dataclass
class IntCatParam(TuningParam):
    id_ = 'intcat'
    method_type = 'categorical'

    def parse_ctx(self, ctx):
        return

    def suggest(self, trial):
        # ctxのパースだけポリモーフィックにしたい所だが、パラメータの数が種類によって違うのでやり辛い
        # 一旦は親クラスのsuggest_メソッドを呼び出す方式で妥協
        # シグネチャが違うので(同名だとIDEで警告が出る)アンダースコアを付けて差別化する
        return super(IntCatParam, self).suggest_(trial, [int(c) for c in self.ctx.split('|')])


@dataclass
class FloatParam(TuningParam):
    id_ = 'float'
    method_type = id_

    def suggest(self, trial):
        ctx = self.ctx.split('|')
        return super(FloatParam, self).suggest_(trial,  float(ctx[0]), float(ctx[1]))


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
