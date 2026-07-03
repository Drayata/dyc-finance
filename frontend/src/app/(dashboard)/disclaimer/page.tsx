export default function DisclaimerPage() {
  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <div className="card">
        <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-6">Disclaimer</h1>
        
        <div className="space-y-4 text-[var(--text-secondary)] leading-relaxed">
          <p>
            <strong>MarketPulse AI is an informational and educational tool, not a licensed investment adviser.</strong>
          </p>
          
          <p>
            The content, signals, sentiment analysis, and data provided on MarketPulse AI (the "Platform") are for informational purposes only. Nothing contained on our Platform constitutes a solicitation, recommendation, endorsement, or offer by MarketPulse AI or any third-party service provider to buy or sell any securities or other financial instruments in this or in in any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such jurisdiction.
          </p>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">No Investment Advice</h2>
          <p>
            All content on this site is information of a general nature and does not address the circumstances of any particular individual or entity. You alone assume the sole responsibility of evaluating the merits and risks associated with the use of any information or other content on the Platform before making any decisions based on such information or other content.
          </p>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">Investment Risks</h2>
          <p>
            There are risks associated with investing in securities and cryptocurrencies. Investing in stocks, bonds, exchange traded funds, mutual funds, cryptocurrencies, and money market funds involve risk of loss. Loss of principal is possible. Some high-risk investments may use leverage, which will accentuate gains & losses.
          </p>

          <h2 className="text-lg font-semibold text-[var(--text-primary)] mt-6 mb-2">Data Accuracy</h2>
          <p>
            While we strive to provide accurate and up-to-date information through our API integrations (such as Alpha Vantage, CoinGecko, and NewsAPI), MarketPulse AI makes no warranties or representations as to the accuracy, completeness, or timeliness of the information provided on this platform. The AI-generated signals are based on historical data and heuristic models, which are subject to error and do not guarantee future performance.
          </p>
        </div>
      </div>
    </div>
  );
}
