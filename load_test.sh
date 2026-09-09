#!/bin/bash
echo "🚀 Starting HEAVY traffic generator to test autoscaling..."
echo "Cleaning up any old load generators..."
kubectl delete pod load-generator --ignore-not-found 2>/dev/null

echo "Starting massive parallel traffic..."
echo "Press Ctrl+C to stop the test at any time."
echo "---------------------------------------------------"

# This runs 10 requests at exactly the same time, over and over, with no sleep delay!
kubectl run -i --tty load-generator \
  --rm \
  --image=busybox:1.28 \
  --restart=Never \
  -- /bin/sh -c "while true; do for i in 1 2 3 4 5 6 7 8 9 10; do wget -q -O- http://practice-api > /dev/null & done; sleep 0.01; done"
