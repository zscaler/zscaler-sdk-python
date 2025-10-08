# Security Policy

## Security Considerations

### JWT Library and CWE-326 Mitigation

#### Background

The Zscaler SDK uses python-jose (version 3.5.0) for OAuth 2.0 JWT client assertion authentication. We migrated from PyJWT to python-jose for consistency with our Go SDK (which uses go-jose).

**Historical Context - PyJWT CWE-326**:
- PyJWT had a known vulnerability classification: CWE-326 (Inadequate Encryption Strength)
- Issue: PyJWT does not enforce minimum key lengths for HMAC or RSA keys
- We addressed this by migrating to python-jose and implementing RSA key validation

#### Risk Assessment for Zscaler SDK

**Risk Level: LOW**

The risk to the Zscaler SDK is minimal because:

1. **SDK Role**: The SDK acts as an OAuth client, not a JWT issuer or validator in security-critical contexts
2. **Key Source**: The SDK uses RSA keys from Zscaler's OAuth infrastructure, not user-generated keys
3. **Zscaler Standards**: Zscaler's OAuth infrastructure uses industry-standard key lengths (≥2048 bits)
4. **Limited Attack Surface**: The vulnerability primarily affects systems that accept keys from untrusted sources
5. **python-jose**: Actively maintained with known security issues patched (e.g., RS256 verification issue fixed in 3.3.0+)

#### Mitigation Implemented

To provide defense-in-depth security, the SDK now includes **RSA key strength validation**:

- **Minimum Key Size**: 2048 bits (NIST recommendation)
- **Validation Point**: All RSA private keys are validated before use
- **Error Handling**: Weak keys are rejected with clear error messages

```python
# Example: Key validation occurs automatically
from zscaler.oneapi_oauth_client import OAuth

# If a weak key is provided, you'll receive:
# ValueError: Insufficient RSA key strength: 1024 bits. 
# Minimum required: 2048 bits (NIST recommendation).
```

#### Recommendations for SDK Users

1. **Use Strong Keys**: Ensure all RSA keys used with the SDK are ≥2048 bits
2. **Key Generation**: When generating keys for Zscaler OAuth:
   ```bash
   # Generate a secure 2048-bit RSA key
   openssl genrsa -out private_key.pem 2048
   
   # Or for higher security, use 4096 bits
   openssl genrsa -out private_key.pem 4096
   ```

3. **Zscaler-Provided Keys**: Keys provided by Zscaler's OAuth system meet security requirements

#### Why python-jose?

We chose python-jose over other JWT libraries for several reasons:

- **Consistency**: Aligns with our Go SDK which uses go-jose
- **Comprehensive**: Full JOSE implementation (JWS, JWE, JWK, JWT)
- **Well-maintained**: Active development with security fixes
- **Battle-tested**: ~15M downloads/month, used by major projects
- **Security**: Known issues patched (RS256 verification fix in 3.3.0+)

#### python-jose Version Status

- **Current Version**: 3.5.0 (Latest as of October 2024)
- **Security Status**: Known vulnerabilities patched
- **Maintainer**: Active community maintenance
- **Compatibility**: Drop-in replacement for PyJWT API

#### Alternative JWT Libraries

Other Python JWT libraries we evaluated:

- **PyJWT**: Previous library, CWE-326 concerns addressed by migration
- **joserfc**: Modern RFC-compliant implementation (newer, smaller community)
- **authlib**: Full OAuth/JWT framework (heavier, overkill for our needs)

## Reporting Security Issues

If you discover a security vulnerability in the Zscaler SDK, please report it to:

- **Email**: devrel@zscaler.com
- **GitHub**: [Security Advisory](https://github.com/zscaler/zscaler-sdk-python/security/advisories)

Please do not report security vulnerabilities through public GitHub issues.

## Security Best Practices

When using the Zscaler SDK:

1. **Credentials Management**
   - Never commit credentials to version control
   - Use environment variables or secure secret management
   - Rotate credentials regularly

2. **Key Management**
   - Use minimum 2048-bit RSA keys
   - Store private keys securely with appropriate file permissions
   - Rotate keys according to your security policy

3. **Network Security**
   - Always use HTTPS for API communications
   - Validate SSL/TLS certificates
   - Keep the SDK and dependencies updated

4. **Logging Security**
   - Configure logging to avoid exposing sensitive data
   - Never log credentials, tokens, or keys
   - Sanitize logs before sharing for support

## Dependencies Security

The SDK regularly updates dependencies to address security vulnerabilities. Monitor:

- GitHub Dependabot alerts
- Security advisories for Python packages
- Release notes for security-related updates

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.8.x   | :white_check_mark: |
| < 1.8   | :x:                |

## Updates and Monitoring

- Subscribe to release notifications on GitHub
- Review CHANGELOG.md for security-related updates
- Monitor Python security advisories at [PyPA Advisory Database](https://github.com/pypa/advisory-database)

