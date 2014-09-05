# ===========================================================================
# Test program for lattice data structures
# ---------------------------------------------------------------------------
# Keijo Mattila & Tuomas Puurtinen, SimPhoNy, JYU, August 2014.
# ===========================================================================
# Import modules
# ===========================================================================
import time
import numpy as np
import abc_lattice
import lb
# ===========================================================================
# Constants and index functions
# ===========================================================================
DOMAIN_NODE = np.uint8(0)
INLET_NODE  = np.uint8(1)
OUTLET_NODE = np.uint8(2)
# ===========================================================================
# FUNCTIONS
# ===========================================================================
def preprocess(dvs, rows, cols, geom_fname, f_ind):

    geom = np.zeros((rows,cols),dtype=np.uint8)
    geom = np.fromfile(geom_fname, dtype=np.uint8).reshape((rows,cols))

    # Neumann bc at the inlet/outlet (x-dir.), clone geometry
    geom[:,0] = geom[:,1]
    geom[:,-1] = geom[:,-2]

    # Enumerate fluid nodes
    fnode_count = np.count_nonzero(geom)
    enum_fnodes = np.ones((rows,cols),dtype=np.int64)*-1
    np.place(enum_fnodes, geom > 0, np.arange(fnode_count,dtype=np.int64))

    # Store coordinates and labels for the fluid nodes
    fnode_coords = np.transpose(geom.nonzero())
    fnode_labels = np.ones(fnode_count, dtype=np.uint8)*DOMAIN_NODE

    # Store streaming information for the fluid nodes
    # Note bounceback and periodic bc in the y-direction
    stream_arr = np.zeros(dvs.Q*fnode_count, dtype=np.int64)
    aux_arr = np.zeros(dvs.Q, dtype=np.int64)

    for n in range(fnode_count):
        i = fnode_coords[n,1]
        j = fnode_coords[n,0]

        i_n_arr = i + dvs.CI[lb.X,dvs.RDIR]
        # i_n_arr = (i + dvs.CI[lb.X,dvs.RDIR] + cols)%cols # periodic bc
        j_n_arr = (j + dvs.CI[lb.Y,dvs.RDIR] + rows)%rows # periodic bc

        for q in range(dvs.Q):
            if i_n_arr[q] >= 0 and i_n_arr[q] < cols:
                aux_arr[q] = enum_fnodes[j_n_arr[q], i_n_arr[q]]
            else:
                aux_arr[q] = -1
            # end else if
        # end for

        # aux_arr = enum_fnodes[j_n_arr, i_n_arr]
        # aux_arr = np.where(i_n_arr >= 0 and i_n_arr < cols, enum_fnodes[j_n_arr, i_n_arr], -1)

        # Bounceback bc enforced
        aux_arr = np.where(aux_arr >= 0,f_ind(fnode_count,dvs.Q,aux_arr,
                      np.arange(dvs.Q)),f_ind(fnode_count,dvs.Q,n,dvs.RDIR))

        stream_arr[n*dvs.Q:(n+1)*dvs.Q] = aux_arr
    #end for
    del enum_fnodes
    del aux_arr

    lat = abc_lattice.make_square_lattice('Lattice1',0.1,(cols,rows))
    lat.new_data_container('Fluid',fnode_coords)

    lat.get_data_container().set_data('MaterialId',geom)
    lat.get_data_container('Fluid').set_data('Label',fnode_labels)
    lat.get_data_container('Fluid').set_data('ReadArrayIndex',stream_arr)

    return lat

# end function preprocess
# ---------------------------------------------------------------------------
def init_distributions(lat,dvs,ref_den,f_ind):

    init_feq = np.zeros(dvs.Q, dtype=np.float)
    lb.feq2_2D(dvs,ref_den,0.0,0.0,init_feq)

    fncount = lat.get_node_count('Fluid')

    fi1 = np.zeros(dvs.Q*fncount, dtype=np.float)
    fi2 = np.zeros(dvs.Q*fncount, dtype=np.float)

    for n in range(fncount):
        fi1[f_ind(fncount,dvs.Q,n,np.arange(dvs.Q))] = init_feq[:]
    # end for

    dens = np.ones(fncount, dtype=np.float)*ref_den
    vels = np.zeros((fncount,2), dtype=np.float)

    lat.get_data_container('Fluid').set_data('Fi1',fi1)
    lat.get_data_container('Fluid').set_data('Fi2',fi2)

    lat.get_data_container('Fluid').set_data('Density',dens)
    lat.get_data_container('Fluid').set_data('Velocity',vels)

# end function init_distributions
# ---------------------------------------------------------------------------
def evolve(lat,dvs,fread,fwrite,tau,gx,gy,f_ind):

    inv_tau_e = float(1.0/tau)
    inv_tau_o = float(8.0*(2.0-inv_tau_e)/(8.0-inv_tau_e)) # The Magic number

    tot_den = float(0.0)
    tot_ux = float(0.0)
    tot_uy = float(0.0)

    fval = np.zeros(dvs.Q, dtype=np.float)
    facc = np.zeros(dvs.Q, dtype=np.float)
    fneq = np.zeros(dvs.Q, dtype=np.float)
    feq  = np.zeros(dvs.Q, dtype=np.float)

    fncount = lat.get_node_count('Fluid')
    stream_arr = lat.get_data_container('Fluid').get_values('ReadArrayIndex')

    relax_timer = 0

    for n in range(fncount):
        fval = fread[stream_arr[n*dvs.Q:(n+1)*dvs.Q]]

        den = dvs.density(fval)
        inv_den = 1.0/den

        lb.facc1_2D(dvs,den,0.5*gx,gy,facc)
        fval = fval + facc

        jx = dvs.momentum_x(fval)
        jy = dvs.momentum_y(fval)
        ux = inv_den*jx
        uy = inv_den*jy

        lat.get_data_container('Fluid').get_values('Density')[n] = den
        lat.get_data_container('Fluid').get_values('Velocity')[n,lb.X] = ux
        lat.get_data_container('Fluid').get_values('Velocity')[n,lb.Y] = uy

        start_time = time.time()

        lb.feq2_2D(dvs, den,ux,uy,feq)
#        lb.bgk_relax(dvs,inv_tau_e,fval,feq)
        lb.trt_relax(dvs, inv_tau_e,inv_tau_o,fval,feq)
        fval = fval + facc

        end_time = time.time()
        comp_time = end_time - start_time
        relax_timer += comp_time

        fwrite[f_ind(fncount,dvs.Q,n,np.arange(dvs.Q))] = fval

        # Exclude inlet and outlet nodes
        if lat.get_data_container('Fluid').get_values('Label')[n] == DOMAIN_NODE:
          tot_den += den
          tot_ux += ux
          tot_uy += uy
        # end if
    # end for

    return (tot_den, tot_ux, tot_uy, relax_timer)

# end function evolve
# ---------------------------------------------------------------------------
