import { Link, Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

export default function Landing() {
  const { isAuthenticated } = useAuthStore();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-blue-900 to-slate-800 text-white">

      <div className="max-w-7xl mx-auto">

        {/* Navbar */}

        <header className="flex justify-between items-center p-8">

          <h1 className="text-3xl font-bold">
            AI Operations Copilot
          </h1>

          <div className="space-x-4">

            <Link
              to="/login"
              className="px-5 py-2 rounded-lg hover:bg-white/10"
            >
              Login
            </Link>

            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded-lg"
            >
              Register
            </Link>

          </div>

        </header>

        {/* Hero */}

        <section className="text-center py-24">

          <h2 className="text-6xl font-extrabold leading-tight">
            AI Operations
            <br />
            Copilot
          </h2>

          <p className="mt-8 text-xl text-gray-300 max-w-3xl mx-auto">
            Manage business operations with AI-powered chat,
            SQL generation, PDF and Excel analysis,
            analytics dashboards and intelligent reporting.
          </p>

          <div className="mt-12 space-x-5">

            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-xl text-lg font-semibold"
            >
              Get Started
            </Link>

            <Link
              to="/login"
              className="border border-white px-8 py-4 rounded-xl text-lg hover:bg-white hover:text-black transition"
            >
              Login
            </Link>

          </div>

        </section>

        {/* Features */}

        <section className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 px-8 pb-24">

          <Feature
            title="AI Chat"
            description="Ask business questions in natural language."
          />

          <Feature
            title="SQL Generator"
            description="Convert business questions into SQL instantly."
          />

          <Feature
            title="PDF Analyzer"
            description="Upload PDFs and receive AI-generated summaries."
          />

          <Feature
            title="Excel Analyzer"
            description="Analyze Excel workbooks using AI."
          />

          <Feature
            title="Analytics"
            description="Monitor users, uploads and AI activity."
          />

          <Feature
            title="Reports"
            description="Generate operational reports with one click."
          />

        </section>

      </div>

    </div>
  );
}

function Feature({ title, description }) {
  return (
    <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/10">

      <h3 className="text-2xl font-semibold mb-4">
        {title}
      </h3>

      <p className="text-gray-300">
        {description}
      </p>

    </div>
  );
}