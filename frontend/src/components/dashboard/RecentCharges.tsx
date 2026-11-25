import { ArrowUpRight } from "lucide-react";

const charges = [
  {
    id: "CHG-10245",
    customer: "John Smith",
    email: "john@example.com",
    plan: "Professional",
    amount: "$249.00",
    date: "Nov 25, 2026",
    status: "Succeeded",
  },
  {
    id: "CHG-10244",
    customer: "Sarah Wilson",
    email: "sarah@example.com",
    plan: "Enterprise",
    amount: "$499.00",
    date: "Nov 25, 2026",
    status: "Succeeded",
  },
  {
    id: "CHG-10243",
    customer: "Mike Johnson",
    email: "mike@example.com",
    plan: "Basic",
    amount: "$89.00",
    date: "Nov 24, 2026",
    status: "Refunded",
  },
  {
    id: "CHG-10242",
    customer: "Emily Davis",
    email: "emily@example.com",
    plan: "Professional",
    amount: "$249.00",
    date: "Nov 24, 2026",
    status: "Failed",
  },
  {
    id: "CHG-10241",
    customer: "David Brown",
    email: "david@example.com",
    plan: "Enterprise",
    amount: "$499.00",
    date: "Nov 23, 2026",
    status: "Pending",
  },
];

function RecentCharges() {
  return (
    <div className="overflow-hidden rounded-xl border border-[#272731] bg-[#131319]">

      <div className="flex items-center justify-between gap-3 p-5">
        <div>
          <h3 className="text-base font-semibold text-white">
            Recent Charges
          </h3>
          <p className="mt-1 text-xs text-zinc-500">
            Latest customer transactions
          </p>
        </div>

        <button
          type="button"
          className="flex items-center gap-1 text-xs font-medium text-purple-400 transition hover:text-purple-300"
        >
          View all
          <ArrowUpRight size={14} />
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[700px] text-left">
          <thead>
            <tr className="border-y border-[#272731] bg-[#0d0d11] text-[10px] uppercase tracking-wider text-zinc-500">
              <th className="px-5 py-3 font-medium">Charge ID</th>
              <th className="px-5 py-3 font-medium">Customer</th>
              <th className="px-5 py-3 font-medium">Plan</th>
              <th className="px-5 py-3 font-medium">Amount</th>
              <th className="px-5 py-3 font-medium">Date</th>
              <th className="px-5 py-3 font-medium">Status</th>
            </tr>
          </thead>

          <tbody>
            {charges.map((charge) => (
              <tr
                key={charge.id}
                className="border-b border-[#272731] last:border-0 transition hover:bg-[#1b1b24]/60"
              >
                <td className="px-5 py-4 text-xs font-medium text-purple-400">
                  {charge.id}
                </td>

                <td className="px-5 py-4">
                  <p className="text-xs font-medium text-zinc-200">
                    {charge.customer}
                  </p>
                  <p className="mt-1 text-[10px] text-zinc-500">
                    {charge.email}
                  </p>
                </td>

                <td className="px-5 py-4 text-xs text-zinc-400">
                  {charge.plan}
                </td>

                <td className="px-5 py-4 text-xs font-semibold text-white">
                  {charge.amount}
                </td>

                <td className="px-5 py-4 text-xs text-zinc-400">
                  {charge.date}
                </td>

                <td className="px-5 py-4">
                  <span
                    className={`inline-flex rounded-full px-2.5 py-1 text-[10px] font-medium ${
                      charge.status === "Succeeded"
                        ? "bg-green-500/10 text-green-400"
                        : charge.status === "Failed"
                          ? "bg-red-500/10 text-red-400"
                          : charge.status === "Refunded"
                            ? "bg-blue-500/10 text-blue-400"
                            : "bg-yellow-500/10 text-yellow-400"
                    }`}
                  >
                    {charge.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RecentCharges;
