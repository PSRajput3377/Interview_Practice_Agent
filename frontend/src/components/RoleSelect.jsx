export default function RoleSelect({ onSelect }) {
  const roles = [
    { id: "software_engineer", label: "Software Engineer" },
    { id: "ml_engineer", label: "ML Engineer" },
    { id: "data_analyst", label: "Data Analyst" },
    { id: "frontend_developer", label: "Frontend Developer" },
    { id: "hr_interview", label: "HR Interview" },
  ];

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-6">Choose Interview Role</h1>

      <div className="space-y-4 w-full max-w-md">
        {roles.map((role) => (
          <button
            key={role.id}
            onClick={() => onSelect(role.id)}
            className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-lg font-medium"
          >
            {role.label}
          </button>
        ))}
      </div>
    </div>
  );
}

