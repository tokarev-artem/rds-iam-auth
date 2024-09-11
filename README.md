## This is a python function to demonstrate RDS IAM Authentication for education purposes

## To enable RDS IAM plugin run the next command:

> ALTER USER 'admin' IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';

## Download a certificate https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html#UsingWithRDS.SSL.CertificatesDownload 

and edit ssl_ca in ssl_config 