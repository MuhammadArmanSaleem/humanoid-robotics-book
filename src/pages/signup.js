import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../theme/AuthContext';
import styles from '../components/NavbarAuth/NavbarAuth.module.css';

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

  const { signup } = useAuth();

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

  const validateForm = () => {
    if (!email || !password || !confirmPassword) {
      setError('All fields are required');
      return false;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return false;
    }

    if (!programmingLanguages.length) {
      setError('Please select at least one programming language');
      return false;
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email address');
      return false;
    }

    setError('');
    return true;
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
      window.location.href = '/';
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
                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <div className={styles.passwordWrapper}>
                      <input
                        type={showConfirmPassword ? 'text' : 'password'}
                        id="confirmPassword"
                        className="form-control"
                        placeholder="Confirm your password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                      />
                      <button
                        type="button"
                        className={styles.passwordToggle}
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                      >
                        {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                      </button>
                    </div>
                  </div>

                  <div className="form-group">
                    <label htmlFor="softwareExperience">Software Experience</label>
                    <select
                      id="softwareExperience"
                      className="form-control"
                      value={softwareExperience}
                      onChange={(e) => setSoftwareExperience(e.target.value)}
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="hardwareExperience">Hardware Experience</label>
                    <select
                      id="hardwareExperience"
                      className="form-control"
                      value={hardwareExperience}
                      onChange={(e) => setHardwareExperience(e.target.value)}
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Programming Languages</label>
                    <div className="checkbox-group">
                      {programmingLanguageOptions.map((lang) => (
                        <div key={lang} className="form-check">
                          <input
                            type="checkbox"
                            id={`lang-${lang}`}
                            className="form-check-input"
                            checked={programmingLanguages.includes(lang)}
                            onChange={() => handleLanguageChange(lang)}
                          />
                          <label htmlFor={`lang-${lang}`} className="form-check-label">
                            {lang}
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="form-group">
                    <label htmlFor="roboticsBackground">Robotics Background (Optional)</label>
                    <textarea
                      id="roboticsBackground"
                      className="form-control"
                      placeholder="Describe your robotics background or experience"
                      value={roboticsBackground}
                      onChange={(e) => setRoboticsBackground(e.target.value)}
                      rows={3}
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="learningGoals">Learning Goals (Optional)</label>
                    <textarea
                      id="learningGoals"
                      className="form-control"
                      placeholder="What do you hope to learn?"
                      value={learningGoals}
                      onChange={(e) => setLearningGoals(e.target.value)}
                      rows={3}
                    />
                  </div>

                  <div className="form-group">
                    <button
                      type="submit"
                      className="button button--primary button--block"
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
                  <a href={`${baseUrl}signin`}>Sign in</a>
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