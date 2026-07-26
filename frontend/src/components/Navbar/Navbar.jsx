function Navbar() {
  return (
    <nav className="bg-slate-900 shadow-lg border-b border-slate-800">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-8 h-20">

        {/* Logo */}
        <div className="flex items-center gap-3">

          <div className="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center text-2xl">
            🛡️
          </div>

          <div>
            <h1 className="text-white text-2xl font-bold">
              AutoSecAI
            </h1>

            <p className="text-slate-400 text-sm">
              Autonomous Pull Request Review
            </p>
          </div>

        </div>

        {/* Navigation */}

        <div className="flex items-center gap-10">

          <button className="text-slate-300 hover:text-white transition">
            Dashboard
          </button>

          <button className="text-slate-300 hover:text-white transition">
            Reports
          </button>

          <button className="text-slate-300 hover:text-white transition">
            Settings
          </button>

          <button className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg transition">
            Login
          </button>

        </div>

      </div>
    </nav>
  );
}

export default Navbar;