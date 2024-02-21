echo "*** Start Redis Stack and Bot ***"
docker compose up -d

echo "*** Load Vectors ***"
python3 $PWD/src/loader.py

echo "*** Launch Bot Browser ***"
google-chrome http://192.168.20.101:8000
