"""Auth layer of Security Studio — thin wrapper around cloudforge-auth-core."""
from src.auth.dependencies import Principal, get_current_user, require_scope

require_security_read = require_scope("security:read")
require_security_write = require_scope("security:write")

__all__ = ["Principal", "get_current_user", "require_security_read", "require_security_write"]
