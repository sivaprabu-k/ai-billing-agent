import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const revenueData = [
  { month: "Jan", revenue: 18000 },
  { month: "Feb", revenue: 22000 },
  { month: "Mar", revenue: 19500 },
  { month: "Apr", revenue: 28000 },
  { month: "May", revenue: 25000 },
  { month: "Jun", revenue: 32000 },
  { month: "Jul", revenue: 29000 },
  { month: "Aug", revenue: 38000 },
  { month: "Sep", revenue: 35000 },
  { month: "Oct", revenue: 42000 },
  { month: "Nov", revenue: 48294 },
  { month: "Dec", revenue: 45000 },
];

// Demo payment status data
const paymentStatusData = [
  { name: "Succeeded", value: 68, color: "#22c55e" },
  { name: "Failed", value: 12, color: "#ef4444" },
  { name: "Pending", value: 8, color: "#f59e0b" },
  { name: "Refunded", value: 12, color: "#3b82f6" },
];

function RevenueChart() {
  return (
    <div className="grid min-w-0 grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1.8fr)_minmax(280px,1fr)]">

      {/* Revenue Overview */}
      <div className="min-w-0 rounded-xl border border-[#272731] bg-[#131319] p-5 sm:p-6">
        <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h3 className="text-base font-semibold text-white">
              Revenue Overview
            </h3>
            <p className="mt-1 text-xs text-zinc-500">
              Monthly revenue performance
            </p>
          </div>

          <select
            defaultValue="2026"
            className="rounded-lg border border-[#272731] bg-[#1b1b24] px-3 py-2 text-xs text-zinc-300 outline-none focus:border-purple-500"
          >
            <option value="2026">2026</option>
            <option value="2025">2025</option>
          </select>
        </div>

        <div className="h-[280px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={revenueData}
              margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
            >
              <defs>
                <linearGradient
                  id="revenueGradient"
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop offset="0%" stopColor="#9333ea" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#9333ea" stopOpacity={0} />
                </linearGradient>
              </defs>

              <CartesianGrid
                stroke="#272731"
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="month"
                stroke="#71717a"
                tick={{ fill: "#a1a1aa", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                stroke="#71717a"
                tick={{ fill: "#a1a1aa", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(value: number) => `$${value / 1000}k`}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#1b1b24",
                  border: "1px solid #383843",
                  borderRadius: "8px",
                  color: "#fff",
                  fontSize: "12px",
                }}
                formatter={(value) => [
                  `$${Number(value).toLocaleString("en-US")}`,
                  "Revenue",
                ]}
              />

              <Area
                type="monotone"
                dataKey="revenue"
                stroke="#a855f7"
                strokeWidth={2.5}
                fill="url(#revenueGradient)"
                activeDot={{ r: 5, fill: "#a855f7" }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Payment Status Breakdown */}
      <div className="min-w-0 rounded-xl border border-[#272731] bg-[#131319] p-5 sm:p-6">
        <div className="mb-2">
          <h3 className="text-base font-semibold text-white">
            Payment Status
          </h3>
          <p className="mt-1 text-xs text-zinc-500">
            Breakdown of payment transactions
          </p>
        </div>

        <div className="relative mx-auto h-[220px] w-full max-w-[280px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={paymentStatusData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={65}
                outerRadius={90}
                paddingAngle={4}
                stroke="none"
              >
                {paymentStatusData.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>

              <Tooltip
                contentStyle={{
                  backgroundColor: "#1b1b24",
                  border: "1px solid #383843",
                  borderRadius: "8px",
                  color: "#fff",
                  fontSize: "12px",
                }}
                formatter={(value, name) => [`${value}%`, name]}
              />
            </PieChart>
          </ResponsiveContainer>

          <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-3xl font-bold text-white">100%</span>
            <span className="mt-1 text-xs text-zinc-500">Transactions</span>
          </div>
        </div>

        <div className="mt-3 grid grid-cols-2 gap-x-4 gap-y-4">
          {paymentStatusData.map((item) => (
            <div key={item.name} className="flex min-w-0 items-center gap-2">
              <span
                className="h-2.5 w-2.5 shrink-0 rounded-full"
                style={{ backgroundColor: item.color }}
              />

              <div className="min-w-0">
                <p className="truncate text-xs text-zinc-400">
                  {item.name}
                </p>
                <p className="mt-0.5 text-sm font-semibold text-white">
                  {item.value}%
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}

export default RevenueChart;
