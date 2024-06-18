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
  role_arn = aws_iam_role.eks-study-cluster-admin-role-01.arn

  vpc_config {
    subnet_ids              = [aws_subnet.my_vpc_subnet_public_01.id]
    endpoint_public_access  = true
    endpoint_private_access = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }
  depends_on = [
    aws_iam_role_policy_attachment.eks-study-cluster-01-AmazonEKSClusterPolicy, aws_iam_role_policy_attachment.eks-study-cluster-01-AmazonEKSVPCResourceController
  ]
  tags = {
    study = "eks"
  }
}

#policy в виде json
data "aws_iam_policy_document" "eks-study-cluster-admin-role-policy" {
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
resource "aws_iam_role" "eks-study-cluster-admin-role-01" {
  name               = "eks-study-cluster-admin-role-01"
  assume_role_policy = data.aws_iam_policy_document.eks-study-cluster-admin-role-policy.json
}

# Policy в aws это обьект который определяет разрешения для управления ресурсами

#Данный ресурс прикрепляет role к policy
# Данная политика может упралять nodes и cоздавать load balancing
resource "aws_iam_role_policy_attachment" "eks-study-cluster-01-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks-study-cluster-admin-role-01.name
}

# Данная политика может упралять EPI и IP для worker node
resource "aws_iam_role_policy_attachment" "eks-study-cluster-01-AmazonEKSVPCResourceController" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.eks-study-cluster-admin-role-01.name
}


resource "aws_eks_addon" "eks-study-addon-coredns" {
  cluster_name                = aws_eks_cluster.eks-study-cluster-01.name
  addon_name                  = "coredns"
  addon_version               = "v1.10.1-eksbuild.2" 
  resolve_conflicts_on_create = "OVERWRITE" 
}


resource "aws_eks_addon" "eks-study-addon-kube-proxy" {
  cluster_name                = aws_eks_cluster.eks-study-cluster-01.name
  addon_name                  = "kube-proxy"
  addon_version               = "v1.28.1-eksbuild.1" 
  resolve_conflicts_on_create = "OVERWRITE" 
}

#аддлн для Eni
resource "aws_eks_addon" "eks-study-addon-vpc-cni" {
  cluster_name                = aws_eks_cluster.eks-study-cluster-01.name
  addon_name                  = "vpc-cni"
  addon_version               = "v1.14.1-eksbuild.1" 
  resolve_conflicts_on_create = "OVERWRITE" 
}


output "endpoint" {
  value = aws_eks_cluster.eks-study-cluster-01.endpoint
}

output "kubeconfig-certificate-authority-data" {
  value = aws_eks_cluster.eks-study-cluster-01.certificate_authority[0].data
}

#desired
resource "aws_eks_node_group" "eks-study-ec2-node-group-01" {
  cluster_name    = aws_eks_cluster.eks-study-cluster-01.name
  node_group_name = "eks-study-node-group-01"
  node_role_arn   = aws_iam_role.eks-study-ec2-node-group-role-01.arn
  subnet_ids      = [aws_subnet.my_vpc_subnet_public_01.id]
  instance_types  = ["t3.medium"]

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks-study-node-group-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.eks-study-node-group-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.eks-study-node-group-AmazonEC2ContainerRegistryReadOnly,
  ]
  labels = {
    study = "eks", 
    eksNodeGroup = "t3_medium"
  }
}


resource "aws_iam_role" "eks-demo-ec2-node-group-role-01" {
  name = "eks-demo-ec2-node-group-role-01"
  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}


resource "aws_iam_role_policy_attachment" "eks-demo-node-group-AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks-demo-ec2-node-group-role-01.name
}

resource "aws_iam_role_policy_attachment" "eks-demo-node-group-AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks-demo-ec2-node-group-role-01.name
}

resource "aws_iam_role_policy_attachment" "eks-demo-node-group-AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks-demo-ec2-node-group-role-01.name
}
