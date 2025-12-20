import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Define initial state
const initialState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

// Auth context
const AuthContext = createContext();

// Auth reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case 'SIGNUP_START':
    case 'SIGNIN_START':
    case 'SIGNOUT_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'SIGNUP_SUCCESS':
    case 'SIGNIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'SIGNOUT_SUCCESS':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case 'AUTH_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const baseUrl = '/';

  // Check authentication status on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      checkAuth();
    }
  }, []);

  // Check authentication status
  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await fetch(`${getApiUrl()}/api/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const userData = await response.json();
          dispatch({
            type: 'SIGNIN_SUCCESS',
            payload: { user: userData },
          });
        } else {
          // Token is invalid, remove it
          localStorage.removeItem('token');
          dispatch({ type: 'SIGNOUT_SUCCESS' });
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        dispatch({ type: 'SIGNOUT_SUCCESS' });
      }
    }
  };

  // Get API URL based on environment
  const getApiUrl = () => {
    // Use the environment variable or default
    return process.env.REACT_APP_API_URL || 'http://localhost:8000';
  };

  // Get auth provider URL for external SSO (like Auth0)
  const getAuthUrl = () => {
    // This would be configured for external providers like Auth0
    // Example: return `https://${process.env.REACT_APP_AUTH0_DOMAIN}/authorize`;
    return null; // Currently not configured for external auth
  };

  // Handle external SSO login
  const handleExternalLogin = (provider) => {
    // This would redirect to external auth provider
    // Example for Auth0:
    // const authUrl = `https://${process.env.REACT_APP_AUTH0_DOMAIN}/authorize?...`;
    // window.location.href = authUrl;
    console.log(`External login with ${provider} not yet configured`);
  };

  // Signup function
  const signup = async (email, password, backgroundData) => {
    dispatch({ type: 'SIGNUP_START' });

    try {
      const response = await fetch(`${getApiUrl()}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          ...backgroundData
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Save token to localStorage
        localStorage.setItem('token', data.access_token);

        dispatch({
          type: 'SIGNUP_SUCCESS',
          payload: { user: data.user },
        });

        // Redirect to home page after successful signup
        window.location.href = baseUrl;
        return { success: true };
      } else {
        dispatch({
          type: 'AUTH_ERROR',
          payload: data.detail || 'Signup failed',
        });
        return { success: false, error: data.detail || 'Signup failed' };
      }
    } catch (error) {
      dispatch({
        type: 'AUTH_ERROR',
        payload: error.message || 'Network error',
      });
      return { success: false, error: error.message || 'Network error' };
    }
  };

  // Signin function
  const signin = async (email, password) => {
    dispatch({ type: 'SIGNIN_START' });

    try {
      const response = await fetch(`${getApiUrl()}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Save token to localStorage
        localStorage.setItem('token', data.access_token);

        dispatch({
          type: 'SIGNIN_SUCCESS',
          payload: { user: data.user },
        });

        return { success: true };
      } else {
        dispatch({
          type: 'AUTH_ERROR',
          payload: data.detail || 'Signin failed',
        });
        return { success: false, error: data.detail || 'Signin failed' };
      }
    } catch (error) {
      dispatch({
        type: 'AUTH_ERROR',
        payload: error.message || 'Network error',
      });
      return { success: false, error: error.message || 'Network error' };
    }
  };

  // Signout function
  const signout = async () => {
    dispatch({ type: 'SIGNOUT_START' });

    try {
      await fetch(`${getApiUrl()}/api/auth/signout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
          'Content-Type': 'application/json',
        },
      });

      // Remove token from localStorage
      localStorage.removeItem('token');

      dispatch({ type: 'SIGNOUT_SUCCESS' });

      // Redirect to home page after signout
      window.location.href = baseUrl;
    } catch (error) {
      console.error('Signout error:', error);
      // Even if the API call fails, still remove the token locally
      localStorage.removeItem('token');
      dispatch({ type: 'SIGNOUT_SUCCESS' });
    }
  };

  // Clear error function
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value = {
    ...state,
    signup,
    signin,
    signout,
    checkAuth,
    clearError,
    handleExternalLogin,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};