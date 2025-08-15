import React, { useState } from "react";
import {
  LayoutDashboard,
  ShieldCheck,
  UserPlus,
  Users,
  FileText,
  BarChart3,
} from "lucide-react";

const NAV = [
  { key: "main", label: "Main", icon: LayoutDashboard },
  { key: "check", label: "Check ads", icon: ShieldCheck },
  { key: "new-client", label: "New Client", icon: UserPlus },
  { key: "client", label: "Client", icon: Users },
  { key: "ord", label: "ORD", icon: FileText },
  { key: "stat", label: "Statistic", icon: BarChart3 },
];

function Sidebar({ active, onSelect }) {
  return (
    <aside className="flex flex-col h-screen w-[15rem] border-r-2 border-gray-700 bg-white dark:bg-gray-900 dark:border-gray-700">
      <div className="flex flex-col w-full h-full">
        {NAV.map(({ key, label, icon: Icon }, idx) => {
          const isActive = active === key;
          return (
            <button
              key={key}
              onClick={() => onSelect(key)}
              className={[
                "w-full flex-1 select-none", // растягивание по высоте
                "flex flex-col items-center justify-center",
                "px-6", // уменьшена ширина
                "gap-4",
                "text-6xl font-extrabold tracking-tight", // увеличенный шрифт в 2 раза
                "bg-white dark:bg-gray-900",
                "text-gray-900 dark:text-gray-100",
                "transition-colors duration-150",
                idx !== 0 ? "border-t-2 border-gray-300 dark:border-gray-700" : "",
                isActive ? "ring-2 ring-gray-800 dark:ring-gray-200" : "hover:bg-gray-100 dark:hover:bg-gray-800",
              ].join(" ")}
            >
              <Icon className="h-20 w-20" />
              <span className="text-center leading-none">{label}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
}

export default function CRMMainLayout() {
  const [active, setActive] = useState("main");

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <Sidebar active={active} onSelect={setActive} />
      <main className="flex-1 p-12 overflow-y-auto">
        {active === "main" && (
          <div>
            <h1 className="text-5xl font-bold mb-12">Главная</h1>
            <p className="text-xl">Это главная страница CRM. Здесь будет строгий UI и основные данные.</p>
          </div>
        )}
        {active !== "main" && (
          <div>
            <h1 className="text-5xl font-bold mb-12">{NAV.find((n) => n.key === active)?.label}</h1>
            <p className="text-xl">Содержимое страницы {active} появится здесь.</p>
          </div>
        )}
      </main>
    </div>
  );
}
