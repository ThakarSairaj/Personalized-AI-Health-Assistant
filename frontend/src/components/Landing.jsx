import { useNavigate } from "react-router-dom";
import "./Landing.css";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing">

      {/* NAVBAR */}
      <header className="navbar">
        <div className="logo">MediAssist</div>

        <div className="nav-buttons">
          <button
            className="btn-outline"
            onClick={() => navigate("/login")}
          >
            Login
          </button>

          <button
            className="btn-primary"
            onClick={() => navigate("/register")}
          >
            Sign Up
          </button>
        </div>
      </header>

      {/* HERO */}
      <section className="hero">
        <div className="hero-content">
          <h1>Your AI-Powered Health Companion</h1>

          <p>
            Instant medical answers, history-aware guidance and personalized
            health insights — all in one secure platform.
          </p>

          <div className="hero-buttons">
            <button
              className="btn-primary large"
              onClick={() => navigate("/register")}
            >
              Get Started Free
            </button>

            <button
              className="btn-light large"
              onClick={() => navigate("/login")}
            >
              Login
            </button>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="features">
        <h2>Features that empower your health</h2>

        <div className="feature-grid">
          <div className="feature-card">
            <span>💬</span>
            <h3>Smart Health Chat</h3>
            <p>AI Doctor available 24/7 for guidance</p>
          </div>

          <div className="feature-card">
            <span>📁</span>
            <h3>History-Aware Answers</h3>
            <p>Personalized insights based on records</p>
          </div>

          <div className="feature-card">
            <span>📊</span>
            <h3>Easy Tracking</h3>
            <p>Monitor symptoms & improvements</p>
          </div>

          <div className="feature-card">
            <span>🔒</span>
            <h3>Secure & Private</h3>
            <p>End-to-end encrypted protection</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta">
        <h2>Ready to take control of your health?</h2>

        <button
          className="btn-gold"
          onClick={() => navigate("/register")}
        >
          Start Free Today
        </button>
      </section>

      {/* FOOTER */}
      <footer>
        © 2026 MediAssist. All rights reserved.
      </footer>

    </div>
  );
}
