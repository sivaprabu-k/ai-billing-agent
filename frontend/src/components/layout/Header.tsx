import {
  Search,
  Bell,
  ChevronDown,
  CalendarDays,
} from "lucide-react";

interface HeaderProps {
  activePage: string;
}

function Header({ activePage }: HeaderProps) {
  return (
    <header className="flex min-h-[76px] items-center justify-between gap-4 border-b border-[#272731] bg-[#0d0d11] px-8">

      <div>
        <div className="mb-1 flex items-center gap-2 text-[11px] text-zinc-500">
          <span>Workspace</span>
          <span>/</span>
          <span className="text-purple-400">{activePage}</span>
        </div>

        <h2 className="text-lg font-semibold text-white">
          {activePage}
        </h2>
      </div>

      <div className="flex items-center gap-5">

        <div className="hidden w-64 items-center gap-2 rounded-lg border border-[#272731] bg-[#131319] px-3 py-2.5 md:flex">
          <Search size={16} className="text-zinc-500" />

          <input
            type="text"
            placeholder="Search anything..."
            className="w-full bg-transparent text-xs text-white outline-none placeholder:text-zinc-600"
          />

          <span className="rounded border border-[#383843] px-1.5 py-0.5 text-[9px] text-zinc-500">
            /
          </span>
        </div>

        <div className="hidden items-center gap-2 text-xs text-zinc-400 lg:flex">
          <CalendarDays size={15} />
          <span>
            {new Date().toLocaleDateString("en-IN", {
              day: "2-digit",
              month: "short",
              year: "numeric",
            })}
          </span>
        </div>

        <button
          type="button"
          aria-label="Notifications"
          className="relative rounded-lg p-2 text-zinc-400 transition hover:bg-[#1b1b24] hover:text-white"
        >
          <Bell size={19} />

          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full border-2 border-[#0d0d11] bg-purple-500" />
        </button>

        <button
          type="button"
          className="flex items-center gap-2 border-l border-[#272731] pl-4"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-purple-500/20 text-xs font-bold text-purple-300">
            SA
          </div>

          <div className="hidden text-left sm:block">
            <p className="text-xs font-semibold text-white">
              Admin User
            </p>
            <p className="text-[10px] text-zinc-500">
              Administrator
            </p>
          </div>

          <ChevronDown size={14} className="text-zinc-500" />
        </button>

      </div>
    </header>
  );
}

export default Header;
