import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useAuth } from '../theme/AuthContext';
import styles from '../components/NavbarAuth/NavbarAuth.module.css';
import formStyles from './signup.module.css';

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [softwareExperience, setSoftwareExperience] = useState('beginner');
  const [hardwareExperience, setHardwareExperience] = useState('beginner');
  const [programmingLanguages, setProgrammingLanguages] = useState([]);
  const [roboticsBackground, setRoboticsBackground] = useState('');
  const [learningGoals, setLearningGoals] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [confirmPasswordError, setConfirmPasswordError] = useState('');

  const { signup } = useAuth();

  // Validate email format
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const programmingLanguageOptions = [
    'Python', 'C++', 'JavaScript', 'C', 'Java', 'ROS', 'MATLAB', 'Rust', 'Go', 'Other'
  ];

  const handleLanguageChange = (lang) => {
    if (programmingLanguages.includes(lang)) {
      setProgrammingLanguages(programmingLanguages.filter(l => l !== lang));
    } else {
      setProgrammingLanguages([...programmingLanguages, lang]);
    }
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
    // Also check confirm password if it's already filled
    if (confirmPassword && value !== confirmPassword) {
      setConfirmPasswordError('Passwords do not match');
    } else if (confirmPassword) {
      setConfirmPasswordError('');
    }
  };

  // Real-time confirm password validation
  const handleConfirmPasswordChange = (e) => {
    const value = e.target.value;
    setConfirmPassword(value);
    if (value && value !== password) {
      setConfirmPasswordError('Passwords do not match');
    } else {
      setConfirmPasswordError('');
    }
  };

  const validateForm = () => {
    let isValid = true;
    setError('');
    setEmailError('');
    setPasswordError('');
    setConfirmPasswordError('');

    if (!email) {
      setEmailError('Email is required');
      isValid = false;
    } else if (!validateEmail(email)) {
      setEmailError('Please enter a valid email address');
      isValid = false;
    }

    if (!password) {
      setPasswordError('Password is required');
      isValid = false;
    } else if (password.length < 6) {
      setPasswordError('Password must be at least 6 characters');
      isValid = false;
    }

    if (!confirmPassword) {
      setConfirmPasswordError('Please confirm your password');
      isValid = false;
    } else if (password !== confirmPassword) {
      setConfirmPasswordError('Passwords do not match');
      isValid = false;
    }

    if (!programmingLanguages.length) {
      setError('Please select at least one programming language');
      isValid = false;
    }

    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    const backgroundData = {
      software_experience: softwareExperience,
      hardware_experience: hardwareExperience,
      programming_languages: programmingLanguages,
      robotics_background: roboticsBackground,
      learning_goals: learningGoals,
    };

    const result = await signup(email, password, backgroundData);

    if (result.success) {
      // Redirect to home page after successful signup
      // Use setTimeout to ensure state is updated before redirect
      setTimeout(() => {
        window.location.href = '/';
      }, 100);
    } else {
      setError(result.error || 'Signup failed');
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create an account to personalize your learning experience">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="card">
              <div className="card__header">
                <h2>Create Your Account</h2>
                <p>Join to get personalized content based on your background</p>
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
                      <button
                        type="button"
                        className={formStyles.passwordToggle}
                        onClick={() => setShowPassword(!showPassword)}
                        aria-label={showPassword ? 'Hide password' : 'Show password'}
                      >
                        {showPassword ? '👁️' : '👁️‍🗨️'}
                      </button>
                    </div>
                    {passwordError && (
                      <div className={formStyles.invalidFeedback}>
                        {passwordError}
                      </div>
                    )}
                  </div>

                  <div className={formStyles.formGroup}>
                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <div className={formStyles.passwordWrapper}>
                      <input
                        type={showConfirmPassword ? 'text' : 'password'}
                        id="confirmPassword"
                        className={`${formStyles.formControl} ${confirmPasswordError ? formStyles.isInvalid : ''}`}
                        placeholder="Confirm your password"
                        value={confirmPassword}
                        onChange={handleConfirmPasswordChange}
                        onBlur={handleConfirmPasswordChange}
                        required
                      />
                      <button
                        type="button"
                        className={formStyles.passwordToggle}
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                      >
                        {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                      </button>
                    </div>
                    {confirmPasswordError && (
                      <div className={formStyles.invalidFeedback}>
                        {confirmPasswordError}
                      </div>
                    )}
                  </div>

                  <div className={formStyles.formGroup}>
                    <label htmlFor="softwareExperience">Software Experience</label>
                    <select
                      id="softwareExperience"
                      className={formStyles.formControl}
                      value={softwareExperience}
                      onChange={(e) => setSoftwareExperience(e.target.value)}
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  <div className={formStyles.formGroup}>
                    <label htmlFor="hardwareExperience">Hardware Experience</label>
                    <select
                      id="hardwareExperience"
                      className={formStyles.formControl}
                      value={hardwareExperience}
                      onChange={(e) => setHardwareExperience(e.target.value)}
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  <div className={formStyles.formGroup}>
                    <label>Programming Languages</label>
                    <div className={formStyles.checkboxGroup}>
                      {programmingLanguageOptions.map((lang) => (
                        <div key={lang} className={formStyles.formCheck}>
                          <input
                            type="checkbox"
                            id={`lang-${lang}`}
                            className={formStyles.formCheckInput}
                            checked={programmingLanguages.includes(lang)}
                            onChange={() => handleLanguageChange(lang)}
                          />
                          <label htmlFor={`lang-${lang}`} className={formStyles.formCheckLabel}>
                            {lang}
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className={formStyles.formGroup}>
                    <label htmlFor="roboticsBackground">Robotics Background (Optional)</label>
                    <textarea
                      id="roboticsBackground"
                      className={formStyles.formControl}
                      placeholder="Describe your robotics background or experience"
                      value={roboticsBackground}
                      onChange={(e) => setRoboticsBackground(e.target.value)}
                      rows={3}
                    />
                  </div>

                  <div className={formStyles.formGroup}>
                    <label htmlFor="learningGoals">Learning Goals (Optional)</label>
                    <textarea
                      id="learningGoals"
                      className={formStyles.formControl}
                      placeholder="What do you hope to learn?"
                      value={learningGoals}
                      onChange={(e) => setLearningGoals(e.target.value)}
                      rows={3}
                    />
                  </div>

                  <div className={formStyles.formGroup}>
                    <button
                      type="submit"
                      className={`${formStyles.button} ${formStyles.buttonPrimary}`}
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? 'Creating Account...' : 'Sign Up'}
                    </button>
                  </div>
                </form>
              </div>
              <div className="card__footer">
                <p>
                  Already have an account?{' '}
                  <Link to="/signin">Sign in</Link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage;