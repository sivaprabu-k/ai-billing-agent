import type { LucideIcon } from "lucide-react";
import { TrendingDown, TrendingUp } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  change: string;
  trend: "up" | "down";
  description: string;
  icon: LucideIcon;
}

function StatCard({
  title,
  value,
  change,
  trend,
  description,
  icon: Icon,
}: StatCardProps) {
  const isPositive = trend === "up";

  return (
    <div className="rounded-xl border border-[#272731] bg-[#131319] p-5 transition hover:border-purple-500/30">

      <div className="mb-5 flex items-center justify-between">
        <p className="text-sm text-zinc-400">{title}</p>

        <div className="rounded-lg bg-purple-500/10 p-2">
          <Icon size={18} className="text-purple-400" />
        </div>
      </div>

      <h3 className="mb-3 text-2xl font-bold tracking-tight text-white">
        {value}
      </h3>

      <div className="flex flex-wrap items-center gap-2">
        <span
          className={`flex items-center gap-1 text-xs font-semibold ${
            isPositive ? "text-green-400" : "text-red-400"
          }`}
        >
          {isPositive ? (
            <TrendingUp size={14} />
          ) : (
            <TrendingDown size={14} />
          )}
          {change}
        </span>

        <span className="text-xs text-zinc-500">
          {description}
        </span>
      </div>
    </div>
  );
}

export default StatCard;
