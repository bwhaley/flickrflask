/usr/local/packer/packer build -var 'base_name=flickr_base' -var 'description=Flickr Demo App Docker 0.7.5 Ubuntu 12.04.3 LTS Instance Store'  -var 'dockerfile_dir=/vagrant/flickrdemo/etc/base/' -var "aws_access_key=${AWS_ACCESS_KEY_ID}" -var "aws_secret_key=${AWS_SECRET_ACCESS_KEY}" packer_demo_template.json