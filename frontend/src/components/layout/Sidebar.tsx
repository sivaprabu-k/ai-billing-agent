import {
  LayoutDashboard,
  Users,
  CreditCard,
  Receipt,
  FileText,
  Bot,
  ClipboardCheck,
  History,
  Settings,
  HelpCircle,
  ChevronLeft,
  Zap,
} from "lucide-react";

interface SidebarProps {
  activePage: string;
  onNavigate: (page: string) => void;
}

const navigationItems = [
  {
    title: "OVERVIEW",
    items: [
      { label: "Dashboard", icon: LayoutDashboard },
    ],
  },
  {
    title: "BILLING",
    items: [
      { label: "Customers", icon: Users },
      { label: "Subscriptions", icon: CreditCard },
      { label: "Charges", icon: Receipt },
      { label: "Invoices", icon: FileText },
    ],
  },
  {
    title: "AI OPERATIONS",
    items: [
      { label: "AI Assistant", icon: Bot },
      { label: "Approvals", icon: ClipboardCheck },
      { label: "Audit Log", icon: History },
    ],
  },
];

function Sidebar({ activePage, onNavigate }: SidebarProps) {
  return (
    <aside className="flex h-screen w-[260px] shrink-0 flex-col border-r border-[#272731] bg-[#0d0d11]">

      <div className="flex h-[76px] items-center justify-between border-b border-[#272731] px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-600 shadow-lg shadow-purple-900/30">
            <Zap size={20} className="text-white" />
          </div>

          <div>
            <h1 className="text-sm font-bold tracking-wide text-white">
              BILLING<span className="text-purple-400">AI</span>
            </h1>
            <p className="text-[10px] tracking-wider text-zinc-500">
              INTELLIGENT FINANCE
            </p>
          </div>
        </div>

        <button
          type="button"
          aria-label="Collapse sidebar"
          className="rounded-lg p-1.5 text-zinc-500 transition hover:bg-[#1b1b24] hover:text-white"
        >
          <ChevronLeft size={17} />
        </button>
      </div>

      <nav className="flex-1 space-y-7 overflow-y-auto px-4 py-7">
        {navigationItems.map((section) => (
          <div key={section.title}>
            <p className="mb-3 px-3 text-[10px] font-semibold tracking-[1.5px] text-zinc-600">
              {section.title}
            </p>

            <div className="space-y-1">
              {section.items.map((item) => {
                const Icon = item.icon;
                const isActive = activePage === item.label;

                return (
                  <button
                    key={item.label}
                    type="button"
                    onClick={() => onNavigate(item.label)}
                    className={`group flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-[13px] transition-all duration-200 ${
                      isActive
                        ? "border border-purple-500/20 bg-purple-500/10 text-purple-400 shadow-[0_0_18px_rgba(147,51,234,0.08)]"
                        : "text-zinc-400 hover:bg-[#1b1b24] hover:text-white"
                    }`}
                  >
                    <Icon
                      size={17}
                      className={
                        isActive
                          ? "text-purple-400"
                          : "text-zinc-500 group-hover:text-white"
                      }
                    />

                    <span className="flex-1 font-medium">
                      {item.label}
                    </span>

                    {item.label === "Approvals" && (
                      <span className="rounded-full bg-red-500/15 px-2 py-0.5 text-[10px] font-semibold text-red-400">
                        3
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* AI Assistant Card */}
      <div className="mx-4 mb-5 rounded-xl border border-purple-500/20 bg-gradient-to-br from-purple-500/10 to-transparent p-4">
        <div className="mb-2 flex items-center gap-2">
          <Bot size={17} className="text-purple-400" />
          <span className="text-xs font-semibold text-white">
            AI Billing Agent
          </span>
        </div>

        <p className="mb-3 text-[11px] leading-relaxed text-zinc-400">
          Need help investigating a billing issue?
        </p>

        <button
          type="button"
          onClick={() => onNavigate("AI Assistant")}
          className="w-full rounded-lg bg-purple-600 px-3 py-2 text-xs font-semibold text-white transition hover:bg-purple-500"
        >
          Ask AI Assistant
        </button>
      </div>

      <div className="border-t border-[#272731] px-4 py-4">
        <button
          type="button"
          onClick={() => onNavigate("Settings")}
          className={`mb-1 flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition hover:bg-[#1b1b24] ${
            activePage === "Settings"
              ? "text-purple-400"
              : "text-zinc-400 hover:text-white"
          }`}
        >
          <Settings size={17} />
          Settings
        </button>

        <button
          type="button"
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-[#1b1b24] hover:text-white"
        >
          <HelpCircle size={17} />
          Help & Support
        </button>

        <div className="mt-4 flex items-center gap-3 border-t border-[#272731] pt-4">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-purple-500/20 text-xs font-bold text-purple-300">
            SA
          </div>

          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-semibold text-white">
              Admin User
            </p>
            <p className="text-[10px] text-zinc-500">
              Administrator
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
