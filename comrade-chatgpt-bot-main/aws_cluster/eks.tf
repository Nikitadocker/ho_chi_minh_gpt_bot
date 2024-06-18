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


#данный компонент позволяте нашей vpc коммуницировать с интернет
resource "aws_internet_gateway" "my-eks-internet-gateway-01" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    Name = "my-eks-internet-gateway-01"
  }
}

# настраиваем маршрут от vpc на все адреса в интернете,через интернет шлюз. Main route table контролирует все subnet,котрые явно не связаны с другими таблицами
resource "aws_route" "eks-internet_access" {
  route_table_id         = aws_vpc.my_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.my-eks-internet-gateway-01.id

}


#ARN это индефикатор ресурса aws
#IAM role нужна что бы control panel могли делать обращение к AWS API
resource "aws_eks_cluster" "eks-study-cluster-01" {
  name     = "eks-study-cluster-01"
  version  = "1.30"
  role_arn = aws_iam_role.eks-demo-cluster-admin-role-01.arn

  vpc_config {
    subnet_ids              = [aws_subnet.my_vpc_subnet_public_01.id]
    endpoint_public_access  = true
    endpoint_private_access = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }
  depends_on = [
    aws_iam_role_policy_attachment.eks-demo-cluster-01-AmazonEKSClusterPolicy,aws_iam_role_policy_attachment.eks-demo-cluster-01-AmazonEKSVPCResourceController
  ]
  tags = {
    demo = "eks"
  }
}


data "aws_iam_policy_document" "eks-demo-cluster-admin-role-policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}



# eks-cluster-03
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role
resource "aws_iam_role" "eks-demo-cluster-admin-role-01" {
  name               = "eks-demo-cluster-admin-role-01"
  assume_role_policy = data.aws_iam_policy_document.eks-demo-cluster-admin-role-policy.json
}

# Policy в aws это обьект который определяет разрешения для управления ресурсами

#Данный ресурс прикрепляет role к policy
# Данная роль может упралять nodes и cоздавать load balancing
resource "aws_iam_role_policy_attachment" "eks-demo-cluster-01-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks-demo-cluster-admin-role-01.name
}


# Reference: https://docs.aws.amazon.com/eks/latest/userguide/security-groups-for-pods.html
resource "aws_iam_role_policy_attachment" "eks-demo-cluster-01-AmazonEKSVPCResourceController" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.eks-demo-cluster-admin-role-01.name
}