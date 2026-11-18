import { Link, Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

export default function Landing() {
  const { isAuthenticated } = useAuthStore();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">

      <div className="max-w-7xl mx-auto">

        <header className="flex items-center justify-between border-b border-slate-200 px-8 py-5">

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

        <section className="px-8 py-20 text-center">

          <h2 className="text-6xl font-extrabold leading-tight">
            AI Operations
            <br />
            Copilot
          </h2>

          <p className="mx-auto mt-8 max-w-3xl text-xl text-slate-600">
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
              className="rounded-lg border border-slate-300 px-8 py-4 text-lg text-slate-700 transition hover:bg-slate-900 hover:text-white"
            >
              Login
            </Link>

          </div>

        </section>

        <section className="grid gap-5 px-8 pb-20 md:grid-cols-2 lg:grid-cols-3">

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
    <div className="rounded-lg border border-slate-200 bg-white p-6">

      <h3 className="text-2xl font-semibold mb-4">
        {title}
      </h3>

      <p className="text-slate-600">
        {description}
      </p>

    </div>
  );
}