import unittest
from src.kaggleway.tuning import TuningParamPool


class TestTuningParamsIntegration(unittest.TestCase):
    def test_tuning_params(self):
        fixture = """learning_rate,1e-7|2e-1,float
ds_size,1000|10000|100000|300000,int"""
        params = TuningParamPool.from_txt(fixture)
        trial = MockTrial()
        for i in range(100):
            compiled_params = compile_tuning_params(params, trial)
            self.assertLessEqual(compiled_params['learning_rate'], 2e-1)
            self.assertGreaterEqual(compiled_params['learning_rate'], 1e-7)
            self.assertIn(compiled_params['ds_size'], [1000, 10000, 100000, 300000])


if __name__ == '__main__':
    unittest.main()
