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
    <div className="flex min-h-screen bg-[#09090b] text-white">

      <div className="hidden lg:block">
        <Sidebar
          activePage={activePage}
          onNavigate={onNavigate}
        />
      </div>

      <main className="flex min-w-0 flex-1 flex-col">

        <Header activePage={activePage} />

        <section className="flex-1 overflow-y-auto p-5 md:p-8">
          <div className="mx-auto w-full max-w-[1600px]">
            {children}
          </div>
        </section>

      </main>
    </div>
  );
}

export default DashboardLayout;
