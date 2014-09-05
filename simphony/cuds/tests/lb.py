# ===========================================================================
# Specifications and definitions for standard LBM
# ---------------------------------------------------------------------------
# Keijo Mattila & Tuomas Puurtinen, SimPhoNy, JYU, August 2014.
# ===========================================================================
# Import modules
# ===========================================================================
import numpy as np
# ===========================================================================
# Common variables
# ===========================================================================
X = int(0)
Y = int(1)
Z = int(2)

KRD_2D = np.array( ((1.0,0.0),
                    (0.0,1.0)), dtype=np.float)

KRD_3D = np.array( ((1.0,0.0,0.0),
                    (0.0,1.0,0.0),
                    (0.0,0.0,1.0)), dtype=np.float)
# ---------------------------------------------------------------------------
# Hermite polynomial tensor of rank 2 in 2D
# Note: defined with CI (i.e. not with VI)
# ---------------------------------------------------------------------------
def HI2_2D(CI,CT2):
    return np.array( ((CI[X,:]*CI[X,:] - CT2*KRD_2D[X,X],
                       CI[X,:]*CI[Y,:] - CT2*KRD_2D[X,Y]),
                           
                      (CI[Y,:]*CI[X,:] - CT2*KRD_2D[Y,X],
                       CI[Y,:]*CI[Y,:] - CT2*KRD_2D[Y,Y])),
                        
                    dtype=np.float)
# ---------------------------------------------------------------------------
# Hermite polynomial tensor of rank 3 in 2D
# Note: defined with CI (i.e. not with VI) using the recurrence relation
# ---------------------------------------------------------------------------
def HI3_2D(CI,CT2,HI2):
    return np.array(
        (((CI[X,:]*HI2[X,X,:] - CT2*(KRD_2D[X,X]*CI[X,:] + KRD_2D[X,X]*CI[X,:]),
           CI[X,:]*HI2[X,Y,:] - CT2*(KRD_2D[X,X]*CI[Y,:] + KRD_2D[X,Y]*CI[X,:])),
                          
          (CI[X,:]*HI2[Y,X,:] - CT2*(KRD_2D[X,Y]*CI[X,:] + KRD_2D[X,X]*CI[Y,:]),
           CI[X,:]*HI2[Y,Y,:] - CT2*(KRD_2D[X,Y]*CI[Y,:] + KRD_2D[X,Y]*CI[Y,:]))),
                          
         ((CI[Y,:]*HI2[X,X,:] - CT2*(KRD_2D[Y,X]*CI[X,:] + KRD_2D[Y,X]*CI[X,:]),
           CI[Y,:]*HI2[X,Y,:] - CT2*(KRD_2D[Y,X]*CI[Y,:] + KRD_2D[Y,Y]*CI[X,:])),
                       
          (CI[Y,:]*HI2[Y,X,:] - CT2*(KRD_2D[Y,Y]*CI[X,:] + KRD_2D[Y,X]*CI[Y,:]),
           CI[Y,:]*HI2[Y,Y,:] - CT2*(KRD_2D[Y,Y]*CI[Y,:] + KRD_2D[Y,Y]*CI[Y,:])))),
                        
        dtype=np.float)
# ---------------------------------------------------------------------------
# Hermite polynomial tensor of rank 2 in 3D
# Note: defined with CI (i.e. not with VI)
# ---------------------------------------------------------------------------
def HI2_3D(CI,CT2):
    return np.array( ((CI[X,:]*CI[X,:] - CT2*KRD_2D[X,X],
                       CI[X,:]*CI[Y,:] - CT2*KRD_2D[X,Y],
                       CI[X,:]*CI[Z,:] - CT2*KRD_2D[X,Z]),
                           
                      (CI[Y,:]*CI[X,:] - CT2*KRD_2D[Y,X],
                       CI[Y,:]*CI[Y,:] - CT2*KRD_2D[Y,Y],
                       CI[Y,:]*CI[Z,:] - CT2*KRD_2D[Y,Z]),
                           
                      (CI[Z,:]*CI[X,:] - CT2*KRD_2D[Z,X],
                       CI[Z,:]*CI[Y,:] - CT2*KRD_2D[Z,Y],
                       CI[Z,:]*CI[Z,:] - CT2*KRD_2D[Z,Z])),
                           
                    dtype=np.float)
