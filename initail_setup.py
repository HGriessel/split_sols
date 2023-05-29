import os
import secrets
import string
import random
import datetime
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID

def generate_self_signed_cert(domain):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'ZA'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'GAUTENG'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, 'CENTURION'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Example Corp'),
            x509.NameAttribute(NameOID.COMMON_NAME, domain)
        ])

        cert = x509.CertificateBuilder().subject_name(subject)\
            .issuer_name(issuer)\
            .public_key(private_key.public_key())\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.datetime.utcnow())\
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))\
            .sign(private_key, hashes.SHA256())

        # Convert private key and certificate to PEM format
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        cert_pem = cert.public_bytes(serialization.Encoding.PEM)

        # Save private key and certificate to files
        with open('ssl/certs/private_key.pem', 'wb') as f:
            f.write(private_key_pem)

        with open('ssl/certs/certificate.pem', 'wb') as f:
            f.write(cert_pem)

        print("Successfully generated self-signed SSL certificate")

def generate_api_token(length):
    alphabet = string.ascii_letters + string.digits
    secure_token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secure_token

def generate_random_string(length):
    letters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(letters) for _ in range(length))


def generate_env_file(username,orginasation,bucket,grafana_domain,grafana_root_url):
    influx_admin_password = generate_random_string(18)
    grafana_admin_password = generate_random_string(18)
    token = generate_api_token(64)
    env_data = {
        
        "GF_SECURITY_ADMIN_PASSWORD": f"{grafana_admin_password}",
        "GF_SERVER_DOMAIN": f"{grafana_domain}",
        "GF_SERVER_ROOT_URL": f"{grafana_root_url}",
        
        "DOCKER_INFLUXDB_INIT_MODE": "setup",
        "DOCKER_INFLUXDB_INIT_USERNAME": f"{username}r",
        "DOCKER_INFLUXDB_INIT_PASSWORD": f"{influx_admin_password}",
        "DOCKER_INFLUXDB_INIT_ORG": f"{orginasation}",
        "DOCKER_INFLUXDB_INIT_BUCKET": f"{bucket}",
        "DOCKER_INFLUXDB_INIT_RETENTION": "1y",
        "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN": f"{token}"
        
    }

    with open(".env", "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")

    print("Successfully generated .env file")

if __name__ == "__main__":
    directory = "grafana"
    user = "472"
    group = "472"
    os.system("chown -R {0}:{1} {2}".format(user, group, directory))
    grafana_domain = "thebigbytefive.africa"
    grafana_sub_domain = "narwal.thebigbytefive.africa"
    grafana_root_url = "http://narwal.thebigbytefive.africa:3000"
    domain = 'example.com'
    generate_self_signed_cert(grafana_sub_domain)

    generate_env_file("admin_auto","FakeOrgA","FakeOrgABrancA",grafana_domain,grafana_root_url)

