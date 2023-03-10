import numpy as np
import pendulumParam as P
import loopShapingInner as L_in
import loopShapingOuter as L_out
from digitalFilter import digitalFilter

class ctrlLoopshape:
    # state feedback control using dirty derivatives to estimate zdot and thetadot
    def __init__(self, method="state_space"):
        self.method = method
        if method == "state_space":
            self.xout_C = np.zeros((L_out.C_ss.A.shape[0], 1))
            self.xout_F = np.zeros((L_out.F_ss.A.shape[0], 1))
            self.xin_C  = np.zeros((L_in.C_ss.A.shape[0], 1))
            self.Aout_F = L_out.F_ss.A
            self.Bout_F = L_out.F_ss.B
            self.Cout_F = L_out.F_ss.C
            self.Dout_F = L_out.F_ss.D
            self.Aout_C = L_out.C_ss.A
            self.Bout_C = L_out.C_ss.B
            self.Cout_C = L_out.C_ss.C
            self.Dout_C = L_out.C_ss.D
            self.Ain_C = L_in.C_ss.A
            self.Bin_C = L_in.C_ss.B
            self.Cin_C = L_in.C_ss.C
            self.Din_C = L_in.C_ss.D
            self.N = 10  #number of Euler integration steps for each sample
        elif method == "digital_filter":
            self.control_out = digitalFilter(L_out.C.num, L_out.C.den, P.Ts)
            self.prefilter_out = digitalFilter(L_out.F.num, L_out.F.den, P.Ts)
            self.control_in = digitalFilter(L_in.C.num, L_in.C.den, P.Ts)

    def update(self, y_r, y):
        # y_r is the referenced input
        # y is the current outputs
        z_r = y_r
        z = y[0][0]
        theta = y[1][0]
        if self.method == "state_space":
            # solve differential equation defining prefilter F
            self.updatePrefilterState(z_r)
            z_r_filtered = self.Cout_F @ self.xout_F + self.Dout_F * z_r
            # error signal for outer loop
            error_out = z_r_filtered[0][0] - z
            # Outer loop control C_out
            self.updateControlOutState(error_out)
            theta_r = self.Cout_C @ self.xout_C + self.Dout_C * error_out
            # error signal for inner loop
            error_in = theta_r[0][0] - theta
            # Inner loop control C_in
            self.updateControlInState(error_in)
            F_unsat = self.Cin_C @ self.xin_C + self.Din_C * error_in
            F = saturate(F_unsat[0][0], P.F_max)
        elif self.method == "digital_filter":
            # prefilter for outer loop
            z_r_filtered = self.prefilter_out.update(z_r)
            # error signal for outer loop
            error_out = z_r_filtered - z
            # outer loop control
            theta_r = self.control_out.update(error_out)
            #error signal for inner loop
            error_in = theta_r - theta
            # inner loop control
            F_unsat = self.control_in.update(error_in)
            F = saturate(F_unsat, P.F_max)
        return F

    def updatePrefilterState(self, z_r):
        for i in range(0, self.N):
            self.xout_F = self.xout_F + (P.Ts/self.N)*(
                self.Aout_F @ self.xout_F + self.Bout_F * z_r
            )

    def updateControlOutState(self, error_out):
        for i in range(0, self.N):
            self.xout_C = self.xout_C + (P.Ts/self.N)*(
                self.Aout_C @ self.xout_C + self.Bout_C * error_out
            )

    def updateControlInState(self, error_in):
        for i in range(0, self.N):
            self.xin_C = self.xin_C + (P.Ts/self.N)*(
                self.Ain_C @ self.xin_C + self.Bin_C * error_in
            )


def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u

