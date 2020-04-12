import threading
import os
import Queue
import sys

def worker():
	while True:
		try:
			j = q.get(block = 0)
		except Queue.Empty:
			return
		#Make directory to save results
		os.system('mkdir -p g_'+j[2]+'/'+j[1])
		os.system(j[0])


q = Queue.Queue()

sim_end = 10000
link_rate = 10
mean_link_delay = 0.0000002
host_delay = 0.000020
queueSize = 120
load_arr = [0.9/2.75, 0.8/2.75, 0.7/2.75, 0.6/2.75, 0.5/2.75]
connections_per_pair = 1
meanFlowSize = 1138*1460
paretoShape = 1.05
flow_cdf = 'CDF_dctcp.tcl'

enableMultiPath = 1
perflowMP = 0

sourceAlg = 'DCTCP-Sack'
initWindow = 70
ackRatio = 1
slowstartrestart = 'true'
if len(sys.argv) == 1:
	DCTCP_g = 0.0625
else:
	DCTCP_g = float(sys.argv[1])
min_rto = 0.002
prob_cap_ = 5

switchAlg = 'Priority'
DCTCP_K = 65.0
drop_prio_ = 'true'
prio_scheme_ = 2
deque_prio_ = 'true'
keep_order_ = 'true'
prio_num_arr = [1]
ECN_scheme_ = 2 #Per-port ECN marking
pias_thresh_0 = [759*1460, 909*1460, 999*1460, 956*1460, 1059*1460]
pias_thresh_1 = [1132*1460, 1329*1460, 1305*1460, 1381*1460, 1412*1460]
pias_thresh_2 = [1456*1460, 1648*1460, 1564*1460, 1718*1460, 1643*1460]
pias_thresh_3 = [1737*1460, 1960*1460, 1763*1460, 2028*1460, 1869*1460]
pias_thresh_4 = [2010*1460, 2143*1460, 1956*1460, 2297*1460, 2008*1460]
pias_thresh_5 = [2199*1460, 2337*1460, 2149*1460, 2551*1460, 2115*1460]
pias_thresh_6 = [2325*1460, 2484*1460, 2309*1460, 2660*1460, 2184*1460]

topology_spt = 8
topology_tors = 4
topology_spines = 2
topology_x = 1

ns_path = '/home/vincentlam0320/fyp/ns-allinone-2.34/ns-2.34/ns'
sim_script = 'spine_empirical.tcl'

for prio_num_ in prio_num_arr:
	for i in range(len(load_arr)):

		scheme = 'unknown'
		if switchAlg == 'Priority' and prio_num_ == 1:
			if sourceAlg == 'DCTCP-Sack':
				scheme = 'dctcp'

		if scheme == 'unknown':
			print 'Unknown scheme'
			sys.exit(0)

		#Directory name: workload_scheme_load_[load]
		directory_name = 'websearch_%s_%d' % (scheme,int(load_arr[i]*100))
		directory_name = directory_name.lower()
		#Simulation command
		cmd = ns_path+' '+sim_script+' '\
			+str(sim_end)+' '\
			+str(link_rate)+' '\
			+str(mean_link_delay)+' '\
			+str(host_delay)+' '\
			+str(queueSize)+' '\
			+str(load_arr[i])+' '\
			+str(connections_per_pair)+' '\
			+str(meanFlowSize)+' '\
			+str(paretoShape)+' '\
			+str(flow_cdf)+' '\
			+str(enableMultiPath)+' '\
			+str(perflowMP)+' '\
			+str(sourceAlg)+' '\
			+str(initWindow)+' '\
			+str(ackRatio)+' '\
			+str(slowstartrestart)+' '\
			+str(DCTCP_g)+' '\
			+str(min_rto)+' '\
			+str(prob_cap_)+' '\
			+str(switchAlg)+' '\
			+str(DCTCP_K)+' '\
			+str(drop_prio_)+' '\
			+str(prio_scheme_)+' '\
			+str(deque_prio_)+' '\
			+str(keep_order_)+' '\
			+str(prio_num_)+' '\
			+str(ECN_scheme_)+' '\
			+str(pias_thresh_0[i])+' '\
			+str(pias_thresh_1[i])+' '\
			+str(pias_thresh_2[i])+' '\
			+str(pias_thresh_3[i])+' '\
			+str(pias_thresh_4[i])+' '\
			+str(pias_thresh_5[i])+' '\
			+str(pias_thresh_6[i])+' '\
			+str(topology_spt)+' '\
			+str(topology_tors)+' '\
			+str(topology_spines)+' '\
			+str(topology_x)+' '\
			+str('./g_'+str(DCTCP_g)+'/'+directory_name+'/flow.tr')+'  >'\
			+str('./g_'+str(DCTCP_g)+'/'+directory_name+'/logFile.tr')

		q.put([cmd, directory_name, str(DCTCP_g)])

#Create all worker threads
threads = []
number_worker_threads = 20

#Start threads to process jobs
for i in range(number_worker_threads):
	t = threading.Thread(target = worker)
	threads.append(t)
	t.start()

#Join all completed threads
for t in threads:
	t.join()
