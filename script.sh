
for ((i = 1725; i <= 10000; i += 5));
do
	echo "$1" $(echo "scale=4; $i/10000" | bc)
	python $1 $(echo "scale=4; $i/10000" | bc)
	
	if [ "$1" == "run_pias_vl2.py" ]; then
		mv g_*$(echo "scale=(3+($i%10)/5); $i/10000" | bc) /mnt/hgfs/Downloads/results/
	fi
done

