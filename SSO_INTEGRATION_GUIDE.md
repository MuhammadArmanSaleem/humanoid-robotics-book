# SSO Integration Guide for Physical AI & Humanoid Robotics Textbook

## Important Note About Better Auth

**Better Auth is not compatible with your current architecture.** Better Auth is specifically designed for Next.js applications, but your project uses Docusaurus (React-based documentation site) with a FastAPI backend. The architecture patterns are fundamentally different.

## Recommended SSO Solution: Auth0

For your Docusaurus + FastAPI setup, we recommend using **Auth0** for SSO functionality. Here's how to integrate it:

### 1. Set Up Auth0 Account

1. Go to [auth0.com](https://auth0.com) and create an account
2. Create a new Application (Single Page Application type)
3. Configure the following settings:
   - Allowed Callback URLs: `http://localhost:3000`, `https://yourdomain.com`
   - Allowed Logout URLs: `http://localhost:3000`, `https://yourdomain.com`
   - Allowed Web Origins: `http://localhost:3000`, `https://yourdomain.com`

### 2. Update Environment Variables

Add these to your `.env.local` file:

```bash
# Frontend environment variables
REACT_APP_AUTH0_DOMAIN=your-auth0-domain.auth0.com
REACT_APP_AUTH0_CLIENT_ID=your-auth0-client-id
REACT_APP_AUTH0_AUDIENCE=your-api-identifier
```

### 3. Install Auth0 Dependencies

For the frontend (in your project root):
```bash
npm install @auth0/auth0-react
```

### 4. Update AuthContext for Auth0 Integration

Replace your current AuthContext with Auth0 integration:

```jsx
import React, { createContext, useContext } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const auth0 = useAuth0();

  // Map Auth0 to your existing interface
  const value = {
    user: auth0.user,
    isAuthenticated: auth0.isAuthenticated,
    isLoading: auth0.isLoading,
    error: null,
    signup: () => {}, // Auth0 handles this
    signin: auth0.loginWithRedirect,
    signout: auth0.logout,
    checkAuth: () => {},
    clearError: () => {},
    handleExternalLogin: () => {}
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
```

### 5. Update Docusaurus Configuration

In your `docusaurus.config.js`, wrap the app with Auth0 provider:

```js
// In docusaurus.config.js, modify the theme config
presets: [
  [
    'classic',
    /** @type {import('@docusaurus/preset-classic').Options} */
    ({
      // ... your existing config
    }),
  ],
],

// Then in your src/theme/Root.jsx:
import React from 'react';
import { Auth0Provider } from '@auth0/auth0-react';
import OriginalRoot from '@theme-original/Root';

const AuthRoot = (props) => {
  return (
    <Auth0Provider
      domain={process.env.REACT_APP_AUTH0_DOMAIN}
      clientId={process.env.REACT_APP_AUTH0_CLIENT_ID}
      authorizationParams={{
        redirect_uri: window.location.origin
      }}
    >
      <OriginalRoot {...props} />
    </Auth0Provider>
  );
};

export default AuthRoot;
```

### 6. Backend Integration

Update your FastAPI backend to accept Auth0 JWT tokens:

```python
# In your backend, add this dependency
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
import requests

security = HTTPBearer()

def verify_auth0_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        # Verify the Auth0 token
        jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"
        issuer = f"https://{settings.auth0_domain}/"

        # Get JWKS
        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(credentials.credentials)

        # Decode token
        decoded_token = jwt.decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.auth0_audience,
            issuer=issuer,
        )

        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 7. Identity Providers

Auth0 supports multiple SSO providers:
- Google
- GitHub
- Microsoft
- Facebook
- And many more

Configure these in your Auth0 dashboard under "Connections" → "Social".

### 8. Migration from Current System

To migrate from the current custom JWT system to Auth0:

1. Update your database schema to store Auth0 user IDs
2. Create a migration script to map existing users to Auth0
3. Update your personalization service to work with Auth0 user IDs
4. Test the transition carefully

## Alternative SSO Solutions

If Auth0 doesn't meet your needs, consider:

1. **Firebase Auth**: Good for Google ecosystem integration
2. **Clerk**: Modern user management platform
3. **Supabase Auth**: Open source Firebase alternative
4. **AWS Cognito**: If using AWS infrastructure

## Current System

Your current custom authentication system is actually quite robust and provides:
- User registration with background collection
- JWT-based authentication
- Password visibility toggles
- Responsive design
- Proper error handling

If SSO isn't absolutely required, your current system is production-ready and secure.

## Next Steps

1. Evaluate if SSO is truly necessary for your use case
2. If yes, choose an appropriate provider (Auth0 recommended)
3. Follow the integration steps above
4. Test thoroughly before deployment