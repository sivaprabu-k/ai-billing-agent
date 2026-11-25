import {
  CheckCircle,
  CreditCard,
  RefreshCw,
  AlertCircle,
  UserPlus,
} from "lucide-react";

const activities = [
  {
    id: 1,
    title: "Payment received",
    description: "Payment of $249.00 received from John Smith",
    time: "2 minutes ago",
    icon: CheckCircle,
    color: "text-green-400",
    bg: "bg-green-500/10",
  },
  {
    id: 2,
    title: "New subscription",
    description: "Sarah Wilson subscribed to Pro Plan",
    time: "18 minutes ago",
    icon: UserPlus,
    color: "text-purple-400",
    bg: "bg-purple-500/10",
  },
  {
    id: 3,
    title: "Refund processed",
    description: "Refund of $89.00 processed for Mike Johnson",
    time: "42 minutes ago",
    icon: RefreshCw,
    color: "text-blue-400",
    bg: "bg-blue-500/10",
  },
  {
    id: 4,
    title: "Payment failed",
    description: "Payment of $129.00 failed for Emily Davis",
    time: "1 hour ago",
    icon: AlertCircle,
    color: "text-red-400",
    bg: "bg-red-500/10",
  },
  {
    id: 5,
    title: "Subscription renewed",
    description: "Enterprise Plan renewed successfully",
    time: "2 hours ago",
    icon: CreditCard,
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
  },
];

function RecentActivity() {
  return (
    <div className="rounded-xl border border-[#272731] bg-[#131319] p-5">

      <div className="mb-5 flex items-center justify-between">
        <div>
          <h3 className="text-base font-semibold text-white">
            Recent Activity
          </h3>
          <p className="mt-1 text-xs text-zinc-500">
            Latest billing events
          </p>
        </div>

        <button
          type="button"
          className="text-xs font-medium text-purple-400 transition hover:text-purple-300"
        >
          View all
        </button>
      </div>

      <div className="space-y-5">
        {activities.map((activity) => {
          const Icon = activity.icon;

          return (
            <div key={activity.id} className="flex items-start gap-3">
              <div
                className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${activity.bg}`}
              >
                <Icon size={17} className={activity.color} />
              </div>

              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium text-zinc-200">
                  {activity.title}
                </p>

                <p className="mt-1 text-xs leading-relaxed text-zinc-500">
                  {activity.description}
                </p>

                <p className="mt-1.5 text-[10px] text-zinc-600">
                  {activity.time}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default RecentActivity;
