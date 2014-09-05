# ===========================================================================
# Boundary conditions for LB models
# ---------------------------------------------------------------------------
# Keijo Mattila & Tuomas Puurtinen, SimPhoNy, JYU, August 2014.
# ===========================================================================
# Import modules
# ===========================================================================
import numpy as np
import abc_lattice
import lb
# ---------------------------------------------------------------------------
def d2q9_inlet_bc(lat,d2q9,fread,fwrite,ref_den,f_ind):

    fval = np.zeros(d2q9.Q, dtype=np.float)
    fneq = np.zeros(d2q9.Q, dtype=np.float)
    feq  = np.zeros(d2q9.Q, dtype=np.float)

    fncount = lat.get_node_count('Fluid')
    incount = lat.get_node_count('Inlet')

    for in_n in range(incount):

        n = int(lat.get_data_container('Inlet').get_values('FluidNodeIndex')[in_n])
        n_nghbr = int(lat.get_data_container('Inlet').get_values('InwardNeighbour')[in_n])

        fval = fread[f_ind(fncount,d2q9.Q,n_nghbr,np.arange(d2q9.Q))]

        den_nghbr = lat.get_data_container('Fluid').get_values('Density')[n_nghbr]
        ux_nghbr = lat.get_data_container('Fluid').get_values('Velocity')[n_nghbr,lb.X]
        uy_nghbr = lat.get_data_container('Fluid').get_values('Velocity')[n_nghbr,lb.Y]

        lb.feq2_2D(d2q9,den_nghbr,ux_nghbr,uy_nghbr,feq)
        fneq = fval - feq

        lb.feq2_2D(d2q9,ref_den,ux_nghbr,0.0,feq)
        fread[f_ind(fncount,d2q9.Q,n,d2q9.NE)] = feq[d2q9.NE] + fneq[d2q9.NE]
        fread[f_ind(fncount,d2q9.Q,n,d2q9.E)]  = feq[d2q9.E]  + fneq[d2q9.E]
        fread[f_ind(fncount,d2q9.Q,n,d2q9.SE)] = feq[d2q9.SE] + fneq[d2q9.SE]
    #end for

# end function d2q9_inlet_bc
# ---------------------------------------------------------------------------
def d2q9_outlet_bc(lat,d2q9,fread,fwrite,ref_den,f_ind):

    fval = np.zeros(d2q9.Q, dtype=np.float)
    fneq = np.zeros(d2q9.Q, dtype=np.float)
    feq  = np.zeros(d2q9.Q, dtype=np.float)

    fncount = lat.get_node_count('Fluid')
    outncount = lat.get_node_count('Outlet')

    for out_n in range(outncount):

        n = int(lat.get_data_container('Outlet').get_values('FluidNodeIndex')[out_n])
        n_nghbr = int(lat.get_data_container('Outlet').get_values('InwardNeighbour')[out_n])

        fval = fread[f_ind(fncount,d2q9.Q,n_nghbr,np.arange(d2q9.Q))]

        den_nghbr = lat.get_data_container('Fluid').get_values('Density')[n_nghbr]
        ux_nghbr = lat.get_data_container('Fluid').get_values('Velocity')[n_nghbr,lb.X]
        uy_nghbr = lat.get_data_container('Fluid').get_values('Velocity')[n_nghbr,lb.Y]

        lb.feq2_2D(d2q9,den_nghbr,ux_nghbr,uy_nghbr,feq)
        fneq = fval - feq

        lb.feq2_2D(d2q9,ref_den,ux_nghbr,0.0,feq)
        fread[f_ind(fncount,d2q9.Q,n,d2q9.NW)] = feq[d2q9.NW] + fneq[d2q9.NW]
        fread[f_ind(fncount,d2q9.Q,n,d2q9.W)]  = feq[d2q9.W]  + fneq[d2q9.W]
        fread[f_ind(fncount,d2q9.Q,n,d2q9.SW)] = feq[d2q9.SW] + fneq[d2q9.SW]
    #end for

# end function d2q9_outlet_bc
# ---------------------------------------------------------------------------
