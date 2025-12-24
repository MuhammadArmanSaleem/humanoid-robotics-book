import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useAuth } from '../theme/AuthContext';
import styles from '../components/NavbarAuth/NavbarAuth.module.css';
import formStyles from './signin.module.css';

const SigninPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const { signin } = useAuth();

  // Validate email format
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // Real-time email validation
  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    if (value && !validateEmail(value)) {
      setEmailError('Please enter a valid email address');
    } else {
      setEmailError('');
    }
  };

  // Real-time password validation
  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);
    if (value && value.length < 6) {
      setPasswordError('Password must be at least 6 characters');
    } else {
      setPasswordError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setEmailError('');
    setPasswordError('');

    // Validate inputs
    if (!email) {
      setEmailError('Email is required');
      return;
    }

    if (!validateEmail(email)) {
      setEmailError('Please enter a valid email address');
      return;
    }

    if (!password) {
      setPasswordError('Password is required');
      return;
    }

    if (password.length < 6) {
      setPasswordError('Password must be at least 6 characters');
      return;
    }

    setIsSubmitting(true);

    const result = await signin(email, password);

    if (result.success) {
      // Clear any errors
      setError('');
      // Redirect to previous page or home page after successful signin
      const urlParams = new URLSearchParams(window.location.search);
      const from = urlParams.get('from') || '/';
      // Use setTimeout to ensure state is updated before redirect
      setTimeout(() => {
        window.location.href = from;
      }, 100);
    } else {
      setError(result.error || 'Signin failed. Please check your credentials and try again.');
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to access your personalized learning experience">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="card">
              <div className="card__header">
                <h2>Sign In to Your Account</h2>
                <p>Access your personalized learning experience</p>
              </div>
              <div className="card__body">
                {error && (
                  <div className="alert alert--danger" role="alert">
                    {error}
                  </div>
                )}
                <form onSubmit={handleSubmit}>
                  <div className={formStyles.formGroup}>
                    <label htmlFor="email">Email Address</label>
                    <input
                      type="email"
                      id="email"
                      className={`${formStyles.formControl} ${emailError ? formStyles.isInvalid : ''}`}
                      placeholder="Enter your email"
                      value={email}
                      onChange={handleEmailChange}
                      onBlur={handleEmailChange}
                      required
                    />
                    {emailError && (
                      <div className={formStyles.invalidFeedback}>
                        {emailError}
                      </div>
                    )}
                  </div>

                  <div className={formStyles.formGroup}>
                    <label htmlFor="password">Password</label>
                    <div className={formStyles.passwordWrapper}>
                      <input
                        type={showPassword ? 'text' : 'password'}
                        id="password"
                        className={`${formStyles.formControl} ${passwordError ? formStyles.isInvalid : ''}`}
                        placeholder="Enter your password"
                        value={password}
                        onChange={handlePasswordChange}
                        onBlur={handlePasswordChange}
                        required
                      />
                      {passwordError && (
                        <div className={formStyles.invalidFeedback}>
                          {passwordError}
                        </div>
                      )}
                      <button
                        type="button"
                        className={formStyles.passwordToggle}
                        onClick={() => setShowPassword(!showPassword)}
                        aria-label={showPassword ? 'Hide password' : 'Show password'}
                      >
                        {showPassword ? '👁️' : '👁️‍🗨️'}
                      </button>
                    </div>
                  </div>

                  <div className={formStyles.formGroup}>
                    <button
                      type="submit"
                      className={`${formStyles.button} ${formStyles.buttonPrimary}`}
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? 'Signing In...' : 'Sign In'}
                    </button>
                  </div>
                </form>
              </div>
              <div className="card__footer">
                <p>
                  Don't have an account?{' '}
                  <Link to="/signup">Sign up</Link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SigninPage;