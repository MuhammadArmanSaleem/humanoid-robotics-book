import React, { useState } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import { useAuth } from '../../theme/AuthContext';
import styles from './NavbarAuth.module.css';

const NavbarAuth = () => {
  const { user, isAuthenticated, signout } = useAuth();
  const { colorMode, setColorMode } = useColorMode();
  const [showDropdown, setShowDropdown] = useState(false);

  const handleSignout = async () => {
    await signout();
    setShowDropdown(false);
  };

  const handleNav = (path) => {
    window.location.href = path;
    setShowDropdown(false);
  };

  if (isAuthenticated && user) {
    // Authenticated user dropdown
    return (
      <div className={`navbar__item dropdown dropdown--hoverable dropdown--right ${styles.navbarItem}`}>
        <a
          className={`navbar__link ${styles.navbarLink}`}
          href="#"
          role="button"
          onClick={(e) => {
            e.preventDefault();
            setShowDropdown(!showDropdown);
          }}
          aria-expanded={showDropdown}
        >
          <span className={styles.navbarUserName}>
            {user.email.split('@')[0]}
            <span className={styles.navbarAvatar}>👤</span>
          </span>
        </a>

        {showDropdown && (
          <ul className={`dropdown__menu ${styles.dropdownMenu}`}>
            <li>
              <a className={`dropdown__link ${styles.dropdownLink}`} href="#" onClick={(e) => {
                e.preventDefault();
                handleNav('/profile');
              }}>
                Profile
              </a>
            </li>
            <li>
              <a
                className={`dropdown__link ${styles.dropdownLink}`}
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  // Toggle language - this would be implemented with i18n
                  console.log('Toggle language');
                }}
              >
                🇵🇰 اردو
              </a>
            </li>
            <li>
              <a
                className={`dropdown__link ${styles.dropdownLink}`}
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  setColorMode(colorMode === 'dark' ? 'light' : 'dark');
                }}
              >
                {colorMode === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode'}
              </a>
            </li>
            <li>
              <a
                className={`dropdown__link ${styles.dropdownLink}`}
                href="https://github.com/your-repo"
                target="_blank"
                rel="noopener noreferrer"
              >
                🐙 GitHub
              </a>
            </li>
            <li className="dropdown__divider"></li>
            <li>
              <a
                className={`dropdown__link dropdown__link--danger ${styles.dropdownLink} ${styles.dropdownLinkDanger}`}
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  handleSignout();
                }}
              >
                Sign Out
              </a>
            </li>
          </ul>
        )}
      </div>
    );
  } else {
    // Not authenticated - show sign in/up buttons and theme toggle
    return (
      <div className={styles.authButtons}>
        <button
          className={styles.themeToggle}
          onClick={() => setColorMode(colorMode === 'dark' ? 'light' : 'dark')}
          aria-label={`Switch to ${colorMode === 'dark' ? 'light' : 'dark'} mode`}
          title={`Switch to ${colorMode === 'dark' ? 'light' : 'dark'} mode`}
        >
          {colorMode === 'dark' ? '☀️' : '🌙'}
        </button>
        <a
          className="button button--secondary button--sm"
          href="/signin"
        >
          Sign In
        </a>
        <a
          className="button button--primary button--sm"
          href="/signup"
        >
          Sign Up
        </a>
      </div>
    );
  }
};

export default NavbarAuth;