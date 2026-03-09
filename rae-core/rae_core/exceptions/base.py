# Copyright 2025 Grzegorz Leśniowski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Base exception classes for RAE Core.
"""

class RAEError(Exception):
    """Base exception for all RAE-related errors."""
    pass

class ContractViolationError(RAEError):
    """Raised when a behavioral or structural contract is violated."""
    pass

class InfrastructureError(RAEError):
    """Raised when an infrastructure component (DB, Vector Store) fails."""
    pass

class SecurityPolicyViolationError(RAEError):
    """Raised when a security policy (e.g., ISO 42001) is violated."""
    pass

class ValidationError(RAEError):
    """Raised when data validation fails."""
    pass

class ResourceExhaustedError(RAEError):
    """Raised when a budget or token limit is reached."""
    pass
