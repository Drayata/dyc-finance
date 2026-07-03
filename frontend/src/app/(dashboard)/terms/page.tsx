export default function TermsOfServicePage() {
  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <div className="card">
        <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-6">Terms of Service</h1>
        
        <div className="space-y-4 text-[var(--text-secondary)] leading-relaxed">
          <p>Last updated: {new Date().toLocaleDateString()}</p>
          
          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">1. Acceptance of Terms</h2>
          <p>
            By accessing or using MarketPulse AI, you agree to be bound by these Terms. If you disagree with any part of the terms, then you may not access the service.
          </p>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">2. Description of Service</h2>
          <p>
            MarketPulse AI provides users with access to a rich collection of resources, including various communications tools, search services, personalized content and market data analysis tools (the "Service"). You understand and agree that the Service is provided "AS-IS" and that MarketPulse AI assumes no responsibility for the timeliness, deletion, mis-delivery, or failure to store any user communications or personalization settings.
          </p>
          
          <div className="disclaimer-box mt-4">
            <strong>IMPORTANT DISCLAIMER:</strong> MarketPulse AI is an informational tool. We are not a broker-dealer or investment advisor. Our AI-generated signals are for educational and research purposes only.
          </div>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">3. User Conduct</h2>
          <p>
            You agree to use the Service only for lawful purposes. You are prohibited from violating or attempting to violate the security of the Service, including, without limitation, accessing data not intended for you or logging into a server or account which you are not authorized to access.
          </p>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">4. Termination</h2>
          <p>
            We may terminate or suspend access to our Service immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms.
          </p>
        </div>
      </div>
    </div>
  );
}
