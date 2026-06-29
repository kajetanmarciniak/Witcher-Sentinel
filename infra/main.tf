# =============================================================================
# Witcher Sentinel v7 — The White Frost
# Immutable Infrastructure as Code (Terraform)
# =============================================================================

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

variable "aws_region" {
  description = "AWS region for all Sentinel resources."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Prefix for resource names."
  type        = string
  default     = "witcher-sentinel-v7"
}

variable "s3_bucket_name" {
  description = "Globally unique S3 Bestiary Vault bucket name."
  type        = string
}

variable "cognitive_api_key" {
  description = "API key for the cognitive scoring engine (Groq / OpenAI-compatible)."
  type        = string
  sensitive   = true
}

variable "search_api_key" {
  description = "Tavily search API key."
  type        = string
  sensitive   = true
}

variable "discord_webhook_url" {
  description = "Discord webhook URL for Passiflora alerts."
  type        = string
  sensitive   = true
}

variable "cognitive_base_url" {
  description = "OpenAI-compatible chat completions base URL."
  type        = string
  default     = "https://api.groq.com/openai/v1"
}

variable "cognitive_model" {
  description = "Model identifier for cognitive scoring."
  type        = string
  default     = "llama-3.3-70b-versatile"
}

variable "cognitive_max_concurrency" {
  description = "Max concurrent cognitive API calls per Lambda invocation."
  type        = number
  default     = 8
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds."
  type        = number
  default     = 90
}

variable "lambda_memory" {
  description = "Lambda memory in MB."
  type        = number
  default     = 512
}

variable "schedule_expression" {
  description = "EventBridge schedule (dummy: rate(1 hour); production: cron(0 8 * * ? *))."
  type        = string
  default     = "rate(1 hour)"
}

# -----------------------------------------------------------------------------
# Package — zip project root, excluding infra & secrets
# -----------------------------------------------------------------------------

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/.."
  output_path = "${path.module}/lambda.zip"

  excludes = [
    ".git",
    ".env",
    ".env.*",
    "infra",
    "__pycache__",
    ".terraform",
    ".venv",
    "venv",
    "build",
    "dist",
    ".dev",
    "*.pyc",
    ".DS_Store",
    "Thumbs.db",
  ]
}

# -----------------------------------------------------------------------------
# S3 — Bestiary Vault (stateful memory + RAG corpus)
# -----------------------------------------------------------------------------

resource "aws_s3_bucket" "bestiary" {
  bucket = var.s3_bucket_name

  tags = {
    Project = var.project_name
    Version = "7.0"
  }
}

resource "aws_s3_bucket_versioning" "bestiary" {
  bucket = aws_s3_bucket.bestiary.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "bestiary" {
  bucket = aws_s3_bucket.bestiary.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# -----------------------------------------------------------------------------
# IAM — Lambda execution role (CloudWatch Logs + S3 Bestiary access)
# -----------------------------------------------------------------------------

resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Project = var.project_name
    Version = "7.0"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_s3_bestiary" {
  name = "${var.project_name}-s3-bestiary"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "BestiaryVaultAccess"
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
      ]
      Resource = [
        aws_s3_bucket.bestiary.arn,
        "${aws_s3_bucket.bestiary.arn}/*",
      ]
    }]
  })
}

# -----------------------------------------------------------------------------
# Lambda — Witcher Sentinel compute
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "sentinel" {
  function_name = var.project_name
  role          = aws_iam_role.lambda.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      COGNITIVE_API_KEY         = var.cognitive_api_key
      COGNITIVE_BASE_URL        = var.cognitive_base_url
      COGNITIVE_MODEL           = var.cognitive_model
      COGNITIVE_MAX_CONCURRENCY = tostring(var.cognitive_max_concurrency)
      SEARCH_API_KEY            = var.search_api_key
      DISCORD_WEBHOOK_URL       = var.discord_webhook_url
      AWS_S3_BUCKET             = aws_s3_bucket.bestiary.id
      AWS_REGION                = var.aws_region
    }
  }

  tags = {
    Project = var.project_name
    Version = "7.0"
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_iam_role_policy.lambda_s3_bestiary,
  ]
}

# -----------------------------------------------------------------------------
# EventBridge — scheduled hunt trigger
# -----------------------------------------------------------------------------

resource "aws_cloudwatch_event_rule" "sentinel_schedule" {
  name                = "${var.project_name}-schedule"
  description         = "Triggers Witcher Sentinel hunt on a fixed schedule."
  schedule_expression = var.schedule_expression

  tags = {
    Project = var.project_name
    Version = "7.0"
  }
}

resource "aws_cloudwatch_event_target" "sentinel_lambda" {
  rule      = aws_cloudwatch_event_rule.sentinel_schedule.name
  target_id = "${var.project_name}-lambda"
  arn       = aws_lambda_function.sentinel.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sentinel.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.sentinel_schedule.arn
}

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "lambda_function_name" {
  description = "Deployed Lambda function name."
  value       = aws_lambda_function.sentinel.function_name
}

output "lambda_function_arn" {
  description = "Deployed Lambda function ARN."
  value       = aws_lambda_function.sentinel.arn
}

output "s3_bucket_name" {
  description = "Bestiary Vault S3 bucket."
  value       = aws_s3_bucket.bestiary.id
}

output "eventbridge_rule_name" {
  description = "EventBridge schedule rule name."
  value       = aws_cloudwatch_event_rule.sentinel_schedule.name
}

output "deploy_package_hash" {
  description = "SHA256 hash of the Lambda deployment package."
  value       = data.archive_file.lambda_zip.output_base64sha256
}
