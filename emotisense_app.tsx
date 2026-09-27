import React, { useState } from 'react';
import { Settings, Bell, User, PlayCircle, Upload, Video, Camera, Heart, Lock, Database, Trash2, UserCheck, Brain, TrendingUp, Smartphone } from 'lucide-react';

export default function EmotiSense() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [analysisMethod, setAnalysisMethod] = useState(null);

  const renderHeader = () => (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold">EmotiSense</h1>
            <p className="text-xs text-gray-500">Mental Health Insights</p>
          </div>
        </div>
        <nav className="flex items-center gap-8">
          <button onClick={() => setCurrentPage('dashboard')} className={`font-medium ${currentPage === 'dashboard' ? 'text-blue-600' : 'text-gray-700'}`}>Dashboard</button>
          <button onClick={() => setCurrentPage('history')} className={`font-medium ${currentPage === 'history' ? 'text-blue-600' : 'text-gray-700'}`}>History</button>
          <button onClick={() => setCurrentPage('insights')} className={`font-medium ${currentPage === 'insights' ? 'text-blue-600' : 'text-gray-700'}`}>Insights</button>
          <button className="text-gray-700 font-medium">Resources</button>
          <button className="text-gray-700 font-medium">Support</button>
        </nav>
        <div className="flex items-center gap-4">
          <Bell className="w-5 h-5 text-gray-600 cursor-pointer" />
          <Settings className="w-5 h-5 text-gray-600 cursor-pointer" />
          <User className="w-5 h-5 text-gray-600 cursor-pointer" />
        </div>
      </div>
    </header>
  );

  const renderHome = () => (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <div className="grid grid-cols-2 gap-12 items-center">
        <div>
          <div className="flex items-center gap-2 mb-6">
            <Lock className="w-5 h-5 text-gray-700" />
            <span className="text-sm font-semibold text-gray-700">HIPAA Compliant & Secure</span>
          </div>
          <h2 className="text-5xl font-bold mb-6 leading-tight">Understand Your Emotional Health Journey</h2>
          <p className="text-gray-600 text-lg mb-8">Advanced facial expression recognition technology provides real-time insights into your emotional well-being. Upload images, videos, or use live camera analysis for personalized mental health tracking.</p>
          <div className="flex gap-4">
            <button onClick={() => setCurrentPage('analysis')} className="px-8 py-3 bg-black text-white rounded-lg font-medium hover:bg-gray-900">Start Analysis →</button>
            <button className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 flex items-center gap-2">
              <PlayCircle className="w-5 h-5" />
              Watch Demo
            </button>
          </div>
          <div className="flex gap-8 mt-8 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Lock className="w-4 h-4" />
              End-to-end encrypted
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Real-time analysis
            </div>
            <div className="flex items-center gap-2">
              <Brain className="w-4 h-4" />
              Detailed insights
            </div>
          </div>
        </div>
        <div className="bg-gray-100 rounded-lg h-96 flex flex-col items-center justify-center">
          <div className="text-center">
            <div className="w-24 h-24 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-4xl">😊</span>
            </div>
            <p className="text-gray-600 font-medium">Interactive Demo Interface</p>
          </div>
          <div className="mt-auto w-full bg-white border-t border-gray-200 p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Live Analysis</span>
              <span className="text-sm font-semibold">99.2% accuracy</span>
            </div>
            <div className="flex items-center gap-2">
              <Heart className="w-5 h-5 text-gray-400" />
              <span className="text-gray-600">Wellness Score: 8.7/10</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAnalysisSelection = () => (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold mb-4">Choose Your Analysis Method</h2>
        <p className="text-gray-600 text-lg">Select from three convenient options to analyze your facial expressions and gain insights into your emotional state</p>
      </div>
      <div className="grid grid-cols-3 gap-6">
        {[
          {
            icon: Upload,
            title: 'Upload Image',
            desc: 'Upload a photo from your device for instant facial expression analysis. Supports JPEG, PNG, and WebP formats up to 10MB.',
            features: ['Instant results in under 3 seconds', 'Multiple face detection', 'Emotion confidence scores'],
            btn: 'Select Image'
          },
          {
            icon: Video,
            title: 'Upload Video',
            desc: 'Upload a video file to analyze emotional changes over time. Get comprehensive timeline analysis and mood patterns.',
            features: ['Timeline emotion tracking', 'Mood pattern analysis', 'Up to 5 minutes duration'],
            btn: 'Select Video'
          },
          {
            icon: Camera,
            title: 'Live Camera',
            desc: 'Use your device camera for real-time emotion analysis. Perfect for meditation sessions, mood tracking, and live insights.',
            features: ['Real-time processing', 'Live emotion graphs', 'Session recording option'],
            btn: 'Start Camera'
          }
        ].map((method, idx) => (
          <div key={idx} className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg transition">
            <div className="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
              <method.icon className="w-8 h-8 text-gray-700" />
            </div>
            <h3 className="text-2xl font-bold mb-3">{method.title}</h3>
            <p className="text-gray-600 text-sm mb-4">{method.desc}</p>
            <ul className="space-y-2 mb-6">
              {method.features.map((f, i) => (
                <li key={i} className="flex items-center gap-3 text-sm text-gray-700">
                  <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  {f}
                </li>
              ))}
            </ul>
            <button onClick={() => setCurrentPage('liveanalysis')} className="w-full py-3 bg-black text-white rounded-lg font-medium hover:bg-gray-900 transition">
              {method.btn}
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderLiveAnalysis = () => (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <h2 className="text-4xl font-bold text-center mb-2">Real-Time Analysis Dashboard</h2>
      <p className="text-center text-gray-600 mb-8">Live emotion detection with comprehensive insights and visual feedback</p>
      
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <div className="bg-gray-100 rounded-lg h-96 flex flex-col items-center justify-center">
            <div className="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center mb-4">
              <User className="w-10 h-10 text-gray-600" />
            </div>
            <p className="text-gray-600">Camera Preview / Analysis Area</p>
            <p className="text-sm text-gray-500">Select an input method to begin analysis</p>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mt-6">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <p className="text-gray-600 text-sm">Current Emotion</p>
              <h3 className="text-3xl font-bold">Happy</h3>
              <p className="text-gray-500 text-sm">Confidence: 87.3%</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <p className="text-gray-600 text-sm">Wellness Score</p>
              <h3 className="text-3xl font-bold">8.2<span className="text-lg">/10</span></h3>
              <p className="text-gray-500 text-sm">Out of 10</p>
            </div>
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <h3 className="font-bold mb-4">Emotion Breakdown</h3>
            {[
              { emotion: 'Happy', pct: 87 },
              { emotion: 'Neutral', pct: 8 },
              { emotion: 'Surprised', pct: 3 },
              { emotion: 'Sad', pct: 2 }
            ].map((e, i) => (
              <div key={i} className="mb-3">
                <div className="flex justify-between text-sm mb-1">
                  <span>{e.emotion}</span>
                  <span className="font-semibold">{e.pct}%</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-gray-400 rounded-full" style={{width: `${e.pct}%`}}></div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <h3 className="font-bold mb-4">Session Stats</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span className="text-gray-600">Duration</span><span className="font-semibold">2:34</span></div>
              <div className="flex justify-between"><span className="text-gray-600">Frames Analyzed</span><span className="font-semibold">154</span></div>
              <div className="flex justify-between"><span className="text-gray-600">Average Confidence</span><span className="font-semibold">91.2%</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderPrivacy = () => (
    <div className="bg-gray-900 text-white py-16">
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-4xl font-bold text-center mb-2">Your Data, Your Control</h2>
        <p className="text-center text-gray-300 mb-12">We prioritize your privacy with end-to-end encryption, local processing, and complete data transparency</p>
        
        <div className="grid grid-cols-4 gap-6 mb-12">
          {[
            { icon: Lock, title: 'End-to-End Encryption', desc: 'All data is encrypted during transmission and storage using AES-256 encryption standards.' },
            { icon: Database, title: 'Local Processing', desc: 'Facial analysis happens on your device when possible, minimizing data transmission.' },
            { icon: Trash2, title: 'Auto-Delete', desc: 'Images and videos are automatically deleted after analysis unless you choose to save them.' },
            { icon: UserCheck, title: 'HIPAA Compliant', desc: 'Full compliance with healthcare privacy regulations and data protection laws.' }
          ].map((item, i) => (
            <div key={i} className="text-center">
              <div className="w-16 h-16 bg-gray-800 rounded-lg flex items-center justify-center mx-auto mb-4">
                <item.icon className="w-8 h-8" />
              </div>
              <h3 className="font-bold mb-2">{item.title}</h3>
              <p className="text-sm text-gray-300">{item.desc}</p>
            </div>
          ))}
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-bold mb-4">Data Transparency Dashboard</h3>
            <p className="text-gray-300 mb-4">View exactly what data we collect, how it's used, and manage your privacy preferences at any time.</p>
            <button className="px-6 py-2 bg-white text-black rounded font-medium hover:bg-gray-100">View Privacy Dashboard</button>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-bold mb-4">Data Collection Status</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span>Facial Analysis</span><span className="text-green-400">Active</span></div>
              <div className="flex justify-between"><span>Data Storage</span><span className="text-yellow-400">Temporary</span></div>
              <div className="flex justify-between"><span>Third-party Sharing</span><span className="text-red-400">Disabled</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderFeatures = () => (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <h2 className="text-4xl font-bold text-center mb-2">Advanced Features</h2>
      <p className="text-center text-gray-600 mb-12">Cutting-edge technology meets user-friendly design for comprehensive emotional analysis</p>
      
      <div className="grid grid-cols-3 gap-6">
        {[
          { icon: Brain, title: 'AI-Powered Analysis', desc: 'Advanced machine learning algorithms trained on diverse datasets provide accurate emotion recognition with 99.2% precision.', features: ['7 core emotions detected', 'Micro-expression analysis', 'Cultural adaptation'] },
          { icon: TrendingUp, title: 'Real-Time Graphs', desc: 'Dynamic visualization of emotional states with interactive charts, timelines, and comparative analysis tools.', features: ['Live emotion tracking', 'Historical comparisons', 'Export capabilities'] },
          { icon: Smartphone, title: 'Cross-Platform', desc: 'Seamless experience across desktop, tablet, and mobile devices with cloud synchronization and offline capabilities.', features: ['Responsive design', 'Cloud sync', 'Offline mode'] }
        ].map((feat, i) => (
          <div key={i} className="bg-white border border-gray-200 rounded-xl p-6">
            <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
              <feat.icon className="w-6 h-6 text-gray-700" />
            </div>
            <h3 className="text-xl font-bold mb-2">{feat.title}</h3>
            <p className="text-gray-600 text-sm mb-4">{feat.desc}</p>
            <ul className="space-y-2">
              {feat.features.map((f, idx) => (
                <li key={idx} className="flex items-center gap-2 text-sm">
                  <span className="w-1 h-1 bg-green-500 rounded-full"></span>
                  {f}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );

  const renderHistory = () => (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <h2 className="text-3xl font-bold mb-8">Analysis History</h2>
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Date</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Type</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Emotion</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Confidence</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Wellness Score</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Action</th>
            </tr>
          </thead>
          <tbody>
            {[
              { date: 'Oct 10, 2025', type: 'Live Camera', emotion: 'Happy', conf: '87.3%', wellness: '8.2' },
              { date: 'Oct 9, 2025', type: 'Video Upload', emotion: 'Neutral', conf: '92.1%', wellness: '7.8' },
              { date: 'Oct 8, 2025', type: 'Image Upload', emotion: 'Happy', conf: '95.4%', wellness: '8.5' },
              { date: 'Oct 7, 2025', type: 'Live Camera', emotion: 'Surprised', conf: '78.2%', wellness: '7.2' },
              { date: 'Oct 6, 2025', type: 'Video Upload', emotion: 'Calm', conf: '88.9%', wellness: '8.7' },
            ].map((record, i) => (
              <tr key={i} className="border-b border-gray-200 hover:bg-gray-50">
                <td className="px-6 py-4 text-sm text-gray-700">{record.date}</td>
                <td className="px-6 py-4 text-sm text-gray-700">{record.type}</td>
                <td className="px-6 py-4 text-sm text-gray-700">{record.emotion}</td>
                <td className="px-6 py-4 text-sm text-gray-700">{record.conf}</td>
                <td className="px-6 py-4 text-sm text-gray-700">{record.wellness}/10</td>
                <td className="px-6 py-4 text-sm"><button className="text-blue-600 hover:text-blue-800 font-medium">View</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderInsights = () => (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <h2 className="text-3xl font-bold mb-8">Emotional Insights</h2>
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-xl font-bold mb-4">Emotion Trends (Last 7 Days)</h3>
          <div className="space-y-4">
            {[
              { emotion: 'Happy', trend: 65 },
              { emotion: 'Calm', trend: 58 },
              { emotion: 'Neutral', trend: 42 },
              { emotion: 'Anxious', trend: 28 },
            ].map((e, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-2">
                  <span className="font-medium">{e.emotion}</span>
                  <span className="text-gray-600">{e.trend}%</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full">
                  <div className="h-full bg-blue-500 rounded-full" style={{width: `${e.trend}%`}}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-xl font-bold mb-4">Weekly Summary</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Average Wellness Score</span>
              <span className="text-2xl font-bold">8.2/10</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Most Common Emotion</span>
              <span className="font-semibold">Happy</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Analysis Sessions</span>
              <span className="font-semibold">12</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total Duration</span>
              <span className="font-semibold">45m 23s</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-white">
      {renderHeader()}
      
      {currentPage === 'dashboard' && renderHome()}
      {currentPage === 'analysis' && renderAnalysisSelection()}
      {currentPage === 'liveanalysis' && renderLiveAnalysis()}
      {currentPage === 'history' && renderHistory()}
      {currentPage === 'insights' && renderInsights()}
      
      {currentPage === 'dashboard' && (
        <>
          {renderPrivacy()}
          {renderFeatures()}
        </>
      )}
    </div>
  );
}