# ---------------------------------------------------------------------------
# Hermite polynomial tensor of rank 3 in 3D
# Note: defined with CI (i.e. not with VI) using the recurrence relation
# ---------------------------------------------------------------------------
def HI3_3D(CI,CT2,HI2):
    return np.array(
        (((CI[X,:]*HI2[X,X,:] - CT2*(KRD_2D[X,X]*CI[X,:] + KRD_2D[X,X]*CI[X,:]),
           CI[X,:]*HI2[X,Y,:] - CT2*(KRD_2D[X,X]*CI[Y,:] + KRD_2D[X,Y]*CI[X,:]),
           CI[X,:]*HI2[X,Z,:] - CT2*(KRD_2D[X,X]*CI[Z,:] + KRD_2D[X,Z]*CI[X,:])),
                          
          (CI[X,:]*HI2[Y,X,:] - CT2*(KRD_2D[X,Y]*CI[X,:] + KRD_2D[X,X]*CI[Y,:]),
           CI[X,:]*HI2[Y,Y,:] - CT2*(KRD_2D[X,Y]*CI[Y,:] + KRD_2D[X,Y]*CI[Y,:]),
           CI[X,:]*HI2[Y,Z,:] - CT2*(KRD_2D[X,Y]*CI[Z,:] + KRD_2D[X,Z]*CI[Y,:]))
           
          (CI[X,:]*HI2[Z,X,:] - CT2*(KRD_2D[X,Z]*CI[X,:] + KRD_2D[X,X]*CI[Z,:]),
           CI[X,:]*HI2[Z,Y,:] - CT2*(KRD_2D[X,Z]*CI[Y,:] + KRD_2D[X,Y]*CI[Z,:]),
           CI[X,:]*HI2[Z,Z,:] - CT2*(KRD_2D[X,Z]*CI[Z,:] + KRD_2D[X,Z]*CI[Z,:]))),
                          
         ((CI[Y,:]*HI2[X,X,:] - CT2*(KRD_2D[Y,X]*CI[X,:] + KRD_2D[Y,X]*CI[X,:]),
           CI[Y,:]*HI2[X,Y,:] - CT2*(KRD_2D[Y,X]*CI[Y,:] + KRD_2D[Y,Y]*CI[X,:]),
           CI[Y,:]*HI2[X,Z,:] - CT2*(KRD_2D[Y,X]*CI[Z,:] + KRD_2D[Y,Z]*CI[X,:])),
                          
          (CI[Y,:]*HI2[Y,X,:] - CT2*(KRD_2D[Y,Y]*CI[X,:] + KRD_2D[Y,X]*CI[Y,:]),
           CI[Y,:]*HI2[Y,Y,:] - CT2*(KRD_2D[Y,Y]*CI[Y,:] + KRD_2D[Y,Y]*CI[Y,:]),
           CI[Y,:]*HI2[Y,Z,:] - CT2*(KRD_2D[Y,Y]*CI[Z,:] + KRD_2D[Y,Z]*CI[Y,:]))
           
          (CI[Y,:]*HI2[Z,X,:] - CT2*(KRD_2D[Y,Z]*CI[X,:] + KRD_2D[Y,X]*CI[Z,:]),
           CI[Y,:]*HI2[Z,Y,:] - CT2*(KRD_2D[Y,Z]*CI[Y,:] + KRD_2D[Y,Y]*CI[Z,:]),
           CI[Y,:]*HI2[Z,Z,:] - CT2*(KRD_2D[Y,Z]*CI[Z,:] + KRD_2D[Y,Z]*CI[Z,:])))
           
         ((CI[Z,:]*HI2[X,X,:] - CT2*(KRD_2D[Z,X]*CI[X,:] + KRD_2D[Z,X]*CI[X,:]),
           CI[Z,:]*HI2[X,Y,:] - CT2*(KRD_2D[Z,X]*CI[Y,:] + KRD_2D[Z,Y]*CI[X,:]),
           CI[Z,:]*HI2[X,Z,:] - CT2*(KRD_2D[Z,X]*CI[Z,:] + KRD_2D[Z,Z]*CI[X,:])),
                          
          (CI[Z,:]*HI2[Y,X,:] - CT2*(KRD_2D[Z,Y]*CI[X,:] + KRD_2D[Z,X]*CI[Y,:]),
           CI[Z,:]*HI2[Y,Y,:] - CT2*(KRD_2D[Z,Y]*CI[Y,:] + KRD_2D[Z,Y]*CI[Y,:]),
           CI[Z,:]*HI2[Y,Z,:] - CT2*(KRD_2D[Z,Y]*CI[Z,:] + KRD_2D[Z,Z]*CI[Y,:]))
           
          (CI[Z,:]*HI2[Z,X,:] - CT2*(KRD_2D[Z,Z]*CI[X,:] + KRD_2D[Z,X]*CI[Z,:]),
           CI[Z,:]*HI2[Z,Y,:] - CT2*(KRD_2D[Z,Z]*CI[Y,:] + KRD_2D[Z,Y]*CI[Z,:]),
           CI[Z,:]*HI2[Z,Z,:] - CT2*(KRD_2D[Z,Z]*CI[Z,:] + KRD_2D[Z,Z]*CI[Z,:])))),
                        
        dtype=np.float)
