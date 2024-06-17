resource "aws_vpc" "my_vpc" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "nikita-study-vpc"
  }
}



resource "aws_subnet" "my_vpc_subnet_public_01" {
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  vpc_id                  = aws_vpc.my_vpc.id
  map_public_ip_on_launch = true
  tags = {
    Name = "my_vpc_subnet_public_01"
  }
}


#данный компонент позволяте нашей vpc коммуницировать с интернетом
resource "aws_internet_gateway" "eks-demo-internet-gateway-01" {
  vpc_id = aws_vpc.eks-demo-vpc-01.id
  tags = {
    Name = "eks-demo-internet-gateway-01"
  }
}