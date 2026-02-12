import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center">
      <div className="text-center text-white">
        <h1 className="text-6xl font-bold mb-4">🦞</h1>
        <h2 className="text-4xl font-bold mb-2">Simon's Command Center</h2>
        <p className="text-xl mb-8 opacity-90">AI-Powered Task & Agent Management</p>
        
        <div className="space-y-4">
          <Link 
            href="/dashboard"
            className="inline-block bg-white text-blue-600 font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors"
          >
            Enter Dashboard
          </Link>
          
          <div className="mt-8 grid grid-cols-2 gap-4 text-sm opacity-80">
            <div>
              <h3 className="font-semibold">🤖 AI Agents</h3>
              <p>Svend, Anders & Content</p>
            </div>
            <div>
              <h3 className="font-semibold">🌐 Domains</h3>
              <p>Elkjøp, Affiliate, Personal</p>
            </div>
            <div>
              <h3 className="font-semibold">📊 Monitoring</h3>
              <p>5 Sites, 24/7 Uptime</p>
            </div>
            <div>
              <h3 className="font-semibold">🚀 Deployment</h3>
              <p>GitHub → SiteGround</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}