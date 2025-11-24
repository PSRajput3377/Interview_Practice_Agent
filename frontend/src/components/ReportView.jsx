export default function ReportView({ report, onBack }) {
  if (!report) return null;

  const final = report.final_summary;
  const scores = report.scores;

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <button
        onClick={onBack}
        className="mb-6 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg"
      >
        ← Back to Chat
      </button>

      <h1 className="text-3xl font-bold mb-4">Final Interview Report</h1>

      {/* Overall Score */}
      <div className="bg-gray-800 p-4 rounded-lg mb-6">
        <h2 className="text-xl font-semibold mb-2">Overall Score</h2>
        <p className="text-4xl font-bold">{final.overall_score.toFixed(2)} / 10</p>
      </div>

      {/* Scores */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        {Object.entries(final.averages).map(([key, val]) => (
          <div key={key} className="bg-gray-800 p-4 rounded-lg">
            <p className="text-lg font-semibold capitalize">{key}</p>
            <p className="text-2xl font-bold">{val.toFixed(1)}</p>
          </div>
        ))}
      </div>

      {/* Strengths */}
      <div className="bg-gray-800 p-4 rounded-lg mb-6">
        <h2 className="text-xl font-semibold mb-2">Top Strengths</h2>
        <ul className="list-disc ml-6">
          {final.top_strengths.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      {/* Weaknesses */}
      <div className="bg-gray-800 p-4 rounded-lg mb-6">
        <h2 className="text-xl font-semibold mb-2">Weaknesses</h2>
        <ul className="list-disc ml-6">
          {final.top_weaknesses.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      {/* Suggestions */}
      <div className="bg-gray-800 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Suggestions</h2>
        <ul className="list-disc ml-6">
          {final.top_suggestions.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

