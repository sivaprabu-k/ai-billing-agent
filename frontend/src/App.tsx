import { useState } from "react";
import DashboardLayout from "./components/layout/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import Customers from "./pages/Customers";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");

  return (
    <DashboardLayout
      activePage={activePage}
      onNavigate={setActivePage}
    >
      {activePage === "Dashboard" ? (
        <Dashboard />
      ) : activePage === "Customers" ? (
        <Customers />
      ) : (
        <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
          <h2 className="text-2xl font-bold text-white">
            {activePage}
          </h2>
          <p className="mt-2 text-sm text-zinc-500">
            This module is coming soon.
          </p>
        </div>
      )}
    </DashboardLayout>
  );
}

export default App;
