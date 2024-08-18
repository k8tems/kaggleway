def compile_tuning_params(params, trial):
    return dict([(p.name, p.suggest(trial)) for p in params])
