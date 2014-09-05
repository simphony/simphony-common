# ===========================================================================
# Test program for lattice data structures
# ---------------------------------------------------------------------------
# Keijo Mattila & Tuomas Puurtinen, SimPhoNy, JYU, August 2014.
# ===========================================================================
# Import modules
# ===========================================================================
import sys
import time
import numpy as np
import pylab as pl
from math import sqrt
import lb_solver
import lb
import bc
# ---------------------------------------------------------------------------
# A memory-address function for collision-optimized data layout
# ---------------------------------------------------------------------------
def FI_IND(N,Q,n,q):
    return n*Q + q
# ---------------------------------------------------------------------------
# A memory-address function for stream-optimized data layout
# ---------------------------------------------------------------------------
#def FI_IND(N,Q,n,q):
#    return q*N + n
# ===========================================================================
# Test program 
# ===========================================================================
argc = len(sys.argv)

if argc < 8:
    print "Provide 7 parameters: gx gy geom_fname tau ax titers evol_tstep!"
    exit()

gx = int(sys.argv[1])  
gy = int(sys.argv[2])
geom_fname = sys.argv[3]
tau = float(sys.argv[4])
ax = float(sys.argv[5])
titers = int(sys.argv[6])
evol_tstep = int(sys.argv[7])

rows = gy
cols = gx
d2q9 = lb.D2Q9()

ref_den = float(1.0)
kvisc = d2q9.CT2*(tau - 0.5)
# ---------------------------------------------------------------------------
# Set up simulation
# ---------------------------------------------------------------------------
lat = lb_solver.preprocess(d2q9, rows, cols, geom_fname, FI_IND)

# Store information about inlet and outlet fluid nodes
inlet_fnode_index  = np.nonzero(lat.get_node_ids('Fluid')[:,1] == 0)[0]
inlet_inward_nghbr = np.nonzero(lat.get_node_ids('Fluid')[:,1] == 1)[0]
inlet_node_ids = lat.get_node_ids('Fluid')[inlet_fnode_index]

outlet_fnode_index  = np.nonzero(lat.get_node_ids('Fluid')[:,1] == cols-1)[0]
outlet_inward_nghbr = np.nonzero(lat.get_node_ids('Fluid')[:,1] == cols-2)[0]
outlet_node_ids = lat.get_node_ids('Fluid')[outlet_fnode_index]

lat.new_data_container('Inlet',inlet_node_ids)
lat.new_data_container('Outlet',outlet_node_ids)

lat.get_data_container('Inlet').set_data('FluidNodeIndex',inlet_fnode_index)
lat.get_data_container('Inlet').set_data('InwardNeighbour',inlet_inward_nghbr)

lat.get_data_container('Outlet').set_data('FluidNodeIndex',outlet_fnode_index)
lat.get_data_container('Outlet').set_data('InwardNeighbour',outlet_inward_nghbr)

lat.get_data_container('Fluid').get_values('Label')[inlet_fnode_index] = lb_solver.INLET_NODE
lat.get_data_container('Fluid').get_values('Label')[outlet_fnode_index] = lb_solver.OUTLET_NODE

pl.imshow(lat.get_data_container().get_values('MaterialId'))
pl.title('Geometry')
pl.show()

# ---------------------------------------------------------------------------
# Initialize simulation variables
# ---------------------------------------------------------------------------
lb_solver.init_distributions(lat, d2q9, ref_den, FI_IND)

# ---------------------------------------------------------------------------
# Print data containers and their data keywords
# ---------------------------------------------------------------------------

print '---------------------------------------------------------------------'
print 'Data containers'
print '---------------------------------------------------------------------'
for container in lat.get_data_containers():
    print container.get_name(), ':', container.get_keywords()
#end for 

# ---------------------------------------------------------------------------
# Time evolution
# ---------------------------------------------------------------------------
fread = lat.get_data_container('Fluid').get_values('Fi1')
fwrite = lat.get_data_container('Fluid').get_values('Fi2')

start_time = time.time()
tot_relax_time = 0

