provider "aws" {
  region = "us-east-2" # AWS region where the EKS cluster will be created
}

resource "aws_vpc" "eks_vpc" {
  cidr_block = "10.0.0.0/16" # CIDR block for the VPC
}

resource "aws_subnet" "eks_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.eks_vpc.id
  cidr_block              = cidrsubnet(aws_vpc.eks_vpc.cidr_block, 8, count.index)
  availability_zone       = element(data.aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = true
}

data "aws_iam_role" "eks_role" {
  name = "eks-service-role" # IAM role for EKS
}

resource "aws_eks_cluster" "eks_cluster" {
  name     = "superherogen-cluster" # Name of the EKS cluster
  role_arn = data.aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = aws_subnet.eks_subnet[*].id
  }
}

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = aws_eks_cluster.eks_cluster.name
  node_group_name = "superherogen-nodes" # Name of the EKS node group
  node_role_arn   = data.aws_iam_role.eks_role.arn
  subnet_ids      = aws_subnet.eks_subnet[*].id

  scaling_config {
    desired_size = 2 # Desired number of nodes
    max_size     = 3 # Maximum number of nodes
    min_size     = 1 # Minimum number of nodes
  }

  instance_types = "t3.medium" # Instance type for the nodes
}
