
for ((i = 1310; i <= 10000; i += 15));
do
	python run_pias_dctcp.py $(echo "scale=4; $i/10000" | bc) & 
	python run_pias_dctcp_oversub.py $(echo "scale=4; $i/10000" | bc) &
	python run_pias_heter.py $(echo "scale=4; $i/10000" | bc) &
	wait
	
	python run_pias_vl2.py $(echo "scale=4; $i/10000" | bc) & 
	python run_pias_dctcp.py $(echo "scale=4; ($i+5)/10000" | bc) & 
	python run_pias_dctcp_oversub.py $(echo "scale=4; ($i+5)/10000" | bc) &
	wait

	python run_pias_heter.py $(echo "scale=4; ($i+5)/10000" | bc) &
	python run_pias_vl2.py $(echo "scale=4; ($i+5)/10000" | bc) & 
	python run_pias_dctcp.py $(echo "scale=4; ($i+10)/10000" | bc) & 
	wait
	
	python run_pias_dctcp_oversub.py $(echo "scale=4; ($i+10)/10000" | bc) &
	python run_pias_heter.py $(echo "scale=4; ($i+10)/10000" | bc) &
	python run_pias_vl2.py $(echo "scale=4; ($i+10)/10000" | bc) & 
	wait

	mv g_* /mnt/hgfs/Downloads/results/
done

