#!/bin/bash
# python3 test.py &
# pid=$!

# echo "Server process started with PID: $pid"
# sleep 1
for i in {1..2}
do
    python3 client.py > outcome$i.txt &
    # python3 client.py
done

# kill $pid
# echo "Background process terminated"