#!/bin/bash

PROJECT_NAME="EnzyHTP Web Application"
VALID_DATE=365
CN="localhost"

# Function to display help message
show_help() {
    echo "Usage: ${0##*/} [--cn COMMON_NAME] [--days VALID_DATE]"
    echo
    echo "Generate Self-signed X509 Certificate using OpenSSL."
    echo
    echo "   --cn    Specify the common name (domain name). Defaults 'localhost'."
    echo "   --days        Specify the validity period of the certificate. Defaults '365'."
    echo "   -h, --help    Display this help and exit."
}

# Define the options
OPTS=$(getopt -o hn: --long help,name: -- "$@")

# Exit if the options have not been correctly specified.
if [ $? != 0 ]; then exit 1; fi

# Extract options and their arguments into variables.
eval set -- "$OPTS"

while true; do
    case "$1" in
        -h|--help)
            show_help
            exit 0;;
        --cn)
            CN="$2"; shift 2;;
        --days)
            VALID_DATE=$3;;
        --)
            shift; break;;
        *)
            break;;
    esac
done

# Generate the openssl configuration files.
cat > ca_cert.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no

[ req_distinguished_name ]
 O                      = $PROJECT_NAME Certificate Authority
EOF

cat > server_cert.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no

[ req_distinguished_name ]
 O                      = $PROJECT_NAME
 CN                     = $CN
EOF

cat > client_cert.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no

[ req_distinguished_name ]
 O                      = $PROJECT_NAME Device Certificate
 CN                     = $CN
EOF

mkdir -p ca
mkdir -p server
mkdir -p client

# Generate private key
openssl genrsa -out ca.key 1024
openssl genrsa -out server.key 1024
openssl genrsa -out client.key 1024

# To create a certificate request file based on the private key, you need to enter some meta-information of the certificate: email, domain name, etc.
openssl req -out ca.req -key ca.key -new -config ./ca_cert.conf
openssl req -out server.req -key server.key -new -config ./server_cert.conf
openssl req -out client.req -key client.key -new -config ./client_cert.conf

# Combine the private key and request file to create a self-signed certificate
openssl x509 -req -in ca.req -out ca.crt -sha256 -days $VALID_DATE -signkey ca.key
openssl x509 -req -in server.req -out server.crt -sha256 -CAcreateserial -days $VALID_DATE -CA ca.crt -CAkey ca.key
openssl x509 -req -in client.req -out client.crt -sha256 -CAcreateserial -days $VALID_DATE -CA ca.crt -CAkey ca.key

mv ca.crt ca.key ca/
mv server.crt server.key server/
mv client.crt client.key client/

rm *.conf
rm *.req
rm *.srl

# Reference: https://zhuanlan.zhihu.com/p/366915564