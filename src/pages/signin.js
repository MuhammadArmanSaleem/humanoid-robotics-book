import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../theme/AuthContext';
import styles from '../components/NavbarAuth/NavbarAuth.module.css';

const SigninPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { signin } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      setError('Email and password are required');
      return;
    }

    setIsSubmitting(true);

    const result = await signin(email, password);

    if (result.success) {
      // Redirect to previous page or home page after successful signin
      const urlParams = new URLSearchParams(window.location.search);
      const from = urlParams.get('from') || '/';
      window.location.href = from;
    } else {
      setError(result.error || 'Signin failed');
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
                  <div className="form-group">
                    <label htmlFor="email">Email Address</label>
                    <input
                      type="email"
                      id="email"
                      className="form-control"
                      placeholder="Enter your email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <div className={styles.passwordWrapper}>
                      <input
                        type={showPassword ? 'text' : 'password'}
                        id="password"
                        className="form-control"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                      />
                      <button
                        type="button"
                        className={styles.passwordToggle}
                        onClick={() => setShowPassword(!showPassword)}
                        aria-label={showPassword ? 'Hide password' : 'Show password'}
                      >
                        {showPassword ? '👁️' : '👁️‍🗨️'}
                      </button>
                    </div>
                  </div>

                  <div className="form-group">
                    <button
                      type="submit"
                      className="button button--primary button--block"
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
                  <a href={`${baseUrl}signup`}>Sign up</a>
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