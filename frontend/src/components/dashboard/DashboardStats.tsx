import {
  DollarSign,
  CreditCard,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

import StatCard from "./StatCard";

const stats = [
  {
    title: "Monthly Revenue",
    value: "$48,294.00",
    change: "+12.8%",
    trend: "up" as const,
    description: "vs. last month",
    icon: DollarSign,
  },
  {
    title: "Active Subscriptions",
    value: "2,845",
    change: "+8.2%",
    trend: "up" as const,
    description: "vs. last month",
    icon: CreditCard,
  },
  {
    title: "Successful Payments",
    value: "4,892",
    change: "+5.4%",
    trend: "up" as const,
    description: "vs. last month",
    icon: CheckCircle,
  },
  {
    title: "Failed Charges",
    value: "126",
    change: "-3.2%",
    trend: "down" as const,
    description: "vs. last month",
    icon: AlertCircle,
  },
];

function DashboardStats() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <StatCard key={stat.title} {...stat} />
      ))}
    </div>
  );
}

export default DashboardStats;
