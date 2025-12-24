import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics Textbook">
      <main style={{ padding: 'var(--spacing-xl) 0' }}>
        <div className="container padding-vert--lg">
          <div className="row">
            <div className="col col--8 col--offset-2">
              <h1 className="hero__title">{siteConfig.title}</h1>
              <p className="hero__subtitle">{siteConfig.tagline}</p>
              <div className="margin-top--lg" style={{ marginBottom: 'var(--spacing-lg)' }}>
                <p style={{ fontSize: 'var(--font-size-base)', marginBottom: 'var(--spacing-md)', color: 'var(--ifm-color-content)' }}>
                  Welcome to the Physical AI & Humanoid Robotics textbook.
                </p>
                <p style={{ fontSize: 'var(--font-size-base)', marginBottom: 'var(--spacing-md)', color: 'var(--ifm-color-content)' }}>
                  Use the navigation menu to access the textbook content or start reading below.
                </p>
              </div>
              <div className="margin-top--lg">
                <Link
                  className="button button--primary button--lg"
                  to="/docs/chapter-1-introduction-to-physical-ai/lesson-1-what-is-physical-ai">
                  Start Reading
                </Link>
                <Link
                  className="button button--secondary button--lg margin-left--md"
                  to="/signup">
                  Sign Up
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}