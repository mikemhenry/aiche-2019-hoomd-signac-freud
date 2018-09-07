import hoomd
import hoomd.hpmc
hoomd.context.initialize('--mode=cpu')

# parameters
seed = 1     # RNG seed
P = 13.2    # pressure

# run the simulation
hoomd.init.read_gsd(filename='init.gsd', restart='restart.gsd', time_step=0);
mc = hoomd.hpmc.integrate.convex_polygon(restore_state=True, seed=seed);
d = hoomd.dump.gsd("trajectory.gsd", period=500, group=hoomd.group.all());
d.dump_state(mc);

restart = hoomd.dump.gsd("restart.gsd", period=500, group=hoomd.group.all(), truncate=True);
restart.dump_state(mc);

hoomd.analyze.log(filename="log.dat", quantities=['volume'], period=100);
boxmc = hoomd.hpmc.update.boxmc(mc, betaP=P, seed=seed);
boxmc.ln_volume(delta=0.001,weight=1);

hoomd.run(20000);
restart.write_restart();
