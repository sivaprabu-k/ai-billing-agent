import { Search, SlidersHorizontal } from "lucide-react";

interface CustomerToolbarProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
  statusFilter: string;
  onStatusChange: (value: string) => void;
}

function CustomerToolbar({
  searchTerm,
  onSearchChange,
  statusFilter,
  onStatusChange,
}: CustomerToolbarProps) {
  return (
    <div className="flex flex-col gap-3 rounded-xl border border-[#272731] bg-[#131319] p-4 sm:flex-row sm:items-center sm:justify-between">

      <div className="flex w-full items-center gap-2 rounded-lg border border-[#272731] bg-[#0d0d11] px-3 py-2.5 sm:max-w-md">
        <Search size={17} className="shrink-0 text-zinc-500" />

        <input
          type="text"
          value={searchTerm}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Search by name or email..."
          className="w-full bg-transparent text-sm text-white outline-none placeholder:text-zinc-600"
        />
      </div>

      <div className="flex items-center gap-2">
        <SlidersHorizontal size={16} className="text-zinc-500" />

        <select
          value={statusFilter}
          onChange={(event) => onStatusChange(event.target.value)}
          className="rounded-lg border border-[#272731] bg-[#0d0d11] px-3 py-2.5 text-sm text-zinc-300 outline-none focus:border-purple-500"
        >
          <option value="All">All Customers</option>
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
        </select>
      </div>

    </div>
  );
}

export default CustomerToolbar;
