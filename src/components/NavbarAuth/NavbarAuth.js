import React, { useState } from 'react';
import { useAuth } from '../../theme/AuthContext';
import styles from './NavbarAuth.module.css';

const NavbarAuth = () => {
  const { user, isAuthenticated, signout } = useAuth();
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
                  // Toggle dark/light mode - this would use Docusaurus theme context
                  console.log('Toggle theme');
                }}
              >
                🌙 Dark Mode
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
    // Not authenticated - show sign in/up buttons
    return (
      <div className={`navbar__auth-buttons ${styles.authButtons}`}>
        <a
          className="button button--secondary button--sm margin-right--sm"
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