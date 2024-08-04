provider "aws" {
  region = "us-east-2" # AWS region
}

resource "aws_vpc" "eks_vpc" {
  cidr_block = "10.0.0.0/16" # CIDR block for the VPC
}

resource "aws_subnet" "eks_subnet" {
  count             = 2
  vpc_id            = aws_vpc.eks_vpc.id
  cidr_block        = cidrsubnet(aws_vpc.eks_vpc.cidr_block, 8, count.index)
  availability_zone = element(data.aws_availability_zones.available.names, count.index)
}

data "aws_availability_zones" "available" {}

resource "aws_eks_cluster" "eks_cluster" {
  name     = "superherogen-cluster" # Cluster name
  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = aws_subnet.eks_subnet[*].id
  }
}

resource "aws_iam_role" "eks_role" {
  name = "eks-role" # IAM role name

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "eks_policy_attachment" {
  role       = aws_iam_role.eks_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "eks_service_policy_attachment" {
  role       = aws_iam_role.eks_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
}

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = aws_eks_cluster.eks_cluster.name
  node_group_name = "superherogen-nodes" # Node group name
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = aws_subnet.eks_subnet[*].id

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  instance_types = ["t3.medium"] # Instance type for the nodes

  # Specify the AMI ID for the node group
  launch_template {
    id      = aws_launch_template.eks_node_launch_template.id
    version = "$Latest"
  }
}

resource "aws_iam_role" "eks_node_role" {
  name = "eks-node-role" # IAM role name for nodes

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "eks_node_policy_attachment" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy_attachment" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "eks_registry_policy_attachment" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_launch_template" "eks_node_launch_template" {
  name_prefix   = "eks-node-"
  image_id       = "ami-0a31f06d64a91614b" # Amazon Linux 2 AMI ID
  instance_type  = "t3.medium"

  lifecycle {
    create_before_destroy = true
  }

  # Define the IAM instance profile for the nodes
  iam_instance_profile {
    name = aws_iam_instance_profile.eks_node_instance_profile.name
  }
}

resource "aws_iam_instance_profile" "eks_node_instance_profile" {
  name = "eks-node-instance-profile"

  role = aws_iam_role.eks_node_role.name
}
