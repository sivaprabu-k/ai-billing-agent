import type { ReactNode } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

interface DashboardLayoutProps {
  activePage: string;
  onNavigate: (page: string) => void;
  children: ReactNode;
}

function DashboardLayout({
  activePage,
  onNavigate,
  children,
}: DashboardLayoutProps) {
  return (
    <div className="flex h-screen overflow-hidden bg-[#080611] text-white">

      <aside className="sticky top-0 hidden h-screen shrink-0 lg:block">
        <Sidebar
          activePage={activePage}
          onNavigate={onNavigate}
        />
      </aside>

      <main className="flex h-screen min-w-0 min-h-0 flex-1 flex-col overflow-hidden">

        <div className="shrink-0">
          <Header activePage={activePage} />
        </div>

        <section className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 py-7 sm:px-7 sm:py-8 lg:px-10 lg:py-10">
          <div className="mx-auto w-full max-w-[1700px]">
            {children}
          </div>
        </section>

      </main>
    </div>
  );
}

export default DashboardLayout;
