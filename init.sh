chmod u+x *.sh

cd dashboard
chmod u+x *.sh
./get_wait-for-it.sh
chmod u+x *.sh

cd dashboard
python generate_key.py
echo "localhost, web" > allowed_hosts.txt
