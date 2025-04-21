#!/bin/bash

# Start NRF - NF Repository Function
echo "Starting NRF..."
./install/bin/open5gs-nrfd &
sleep 2

# Start SCP - Service Communication Proxy
echo "Starting SCP..."
./install/bin/open5gs-scpd &
sleep 2

# Start SEPP - Security Edge Protection Proxy
echo "Starting SEPP..."
./install/bin/open5gs-seppd -c ./install/etc/open5gs/sepp1.yaml &
sleep 2

# Start AMF - Access and Mobility Management Function
echo "Starting AMF..."
./install/bin/open5gs-amfd &
sleep 2

# Start SMF - Session Management Function
echo "Starting SMF..."
./install/bin/open5gs-smfd &
sleep 2

# Start UPF - User Plane Function
echo "Starting UPF..."
./install/bin/open5gs-upfd &
sleep 2

# Start AUSF - Authentication Server Function
echo "Starting AUSF..."
./install/bin/open5gs-ausfd &
sleep 2

# Start UDM - Unified Data Management
echo "Starting UDM..."
./install/bin/open5gs-udmd &
sleep 2

# Start UDR - Unified Data Repository
echo "Starting UDR..."
./install/bin/open5gs-udrd &
sleep 2

# Start PCF - Policy and Charging Function
echo "Starting PCF..."
./install/bin/open5gs-pcfd &
sleep 2

# Start NSSF - Network Slice Selection Function
echo "Starting NSSF..."
./install/bin/open5gs-nssfd &
sleep 2

# Start BSF - Binding Support Function
echo "Starting BSF..."
./install/bin/open5gs-bsfd &
sleep 2


echo "All services started."

# Wait for all background processes to complete (optional, depends on how you want to handle them)
wait

