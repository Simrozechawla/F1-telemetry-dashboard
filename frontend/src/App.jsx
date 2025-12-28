import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const MAX_SPEED = 330;

export default function App() {
  const [telemetry, setTelemetry] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/telemetry");
        const data = await res.json();

        setTelemetry(data);

        const visualSpeed =
          data.avg_speed + (Math.random() * 6 - 3);

        setHistory((prev) =>
          [...prev, { speed: Math.max(0, visualSpeed) }].slice(-50)
        );
      } catch (err) {
        console.error("Fetch failed", err);
      }
    }, 500);

    return () => clearInterval(interval);
  }, []);

  if (!telemetry) {
    return (
      <div className="h-screen bg-black flex items-center justify-center text-white">
        Loading telemetry…
      </div>
    );
  }

  /* ---------- SPEED ARC ---------- */
  const speedPercent = Math.min(telemetry.avg_speed / MAX_SPEED, 1);
  const arcLength = 440;
  const arcOffset = arcLength * (1 - speedPercent);

  const speedColor =
    telemetry.avg_speed < 200
      ? "#22c55e"
      : telemetry.avg_speed < 280
      ? "#eab308"
      : "#ef4444";

  // --- DRIVER BEHAVIOR DISPLAY MAPPING (SAFE) ---
  const behaviorLabelMap = {
  SMOOTH: "🟢 SMOOTH OPERATOR",
  AGGRESSIVE: "🔥 AGGRESSIVE",
  CONSERVATIVE: "🟡 CONSERVATIVE",
  ERRATIC: "🔴 ERRATIC"
};

const behaviorLabel =
  behaviorLabelMap[telemetry.driver_behavior] ||
  telemetry.driver_behavior;


  return (
    <div
      className="min-h-screen bg-gradient-to-br from-black via-[#020617] to-black text-white px-10 py-8"
      style={{ color: "white" }}
    >
      {/* HEADER */}
      <header className="text-center mb-10">
        <h1 className="text-5xl font-bold tracking-wide">
          🏎️ AI-Driven F1 Telemetry Dashboard
        </h1>
        <p className="text-lg opacity-80 mt-3">
          Real-time telemetry with AI speed forecasting & behavior analysis
        </p>
      </header>

      {/* TOP METRICS */}
      <section className="grid grid-cols-5 gap-6 mb-12">
        <Metric title="AI STATUS" value={telemetry.status} />
        <Metric title="AVG SPEED" value={`${telemetry.avg_speed} km/h`} />
        <Metric
          title="AI SPEED FORECAST"
          value={
            telemetry.predicted_speed > telemetry.avg_speed
              ? `↑ ${telemetry.predicted_speed} km/h`
              : `↓ ${telemetry.predicted_speed} km/h`
          }
        />
        <Metric title="AVG RPM" value={telemetry.avg_rpm} />
        <Metric title="DRIVER BEHAVIOR" value={behaviorLabel} />
      </section>

      {/* MAIN HUD */}
      <section className="grid grid-cols-2 gap-10 mb-12 min-h-[420px]">
        {/* SPEED ARC */}
        <div className="bg-[#0b1220] rounded-3xl p-10 border border-white/10 flex flex-col justify-center">
          <h2 className="text-center text-2xl tracking-widest opacity-80 mb-8">
            SPEED
          </h2>

          <div className="relative flex justify-center">
            <svg width="360" height="200">
              <path
                d="M40 170 A140 140 0 0 1 320 170"
                stroke="#1f2937"
                strokeWidth="16"
                fill="none"
              />
              <path
                d="M40 170 A140 140 0 0 1 320 170"
                stroke={speedColor}
                strokeWidth="16"
                fill="none"
                strokeDasharray={arcLength}
                strokeDashoffset={arcOffset}
                style={{
                  filter: `drop-shadow(0 0 18px ${speedColor})`
                }}
              />
            </svg>

            <div className="absolute bottom-6 text-center">
              <div
                className="text-6xl font-extrabold"
                style={{
                  color: speedColor,
                  textShadow: `0 0 20px ${speedColor}`
                }}
              >
                {telemetry.avg_speed}
              </div>
              <div className="text-lg opacity-70">km/h</div>
            </div>
          </div>
        </div>

        {/* LIVE GRAPH */}
        <div className="bg-[#0b1220] rounded-3xl p-8 border border-white/10">
          <h2 className="text-center text-2xl tracking-widest opacity-80 mb-6">
            LIVE SPEED TELEMETRY
          </h2>

          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={history}>
              <XAxis hide />
              <YAxis domain={[0, MAX_SPEED]} stroke="#aaa" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#020617",
                  border: "1px solid #333",
                  color: "#fff"
                }}
              />
              <Line
                type="monotone"
                dataKey="speed"
                stroke={speedColor}
                strokeWidth={3}
                dot={false}
                isAnimationActive
                style={{
                  filter: `drop-shadow(0 0 14px ${speedColor})`
                }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* AI INSIGHTS */}
      <section className="bg-[#0b1220] rounded-3xl p-8 border border-white/10 max-w-6xl mx-auto">
        <h2 className="text-center text-2xl tracking-widest opacity-80 mb-6">
          🧠 AI INSIGHTS
        </h2>

        <ul className="space-y-4 text-lg opacity-85">
          <li>
            • Speed trend indicates{" "}
            <strong>
              {telemetry.predicted_speed > telemetry.avg_speed
                ? "acceleration"
                : "deceleration"}
            </strong>
          </li>
          <li>
            • Forecast suggests speed will{" "}
            <strong>
              {Math.abs(telemetry.predicted_speed - telemetry.avg_speed) < 5
                ? "remain stable"
                : telemetry.predicted_speed > telemetry.avg_speed
                ? "increase"
                : "decrease"}
            </strong>
          </li>
          <li>
            • Driving behavior classified as{" "}
            <strong>{telemetry.driver_behavior}</strong>
          </li>
        </ul>
      </section>
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div className="bg-[#0b1220] rounded-xl p-5 text-center border border-white/10">
      <div className="text-sm tracking-widest opacity-70 mb-1">
        {title}
      </div>
      <div className="text-2xl font-semibold">
        {value}
      </div>
    </div>
  );
}
