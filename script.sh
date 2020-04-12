
for ((i = 0; i <= 10000; i += 5));
do
	python run_pias_dctcp.py $(echo "scale=4; $i/10000" | bc)
	python run_pias_dctcp_oversub.py $(echo "scale=4; $i/10000" | bc)
	python run_pias_heter.py $(echo "scale=4; $i/10000" | bc)
	python run_pias_vl2.py $(echo "scale=4; $i/10000" | bc)
done

