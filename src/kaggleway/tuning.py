from dataclasses import dataclass


@dataclass
class TuningParam(object):
    """
    csv形式で定義されたチューニング対象パラメータのリストを格納するクラス
    ctorのパラメータ：
      - `name`: trial.suggest_param(name, *args)の`name`に渡すパラメータ名
      - `ctx`: csvから抽出した生のパラメータ範囲または候補のリスト、親クラスによって使われ方が違う
    スーパークラスで定義するもの：
      - `id_`: 該当パラメータがどの親クラスのパラメータに相当するかを示す識別子(e.g. intcat)
      - `method_type`: optunaのsuggest_の後に付く識別子。合成した文字列を直接getattrにぶち込む
    """
    name: str
    ctx: []
    id_ = ''
    method_type = ''

    def __init__(self, *args, **kwargs):
        super(TuningParam, self).__init__(*args, **kwargs)

    def get_suggest_method(self, trial):
        return getattr(trial, f'suggest_{self.method_type}')

    def suggest_(self, trial, *args):
        return self.get_suggest_method(trial)(self.name, *args)


@dataclass
class IntCatParam(TuningParam):
    id_ = 'intcat'
    method_type = 'categorical'

    def suggest(self, trial):
        # ctxのパースだけポリモーフィックにしたい所だが、パラメータの数が種類によって違うのでやり辛い
        # 一旦は親クラスのsuggest_メソッドを呼び出す方式で妥協
        # シグネチャが違うので(同名だとIDEで警告が出る)アンダースコアを付けて差別化する
        return super(IntCatParam, self).suggest_(trial, [c for c in self.ctx])


@dataclass
class FloatParam(TuningParam):
    id_ = 'float'
    method_type = id_

    def suggest(self, trial):
        return super(FloatParam, self).suggest_(trial,  self.ctx[0], self.ctx[1])


@dataclass
class IntParam(TuningParam):
    id_ = 'int'
    method_type = id_

    def suggest(self, trial):
        return super(IntParam, self).suggest_(trial,  self.ctx[0], self.ctx[1])


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
    def from_dict(cls, params):
        """yamlファイルで定義されたチューニング対象のパラメータを保存する
        入力の例：
        fixture = [
            {'name': 'learning_rate', 'range': [1e-7, 2e-1], 'type': 'float'},
            {'name': 'ds_size', 'range': [1000, 10000, 100000, 300000], 'type': 'intcat'}]
        """
        return [get_param_cls(p['type'])(p['name'], p['range']) for p in params]


def compile_tuning_params(params, trial):
    """指定されたoptunaのtrialを使ってチューニングしたいパラメータをランダムで生成する"""
    return dict([(p.name, p.suggest(trial)) for p in params])
