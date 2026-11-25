import {
  Users,
  UserCheck,
  UserPlus,
  UserX,
} from "lucide-react";

import StatCard from "./StatCard";

const customerStats = [
  {
    title: "Total Customers",
    value: "3,842",
    change: "+12.5%",
    trend: "up" as const,
    description: "vs. last month",
    icon: Users,
  },
  {
    title: "Active Customers",
    value: "3,216",
    change: "+8.4%",
    trend: "up" as const,
    description: "vs. last month",
    icon: UserCheck,
  },
  {
    title: "New Customers",
    value: "284",
    change: "+15.2%",
    trend: "up" as const,
    description: "vs. last month",
    icon: UserPlus,
  },
  {
    title: "Inactive Customers",
    value: "626",
    change: "-3.5%",
    trend: "down" as const,
    description: "vs. last month",
    icon: UserX,
  },
];

function CustomerStats() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {customerStats.map((stat) => (
        <StatCard key={stat.title} {...stat} />
      ))}
    </div>
  );
}

export default CustomerStats;