print '---------------------------------------------------------------------'

for t in range(titers):
     
    bc.d2q9_inlet_bc(lat,d2q9,fread,fwrite,ref_den,FI_IND)
    bc.d2q9_outlet_bc(lat,d2q9,fread,fwrite,ref_den,FI_IND)
    
    (tden,tux,tuy,relax_timer) = lb_solver.evolve(lat,d2q9,fread,fwrite,tau,ax,0.0,FI_IND)
    tot_relax_time += relax_timer
    
    swap = fread 
    fread = fwrite
    fwrite = swap
 
    if t%evol_tstep == 0 or t == (titers-1):
        print 't:', t, ', tot.den =', tden, \
              ', tot.ux =', tux, ', tot.uy =', tuy
# end for

print '---------------------------------------------------------------------'
end_time = time.time()
comp_time = end_time - start_time

fncount = lat.get_node_count('Fluid')
lu = fncount*titers

print 'Computing time (s) =', comp_time, ', MFLUPS = ', lu/(comp_time*1e6)
print 'Relaxation time (s) =', tot_relax_time
# ---------------------------------------------------------------------------
# Post-processing
# ---------------------------------------------------------------------------
curr_dens = np.zeros((rows,cols), dtype=np.float)
curr_uxs = np.zeros((rows,cols), dtype=np.float)
curr_uys = np.zeros((rows,cols), dtype=np.float)

den_fnodes = lat.get_data_container('Fluid').get_values('Density')
ux_fnodes = lat.get_data_container('Fluid').get_values('Velocity')[:,lb.X]
uy_fnodes = lat.get_data_container('Fluid').get_values('Velocity')[:,lb.Y]
fnode_coords = lat.get_node_ids('Fluid')

curr_dens[fnode_coords[:,0], fnode_coords[:,1]] = den_fnodes[:]
curr_uxs[fnode_coords[:,0], fnode_coords[:,1]] = ux_fnodes[:]
curr_uys[fnode_coords[:,0], fnode_coords[:,1]] = uy_fnodes[:]

pl.imshow(curr_dens[:,1:-1])
pl.title('Density')
pl.show()

pl.imshow(curr_uxs[:,1:-1])
pl.title('Velocity, x-component')
pl.show()

pl.imshow(curr_uys[:,1:-1])
pl.title('Velocity, y-component')
pl.show()

speed = np.array(np.sqrt(ux_fnodes[:]**2 + uy_fnodes[:]**2), dtype=float)
#pl.streamplot(domain_fcoords[:,1],domain_fcoords[:,0],ux_fnodes[:],uy_fnodes[:])
pl.quiver(fnode_coords[:,1],fnode_coords[:,0],ux_fnodes[:],uy_fnodes[:],speed)
pl.title('Velocity')
pl.show()

# ---------------------------------------------------------------------------
# For Poiseuille flow
# ---------------------------------------------------------------------------
channel_h = 0.5*(rows-2)
max_ana_vx = ((0.5*channel_h*channel_h)/kvisc)*ax;
max_sim_vx = np.max(ux_fnodes)

center_dist = np.arange(rows, dtype=float) - 0.5 - channel_h
ana_vx_prof = max_ana_vx*(1.0 - (center_dist[:]/channel_h)**2)

rel_L2_err = sqrt(np.sum((ana_vx_prof[1:-1] - curr_uxs[1:-1,cols/2])**2)/np.sum(ana_vx_prof[1:-1]))

print '---------------------------------------------------------------------'
print 'Max.sim.vx =', max_sim_vx, ', max.ana.vx =', max_ana_vx
print '---------------------------------------------------------------------'
print 'Rel.L2 error =', rel_L2_err
print '---------------------------------------------------------------------'

sim_pl = pl.plot(curr_uxs[:,cols/2],'-bs', label = 'Simulated')
ana_pl = pl.plot(ana_vx_prof,'-go', label = 'Analytical')
pl.title('Velocity, x-component, profile')
pl.legend()
pl.show()
# ===========================================================================
