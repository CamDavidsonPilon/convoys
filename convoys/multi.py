import numpy
from convoys import regression
from convoys import single


class MultiModel:
    pass  # TODO


class RegressionToMulti(MultiModel):
    def __init__(self, *args, **kwargs):
        self.base_model = self.base_model_cls(*args, **kwargs)

    def fit(self, G, B, T):
        self._n_groups = max(G) + 1
        X = numpy.zeros((len(G), self._n_groups))
        for i, group in enumerate(G):
            X[i,group] = 1
        self.base_model.fit(X, B, T)

    def _get_x(self, group):
        x = numpy.zeros(self._n_groups)
        x[group] = 1
        return x

    def predict(self, group, t, *args, **kwargs):
        return self.base_model.predict(self._get_x(group), t, *args, **kwargs)


class SingleToMulti(MultiModel):
    def __init__(self, *args, **kwargs):
        self.base_model_init = lambda: self.base_model_cls(*args, **kwargs)

    def fit(self, G, B, T):
        group2bt = {}
        for g, b, t in zip(G, B, T):
            group2bt.setdefault(g, []).append((b, t))
        self._group2model = {}
        for g, BT in group2bt.items():
            self._group2model[g] = self.base_model_init()
            self._group2model[g].fit([b for b, t in BT], [t for b, t in BT])

    def predict(self, group, t, *args, **kwargs):
        return self._group2model[group].predict(t, *args, **kwargs)


class Exponential(RegressionToMulti):
    base_model_cls = regression.Exponential


class Weibull(RegressionToMulti):
    base_model_cls = regression.Weibull


class Gamma(RegressionToMulti):
    base_model_cls = regression.Gamma


class KaplanMeier(SingleToMulti):
    base_model_cls = single.KaplanMeier


class Nonparametric(SingleToMulti):
    base_model_cls = single.Nonparametric