# ===========================================================================
# D2Q9 (second-order velocity set, isothermal equilibrium function)
# ===========================================================================
# NW  N  NE
#   \ | /     
# W-- C --E    y ^
#   / | \        |
# SW  S  SE     ---> x
# ===========================================================================
class D2Q9:
    SW = int(0)
    S  = int(1)
    SE = int(2)
    W  = int(3)
    C  = int(4)
    E  = int(5)
    NW = int(6)
    N  = int(7)
    NE = int(8)
    Q  = int(9)

    W0 = float(4.0/9.0)
    W1 = float(1.0/9.0)
    W2 = float(1.0/36.0)
    
    AS2 = float(3.0)
    CT2 = float(1.0/AS2)
    INV_CT2 = float(1.0/CT2)
    
    WI = np.array( (W2,W1,W2, W1,W0,W1, W2,W1,W2), dtype=np.float)
    CI = np.array( ((-1,0,1, -1,0,1, -1,0,1),
                    (-1,-1,-1, 0,0,0, 1,1,1)), dtype=np.int)
    RDIR = np.array( (NE,N,NW,E,C,W,SE,S,SW), dtype=np.int)
    
    KI0 = WI
    KI1 = np.array(WI*INV_CT2*CI, dtype = np.float)
    KI2 = np.array(WI*(1.0/2.0)*INV_CT2*INV_CT2*HI2_2D(CI,CT2), dtype = np.float)
    # -----------------------------------------------------------------------
    # Computation of density from the given distributions 
    # -----------------------------------------------------------------------
    def density(self,fi):
        den = (fi[self.SW] + fi[self.S] + fi[self.SE]
            + fi[self.W]  + fi[self.C] + fi[self.E]
            + fi[self.NW] + fi[self.N] + fi[self.NE])

        return den
    # -----------------------------------------------------------------------
    # Computation of momentum in x-dir.
    # -----------------------------------------------------------------------
    def momentum_x(self,fi):
        jx = (fi[self.NE] + fi[self.E] + fi[self.SE]
            - fi[self.NW] - fi[self.W] - fi[self.SW])

        return jx
    # -----------------------------------------------------------------------
    # Computation of momentum in y-dir.
    # -----------------------------------------------------------------------
    def momentum_y(self,fi):
        jy = (fi[self.NW] + fi[self.N] + fi[self.NE]
            - fi[self.SW] - fi[self.S] - fi[self.SE])

        return jy
    # -----------------------------------------------------------------------
    # Computation of density and velocity from the given distributions 
    # -----------------------------------------------------------------------
    def den_vels(self,fi):
        den = (fi[self.SW] + fi[self.S] + fi[self.SE]
            + fi[self.W]  + fi[self.C] + fi[self.E]
            + fi[self.NW] + fi[self.N] + fi[self.NE])

        inv_den = 1.0/den

        jx = (fi[self.NE] + fi[self.E] + fi[self.SE]
            - fi[self.NW] - fi[self.W] - fi[self.SW])

        jy = (fi[self.NW] + fi[self.N] + fi[self.NE]
            - fi[self.SW] - fi[self.S] - fi[self.SE])
           
        return (den,inv_den*jx,inv_den*jy)
        
# end class D2Q9
# ===========================================================================
# Common functions
# ===========================================================================
# Isothermal equilibrium function (2nd-order expansion)
# -----------------------------------------------------------------------
def feq2_2D(dvs,den,ux,uy,feq_ret):
    ux2  = ux*ux
    uxuy = ux*uy
    uy2  = uy*uy

    feq_ret[:] = den*(dvs.KI0[:] + dvs.KI1[X,:]*ux + dvs.KI1[Y,:]*uy
                 + dvs.KI2[X,X,:]*ux2 + 2.0*dvs.KI2[X,Y,:]*uxuy
                 + dvs.KI2[Y,Y,:]*uy2)
# -----------------------------------------------------------------------
# Forcing term (due to an external acceleration, 1st-order expansion)
# -----------------------------------------------------------------------
def facc1_2D(dvs,den,ax,ay,facc_ret):
    facc_ret[:] = den*(dvs.KI1[X]*ax + dvs.KI1[Y]*ay)
# -----------------------------------------------------------------------
# Single-relaxation-time procedure (or collision operator)
# -----------------------------------------------------------------------
def bgk_relax(dvs,inv_tau,fi_ret,feq):
    fi_ret[:] = (1.0 - inv_tau)*fi_ret + inv_tau*feq
# -----------------------------------------------------------------------
# Two-relaxation-time procedure (or collision operator)
# -----------------------------------------------------------------------
def trt_relax(dvs,inv_tau_e,inv_tau_o,fi_ret,feq):
    relax_we = 0.5*(inv_tau_e + inv_tau_o)
    relax_wo = 0.5*(inv_tau_e - inv_tau_o)
    fi_neq = np.array(fi_ret - feq, dtype=np.float)
                         
    fi_ret[:] = fi_ret - relax_we*fi_neq - relax_wo*fi_neq[dvs.RDIR]
# ===========================================================================