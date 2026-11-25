import DashboardStats from "../components/dashboard/DashboardStats";
import RevenueChart from "../components/dashboard/RevenueChart";
import RecentActivity from "../components/dashboard/RecentActivity";
import RecentCharges from "../components/dashboard/RecentCharges";

function Dashboard() {
  return (
    <div className="space-y-6">

      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Dashboard Overview
          </h1>
          <p className="mt-1 text-sm text-zinc-500">
            Monitor your billing performance and AI operations.
          </p>
        </div>

        <div className="rounded-lg border border-purple-500/20 bg-purple-500/10 px-3 py-2">
          <p className="text-xs font-medium text-purple-300">
            <span className="mr-2 inline-block h-2 w-2 rounded-full bg-green-400" />
            AI Agent Online
          </p>
        </div>
      </div>

      <DashboardStats />

      <div className="grid grid-cols-1 gap-5 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <RevenueChart />
        </div>

        <RecentActivity />
      </div>

      <RecentCharges />

    </div>
  );
}

export default Dashboard;
