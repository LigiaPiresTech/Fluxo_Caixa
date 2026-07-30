import os

# The API modules create their SQLAlchemy engine at import time.
# Tests must never point to a production RDS endpoint.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("ENVIRONMENT", "test")
