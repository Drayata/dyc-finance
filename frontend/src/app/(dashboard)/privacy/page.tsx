export default function PrivacyPolicyPage() {
  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <div className="card">
        <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-6">Privacy Policy</h1>
        
        <div className="space-y-4 text-[var(--text-secondary)] leading-relaxed">
          <p>Last updated: {new Date().toLocaleDateString()}</p>
          
          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">1. Information We Collect</h2>
          <p>
            We collect information you provide directly to us, such as when you create or modify your account, request on-demand services, contact customer support, or otherwise communicate with us. This information may include: name, email, encrypted passwords, and your configured watchlists and alerts.
          </p>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">2. How We Use Your Information</h2>
          <p>
            We may use the information we collect about you to:
          </p>
          <ul className="list-disc pl-5 space-y-1">
            <li>Provide, maintain, and improve our services, including the AI signal generation and alerting.</li>
            <li>Send you technical notices, updates, security alerts, and support and administrative messages.</li>
            <li>Respond to your comments, questions, and requests, and provide customer service.</li>
            <li>Monitor and analyze trends, usage, and activities in connection with our Services.</li>
          </ul>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">3. Data Security</h2>
          <p>
            We take reasonable measures to help protect information about you from loss, theft, misuse and unauthorized access, disclosure, alteration and destruction. Passwords are cryptographically hashed using standard security protocols.
          </p>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">4. Third-Party Services</h2>
          <p>
            Our platform integrates with third-party APIs (e.g., Alpha Vantage, CoinGecko) to retrieve financial data. We do not share your personal identification data with these providers.
          </p>
        </div>
      </div>
    </div>
  );
}
