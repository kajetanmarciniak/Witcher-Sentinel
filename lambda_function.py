"""AWS Lambda entrypoint — keeps handler name compatible with existing deploy config."""
from main import lambda_handler

__all__ = ["lambda_handler"]
