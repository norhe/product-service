#! /bin/bash

# install the product service app
sudo adduser --disabled-password --gecos "" product

# install the requirements
sudo chown -R product:product /home/product/.cache
pip3 install flask
pip3 install pymongo

# download the apply
mkdir /home/product/src
cd /home/product/src
git clone https://github.com/norhe/product-service.git

# systemd

cat <<EOF | sudo tee /lib/systemd/system/product.service
[Unit]
Description=product.py - Product service API
After=network.target

[Service]
Type=simple
User=product
ExecStart=/usr/local/bin/envconsul -prefix product_conf /usr/bin/python3 /home/product/src/product-service/product.py
Restart=always
SyslogIdentifier=product_service

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable product.service
sudo systemctl start product.service
