errorTolerance = 0.001
dynamics_test_cases = [
# initial state (z, theta, zdot, theta_dot),    input (F),     true state of plant (z, theta, zdot, theta_dot)
    ([[0.], [0.], [0.], [0.]],                  0.0,        [[ 1.20049989e-07], [-1.46999987e-03], [4.80199892e-05], [-2.93999921e-01]]),
    ([[1.], [0.], [0.], [0.]],                  10.0,       [[ 1.00000006e+00], [-3.22258059e-04], [2.43737977e-05], [-6.44516073e-02]]),
    ([[0.], [1.], [0.], [0.]],                  100.0,      [[-4.12339381e-04], [1.00042143e+00], [-8.24715991e-02], [8.42839597e-02]]),
    ([[0.], [0.], [1.], [0.]],                  5.0,        [[ 1.00000597e-02], [-7.23354032e-04], [1.00002413e+00], [-1.44998540e-01]]),
    ([[1.], [0.], [0.], [1.]],                  50.0,       [[1.00004784], [0.00991946], [0.00935258], [0.98387091]]),
    ([[-1.], [-10.], [0.], [1.]],               -10.0,      [[-1.00031876], [-9.98947504], [-0.06397547], [1.10494087]]),
    ([[0.], [5.], [-5.], [-5.]],                -1.0,       [[-0.04954894], [4.94965818], [-4.9116877], [-5.05670704]]),
    ([[1.], [2.], [3.], [4.]],                  -20.,       [[1.03036073], [2.03983429], [3.07279632], [3.96777795]]),
    ([[-1.], [2.], [-3.], [4.]],                -50.,       [[-1.03123862], [2.03953929], [-3.24701186], [3.90697329]]),
    ([[1.], [1.], [1.], [1.]],                  50.,        [[1.00963624], [1.00989089], [0.92710513], [0.97837952]]),
]